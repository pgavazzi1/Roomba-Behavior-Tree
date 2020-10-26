 #
 # behavior_tree.py
 # COMP131
 # Fall 2020
 #
 # Simulates the behavior tree with also classes for parts of the tree such as
 # Tasks, conditions, composities, and decorators
 #
 

################# Tree #################
 
class Tree:
    
    # function name: constructor
    # Parameters: A node that will be the root of the tree
    # Returns: nothing
    # Does: creates a tree object with a root node and a stack to later use to
    #       execute nodes.
    def __init__(self, root_node):
        self.root = root_node
        self.node_stack = []
    
       
    # function name: run_tree
    # Parameters: A blackboard for the behavior tree
    # Returns: nothing
    # Does: Starts the behavior tree simulation with it's root node, then 
    #       calls another funtion that resets all nodes in the tree to say
    #       They have not been executed yet if there is not currnetly 
    #       running nodes.
    def run_tree(self, blackboard):
        self.root.execute(blackboard, self.node_stack)
        if self.root.executed_result != 'RUNNING':
            self.root.reset_node()
    


    
    

################# Nodes #################
class task:
    
    # function name: constructor
    # Parameters: Takes in a task name, string that tells the node if it will 
    #             either write to the blackboard or recive info from it,  
    #             a key that tells the node where in the blackbaord to look,
    #             And finally a bolean of what it will be changing in the 
    #             blackbaord.
    # Returns: nothing
    # Does: Creates a node that will be capable of carrying out a task with 
    #       a task name, a black board key and instructions on what to do
    #       with the blackbaord, as well as the results of it's last 
    #       run and a boolean that says if it has been executed or not
    def __init__(self, task, need_blackbaord, blackbaord_key, to_change):
        self.node_task            = task
        self.need_blackbaord      = need_blackbaord
        self.blackbaord_key       = blackbaord_key
        self.new_variable         = to_change
        self.executed_result      = None
        self.was_executed         = False


    # function name: execute
    # Parameters: A balckboard for the simulation, and a stack with the 
    #             previously executed nodes
    # Returns: Returns 'SUCCEEDED' if the task was carried out as expecyed,
    #          returns 'FAILED' otherwise
    # Does: Changes the nodes status to executed, and then carrys out a nodes 
    #       task and returns the result 
    def execute(self, blackboard, stack):
        
        
        self.was_executed = True
        
        #Make the node do it's task and then return SUCCEEDED if the node 
        #completes it
        if self.need_blackbaord is None:
             self.executed_result = 'SUCCEEDED'
             return 'SUCCEEDED'
        elif self.need_blackbaord == 'write' :
            blackboard[self.blackbaord_key] = self.new_variable
            self.executed_result = 'SUCCEEDED'
            return 'SUCCEEDED'
        elif self.need_blackbaord == 'recive' :
            blackboard[self.blackbaord_key]
            self.executed_result = 'SUCCEEDED'
            return 'SUCCEEDED'
        
        #Return false if node failed it's task
        self.print_task(False)
        self.executed_result = 'FAILED'
        return 'FAILED'
    
    # function name:reset_node
    # Parameters: none
    # Returns: nothing
    # Does: Changes the node's indication that it has already been executed to
    #       show that it can be run again
    def reset_node(self): 
        self.executed_result = None
        self.was_executed    = False
 
            
        

class condition:
    
    # function name: constructor
    # Parameters: A condition key which gives the location of the condition 
    #             the node will be checking in the blackbaord 
    # Returns: nothing
    # Does: Creates a conditon node that will be able to check a condtion in 
    #       the blackbaord with a blackboard key as well as the results of 
    #       its last run, and a boolean that says if it has been executed or 
    #       not
    def __init__(self, condition):
        self.condition_key   = condition
        self.executed_result = None
    
    # function name: execute
    # Parameters: none
    # Returns: 'SUCCEEDED' if the conditon was true, 'FAILED' if the condition
    #           the conditon was false 
    # Does: Changes the node's status to executed, and then checks the node's
    #       assigned condition in the blackboard 
    def execute(self, blackboard, stack): 
        
        self.was_executed = True
        
        #Return based on how the condition returns 
        if blackboard[self.condition_key] :
            self.executed_result = 'SUCCEEDED'
            return 'SUCCEEDED'
        
        self.executed_result = 'FAILED'
        return 'FAILED'
    
    # function name:reset_node
    # Parameters: none
    # Returns: nothing
    # Does: Changes the node's indication that it has already been executed to
    #       show that it can be run again
    def reset_node(self): 
        self.executed_result = None
        self.was_executed    = False
 

     
         
     


