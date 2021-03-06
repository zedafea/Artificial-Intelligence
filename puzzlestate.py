import queue as Q
import time
import sys
import math
class PuzzleState:
    def __init__(self,config,n,parent=None,action='Initial',cost=0):
        if n*n != len(config) or n<2:
            raise Exception("the lenght of config is not correct")
        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.dimension = n
        self.config = config
        self.children = []
        for i,item in enumerate(self.config):
            if item == 0:
                self.blank_row = i//self.n
                self.blank_col = i%self.n
                break
    def __lt__(self, other):
    selfPriority = (self.cost, self.config)
    otherPriority = (other.cost, other.config)
    return selfPriority < otherPriority

    
    def display(self):
        for i in range(self.n):
            line=[]
            offset=i*self.n
            for j in range(self.n):
                line.append(self.config[offset + j])
            print(line)
            
    def move_left(self):
        if self.blank_col==0:
            return None
        else:
            blank_index=self.blank_row*self.n + self.blank_col
            target=blank_index-1
            new_config=list(self.config)
            new_config[blank_index],new_config[target]=new_config[target],new_config[blank_index]
            return PuzzleState(tuple(new_config),self.n,parent=self,action="Left",cost=self.cost+1)
    
    def move_right(self):
        if self.blank_col==self.n-1:
            return None
        else:
            blank_index=self.blank_row*self.n + self.blank_col
            target=blank_index + 1
            new_config=list(self.config)
            new_config[blank_index],new_config[target]=new_config[target],new_config[blank_index]
            return PuzzleState(tuple(new_config),self.n,parent=self,action="Right",cost=self.cost + 1)
    
    def move_up(self):
        if self.blank_row==0:
            return None
        else:
            blank_index=self.blank_row*self.n + self.blank_col
            target=blank_index - self.n
            new_config=list(self.config)
            new_config[blank_index],new_config[target]=new_config[target],new_config[blank_index]
            return PuzzleState(tuple(new_config),self.n,parent=self,action="Up",cost=self.cost + 1)
    
    def move_down(self):
        if self.blank_row==self.n-1:
            return None
        else:
            blank_index=self.blank_row*self.n+self.blank_col
            target=blank_index+self.n
            new_config=list(self.config)
            new_config[blank_index],new_config[target]=new_config[target],new_config[blank_index]
            return PuzzleState(tuple(new_config),self.n,parent=self,action="Down",cost=self.cost+1)
   
    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:

                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:

                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:

                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:

                self.children.append(right_child)

        return self.children

def writeOutput(tm,state,max_search_depth,state_cost,l):
    path = []
    while state.parent != None:
        path.append(state.action)
        state = state.parent
    
    state_path = path[::-1]
    search_depth = state.n
    running_time = tm
    print(state_path,"\n",state_cost,"\n",search_depth,"\n",len(l) - 1,'\n',max_search_depth,"\n",running_time,'\n')

def bfs_search(initial_state):
    """bfs search"""   
    tm = time.time()
    explored = []
    l =[]
    max_search_depth = 0
    frontier = Q.Queue()
    frontier.put(initial_state)
    while not frontier.empty():
        state = frontier.get() 
        if state.config not in l:
            l.append(state.config)
        explored.append(state)
        
        if test_goal(state):
            
            state_cost = state.cost
            if state.n <= state_cost :
                max_search_depth = state_cost + 1
            else:
                max_search_depth = state.n
            return writeOutput(tm,state,max_search_depth,state_cost,l)
            
        else:
            
            for i in state.expand():
                
                if i not in explored and i not in frontier.queue:
                    frontier.put(i)
                    
    return writeOutput(tm)

def dfs_search(initial_state):
    explored = []
    tm = time.time()
    l = []
    d = [0]
    c = 0
    frontier = Q.LifoQueue()
    frontier.put(initial_state)
    while not frontier.empty():
        state = frontier.get() 
        if state.config not in l:
            l.append(state.config)
        explored.append(state)
        
        if test_goal(state):
            state_cost = state.cost
            max_search_depth = d[-1]
            return writeOutput(tm,state,state_cost,max_search_depth,l)
        else:
            for i in state.expand():
                if i not in explored and i not in frontier.queue:
                    frontier.put(i)
                    if state.parent != None:
                        state.parent = c
                        if c.n >= d[-1]:
                            d.append(state.n)
    return writeOutput(tm)

def A_star_search(initial_state):
    tm = time.time()
    explored = []
    l = []
    frontier = Q.PriorityQueue()
    frontier.put((initial_state.cost,initial_state))
    while not frontier.empty():
        state = frontier.get()
        state = state[1]
        explored.append(state)
        if state.config not in l:
            l.append(state.config)
    
        if test_goal(state):
            max_search_depth = state.n
            state_cost = state.cost
            return writeOutput(tm,state,state_cost,max_search_depth,l)
        else:
            for child in state.expand():
                
                if child not in explored and child not in frontier.queue:
                    
                    total_cost = child.cost + calculate_mahn_dist(child)
                    frontier.put((total_cost,child))
                elif child in frontier.queue:
                    frontier.get(child)
                    
                    new_cost = child.cost + calculate_mahn_dist(child)
                    frontier.put((new_cost,child))
                    
    return writeOutput(tm)

def calculate_mahn_dist(state):
    
    mahn_dist = []
    n = state.dimension
    for i,value in enumerate(state.config):
        v_row = value//n
        v_col = value%n
        goal_row = i//n
        goal_col = i%n
        if v_row == goal_row:
            if v_col == goal_col:
                mahn_dist.append(0)
            else:
                mahn_dist.append(abs(v_col-goal_col))
        else:
            if v_col == goal_col:
                mahn_dist.append(abs(v_row-goal_row))
            else:
                mahn_dist.append(abs(v_row-goal_row)+abs(v_col-goal_col))
        mahn_dist = sum(mahn_dist)
        return mahn_dist
        
def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""
    return state.cost()

def calculate_manhattan_dist(state):

    """calculate the manhattan distance of a tile"""
    

def test_goal(state):

    """test the state is the goal state or not"""
    
    if state.config == (0,1,2,3,4,5,6,7,8):
        return True
    else:
        return False

# Main Function that reads in Input and Runs corresponding Algorithm

def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":

        bfs_search(hard_state)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")

if __name__ == '__main__':

    main()     
    
        