############ Composities #################
class priority:
    
    # function name: constructor
    # Parameters: a list of children that are arranged in the order for which
    #             they are to be evealuated
    # Returns: nothing
    # Does: creates  a prioty node with cildren in there correct heirachicale
    #       order as well as as well as the results of its last run, and a 
    #       boolean that says if it has been executed or not
    def __init__(self, children_list):
        self.priority_children   = children_list
        self.executed_result = None
        self.was_executed    = False
    
    # function name: execute_running
    # Parameters: A blackbaord for the simulation, and a stack with currently 
    #             running nodes, and the current child we are working with in
    #             in the priority node
    # Returns: 'RUNNING' if the node is still running, or will return what 
    #           the rest of the branch ends up doing
    # Does: Executes the currently running node (loacted at the back of the 
    #       stack), then returns running if it is still running or executes
    #       the rest of the nodes after it if the running node has finished
    #       and returns the result
    def execute_running(self, Blackboard, stack, child):
        
        #Execute the running node stored at the back of the stack
        stack[-1].execute(Blackboard, stack)
        
        #Returns running if the node is stil running 
        if stack[-1].executed_result == 'RUNNING':
            self.executed_result = 'RUNNING'
            return 'RUNNING'
       
        #If node is finished running, then clear all running nodes, get rid of    
        #the current running branch, and execute/return the result of the rest
        #of the nodes in the branch
        elif stack[-1].executed_result == 'SUCCEEDED':
            stack.clear()
            Blackboard['RUNNING_BRANCH'].pop()
            self.executed_result = 'SUCCEEDED'
            child.execute(Blackboard, stack)
            self.was_executed    = True
            return 'SUCCEEDED'
        
    # function name: execute
    # Parameters: A blackbaord for the simulation, and a stack with currently 
    #             running nodes
    # Returns: SUCCEEDED if one of its child returns that, FAILED if all child
    #          failed, or RUNNING if it's child is running
    # Does: Executes each of it's child in priority order, and jumps to a 
    #       running node if it's child contains a branch with one 
    def execute(self, Blackboard, stack):
        for child in self.priority_children :
            
            #Call a function that executes a branch with a running node in it
            #and return the result
            if  Blackboard['RUNNING_BRANCH']:
                if child == Blackboard['RUNNING_BRANCH'][-1]:
                    self.executed_result = self.execute_running(Blackboard, 
                                                                stack, child)
                    return self.executed_result
            
            child.reset_node()
            
            # Else, return add the node to the stack of running nodes, execute 
            # it, and print out it's success or failure if it is a task
            stack.append(child) 
            result = child.execute(Blackboard, stack)
            if isinstance(child, task):
                    print(child.node_task,':', result)
                    
            # Return result of node, and add it's branch to list of RUNNING 
            # nodes if it's branch still hasa running node.
            if child.executed_result == 'SUCCEEDED':
                stack.pop() 
                self.executed_result = 'SUCCEEDED'
                self.was_executed    = True
                return 'SUCCEEDED'
            
            elif child.executed_result == 'RUNNING':
                Blackboard['RUNNING_BRANCH'].append(child) 
                self.executed_result = 'RUNNING'
                return 'RUNNING'
            stack.pop() 
            
        #return false if no nodes returned SUCCEEDED or RUNNING
        self.executed_result = 'FAILED' 
        self.was_executed    = True
        return 'FAILED' 
    
    
    # function name: reset_node
    # Parameters: none
    # Returns: nothing
    # Does: Calls the same function in all of it's children, then changes it's
    #       executed boolean to false so it can be executed again
    def reset_node(self): 
        for child in self.priority_children :
            child.reset_node()
        self.executed_result = None
        self.was_executed    = False
  
    
  
    
class selector:
    
    # function name: constructor
    # Parameters: A list of children
    # Returns: nothing
    # Does: Creates a selector node with children, the results of it's last 
    #       run, and a boolean that says if it has been executed or not
    def __init__(self, children_list):
        self.children         = children_list
        self.executed_result  = None
        self.was_executed     = False
    
    
    # function name: execute
    # Parameters: A blackbaord for the simulation, and a stack with currently 
    #             running nodes
    # Returns: SUCCEEDED if at lest one of its nodes succeeds, RUNNING if one 
    #          of it's nodes is still running, and FAILED if none of it's 
    #          children succeede
    # Does: Goes through each of it's children and if they have not been 
    #       executed, run them until one of the children succeedes
    def execute(self, Blackboard, stack):
        
        for child in self.children :

        
            #If node has been executed, go on to next node
            if self.was_executed == True :
                continue
            stack.append(child) 
            
            #If node has been executed if it has not finished yet
            if (child.executed_result == None 
                or child.executed_result == 'RUNNING') :
                #for each child, add it to stack and then execute it, print the
                #result if it is a task
                result = stack[-1].execute(Blackboard, stack)
                if isinstance(child, task):
                        print(child.node_task,':', result)
               
            #get it off the stack if it succeeded, else keep it on the stack
            #if it is running
            if child.executed_result == 'SUCCEEDED':
                stack.pop() 
                self.executed_result = 'SUCCEEDED'
                self.was_executed    = True
                return 'SUCCEEDED' 
            if child.executed_result == 'RUNNING':
                self.executed_result = 'RUNNING'
                return 'RUNNING'
            stack.pop() 
        
        #set the node to executed and return FAILED if no nodes returned 
        # SUCCEEDED
        self.executed_result = 'FAILED'
        self.was_executed    = True
        return 'FAILED' 
    
    # function name: reset_node
    # Parameters: none
    # Returns: nothing
    # Does: Calls the same function in all of it's children, then changes it's
    #       executed boolean to false so it can be executed again
    def reset_node(self): 
        for child in self.children :
            child.reset_node()
        self.executed_result = None
        self.was_executed    = False
    
    
   
    
   
    
    
class sequence:
    
    # function name: constructor
    # Parameters: A list of children
    # Returns: nothing
    # Does: Creates a sequence node with children and boolean that says if it 
    #       has been executed or not. It also stores it's last runtime result
    def __init__(self, children_list):
         self.children         = children_list
         self.executed_result  = None
         self.was_executed     = False

    
    # function name: execute
    # Parameters: A blackbaord for the simulation, and a stack with currently 
    #             running nodes
    # Returns: RUNNING if one of its children is still running,  SUCCEEDED if
    #          all of its children return succeeded, failed if one of its 
    #          children returns failed
    # Does: Goes through each of it's children and if they have not been 
    #       executed, run them until one of the children fails
    def execute(self, Blackboard, stack):
        
        
        for child in self.children :
            # If node has been executed, go on to next node.. else put it on 
            # the stack
            if self.was_executed == True :
                continue

            stack.append(child) 
            #If node has been executed already, go on to next node
            if (child.executed_result == None 
                or child.executed_result == 'RUNNING') :
                result = stack[-1].execute(Blackboard, stack)       
                if isinstance(child, task):
                        print(child.node_task,':', result)
               
            #get it off the stack if it failed and return, else keep it on
            #the stack if it is still running
            if child.executed_result == 'FAILED':
                stack.pop() 
                self.executed_result = 'FAILED'
                self.was_executed    = True
                return 'FAILED' 
            if child.executed_result == 'RUNNING':
                self.executed_result = 'RUNNING' 
                return 'RUNNING' 
            
            #make sure to pop it off if it succeeded
            stack.pop() 
        self.executed_result = 'SUCCEEDED'
        self.was_executed    = True
        return 'SUCCEEDED'
    
    # function name: reset_node
    # Parameters: none
    # Returns: nothing
    # Does: Calls the same function in all of it's children, then changes it's
    #       executed boolean to false so it can be executed again
    def reset_node(self): 
        self.executed_result = None
        self.was_executed    = False
        for child in self.children :
            child.reset_node()

         






    
########### Decorators #################

class negation:
    
    # function name:constructor
    # Parameters: a child for the node
    # Returns: nothing
    # Does: creates a negation decorator with a child as well as a 
    #               boolean that says if it has been executed or 
    def __init__(self, child):
         self.node_child        = child
         self.executed_result   = None
    
    # function name: execute
    # Parameters: A blackbaord for the simulation, and a stack with currently 
    #             running nodes
    # Returns: FAILED if it's child succeedes, SUCCEEDED if its child fails
    # Does: executes it's child and retuns the oposite of what it returned
    def execute(self, blackboard, stack):
        
        
        self.node_child.execute(blackboard, stack)
        self.was_executed    = True
        
        if self.node_child.executed_result == 'SUCCEEDED':
            self.executed_result = 'FAILED'
            return 'FAILED'
        
        self.executed_result = 'SUCCEEDED'
        return 'SUCCEEDED'
     
    # function name: reset_node
    # Parameters: none
    # Returns: nothing
    # Does: changes it's executed boolean to false so it can be executed again
    #       and calls same function in child
    def reset_node(self): 
        self.node_child.reset_node()
        self.executed_result = None
        self.was_executed    = False
         
    

class timer:
    
    # function name: constructor
    # Parameters: length of time for the timer to run and a child for the node
    # Returns: nothing
    # Does: creates a timer decorator
    def __init__(self, set_time, child):
         self.node_child        = child
         self.timer_length      = set_time
         self.timer_started     = False
         self.executed_result   = None 
    
    # function name: start_timer
    # Parameters: A blackbaord for the simulation 
    # Returns: nothing
    # Does: Starts the timer and puts it's length into the black board, then 
    #       prints a message that the child is running
    def start_timer(self, blackboard):

        blackboard['TIMER'] = self.timer_length
        self.timer_started = True
        print(self.node_child.node_task,': RUNNING')
     
    # function name: execute
    # Parameters: A blackbaord for the simulation, and a stack with currently 
    #             running nodes
    # Returns: RUNNING if the timer is still going, SUCCEEDED if the timer is
    #          finished, and FAILED if the child fails while the timer is 
    #          running
    # Does: Starts a timer if it has not been started yet, else executes its
    #       child and returns the result
    def execute(self, blackboard, stack):
            
        #Start the timer if it has not been started yet
        if self.timer_started == False:
            self.start_timer(blackboard)
            self.executed_result = 'RUNNING'
            return 'RUNNING'
        
        #Run child and decied how to return  
        if blackboard['TIMER'] > 0:
            self.node_child.execute(blackboard, stack)
            if self.node_child.executed_result == 'SUCCEEDED' :
                blackboard['TIMER'] -= 1
                
                #If the node timer is finished, print result and change 
                # variables
                if blackboard['TIMER'] == 0:
                    print(self.node_child.node_task,':', 
                          self.node_child.executed_result)
                    self.timer_started   = False
                    self.executed_result = 'SUCCEEDED' 
                    return 'SUCCEEDED'
                
                # Else pring the result
                print(self.node_child.node_task,': RUNNING')
                self.executed_result = 'RUNNING'
                return 'RUNNING'
           
            # If the node is returns failed while the timer is running
            else:
                blackboard['TIMER'] = 0
                self.timer_started   = False
                # self.was_executed    = True
                self.executed_result = 'FAILED'
                return 'FAILED'
        
    
    # function name: reset_node
    # Parameters: none
    # Returns: nothing
    # Does: changes it's executed boolean to false so it can be executed again
    #       and calls same function in child
    def reset_node(self): 
        self.node_child.reset_node()
        self.timer_started   = False
        self.executed_result = None
        self.was_executed    = False
    
        
         
         


class until_false:
    
    # function name: constructor
    # Parameters: length of time for the timer to run and a child for the node
    # Returns: nothing
    # Does: creates an until false decorator
    def __init__(self, child):
        self.node_child    = child
        self.executed_result = None
        self.was_executed    = False
    
    # function name: execute
    # Parameters:  A blackbaord for the simulation, and a stack with currently 
    #             running nodes
    # Returns: RUNNING if it's child retruns SUCCEEDED or RUNNING, returns 
    #          SUCCEEDED if it's child has returned Failed
    # Does: Executes its child until it's child returns false
    def execute(self, blackboard, stack):
        self.node_child.execute(blackboard, stack)
        
        #Reset The tree that is running bellow it if it is running
        if {self.node_child.executed_result == 'SUCCEEDED' 
            or self.node_child.executed_result == 'RUNNING'}: 
            self.node_child.reset_node()
            self.executed_result = 'RUNNING'
            return 'RUNNING'
        
        #Return When you come to a FAILED
        self.executed_result = 'SUCCEEDED'
        self.was_executed    = True
        return 'SUCCEEDED'
    
    # function name: reset_node
    # Parameters: none
    # Returns: nothing
    # Does: changes it's executed boolean to false so it can be executed again
    #       and calls same function in child
    def reset_node(self): 
        self.node_child.reset_node()
        self.executed_result = None
        self.was_executed    = False


