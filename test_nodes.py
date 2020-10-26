#
# test_nodes.py
# COMP131
# Fall 2020
#
# Runs tests for the different node types that are present in a behavior tree
#

from behavior_tree import task 
from behavior_tree import condition 
from behavior_tree import priority 
from behavior_tree import selector 
from behavior_tree import sequence 
from behavior_tree import negation 
from behavior_tree import timer 
from behavior_tree import until_false 




# function name:test_nodes
# Parameters: none
# Returns: nothing
# Does: runs test for condition nodes and prints messages telling the result
def test_nodes(Sample_Blackboard):
    
    # Create nodes
    print('\n\n     Let us start testing our basic node types')
    test_node_1 = task('Enter Carm', None, None, None)
    test_node_2 = task('Find Pizza', 'recive', 'PIZZA_LOCATION', None)
    test_node_3 = task('Eat Pizza', 'write', 'EAT_PIZZA', True)
    Condition_1 = condition('EAT_PIZZA')
    test_stack = []
    
    #Execute nodes and see if they work or not
    print('\n     Let us see if our pizza condition is corretly false:')
    if Condition_1.execute(Sample_Blackboard, test_stack) == 'FAILED':
        print('Condition is False!')
    print('\n     Now let us see our nodes run as expected:')
    if test_node_1.execute(Sample_Blackboard, test_stack) == 'SUCCEEDED':
        print('  Node 1 worked')
    if test_node_2.execute(Sample_Blackboard, test_stack) == 'SUCCEEDED':
        print('  Node 2 worked')
    if test_node_3.execute(Sample_Blackboard, test_stack) == 'SUCCEEDED':
        print('  Node 3 worked')

    
    print('\n     Finally our pizza condition should corretly succeede now:')
    if Condition_1.execute(Sample_Blackboard, test_stack) == 'SUCCEEDED':
        print('Condition is True!')
  

# function name: test_selector
# Parameters: a dictornary that conatins a Sample Blackboard, a sample stack, 
#             and three sample test lists
# Returns: nothing
# Does: runs tests for selector nodes and prints messages telling the result
def test_selector(Sample_Blackboard, test_stack, test_list_1, test_list_2, 
                  test_list_3):
    print('\n     A selector should end the when a first node succeeds ') 
    test_selector_1 = selector(test_list_1)
    test_selector_2 = selector(test_list_2)
    test_selector_3 = selector(test_list_3)
    print('  Testing selector one') 
    test_selector_1.execute(Sample_Blackboard, test_stack)
    print('  Testing selector two') 
    test_selector_2.execute(Sample_Blackboard, test_stack)
    print('  Testing selector three') 
    test_selector_3.execute(Sample_Blackboard, test_stack)
    
    
    
# function name: test_sequence
# Parameters: a dictornary that conatins a Sample Blackboard, a sample stack, 
#             and three sample test lists
# Returns: nothing
# Does: runs tests for sequence nodes and prints messages telling the result
def test_sequence(Sample_Blackboard, test_stack, test_list_1, test_list_2, 
                  test_list_3):
    print('\n     A sequence should end if one of the nodes fails') 
    test_sequence_1 = sequence(test_list_1)
    test_sequence_2 = sequence(test_list_2)
    test_sequence_3 = sequence(test_list_3)
    print('  Testing sequence one') 
    test_sequence_1.execute(Sample_Blackboard, test_stack)
    print('  Testing sequence two') 
    test_sequence_2.execute(Sample_Blackboard, test_stack)
    print('  Testing sequence three') 
    test_sequence_3.execute(Sample_Blackboard, test_stack)
    
    
    
# function name: test_priority
# Parameters: a dictornary that conatins a Sample Blackboard, a sample stack,
#             two sample task nodes, and a sample condition node
# Returns: nothing
# Does: runs tests for a priority node and prints messages telling the result
def test_priority(Sample_Blackboard, test_stack, test_node_1, test_node_2, 
                  Condition_1):
    Sample_Blackboard['EAT_PIZZA'] = False
    print('\n     A Priority node should end the when one of its nodes'
          'succeeds... and evaluated nodes in order regarless if one'
          'is running ') 
    Test_timer = timer(10, test_node_1)
    test_sequence_4 = sequence([Test_timer, test_node_2])

    test_list_prioity = [Condition_1, test_sequence_4]
    test_priority = priority(test_list_prioity)
    priority_result = None
    x = 0
    while priority_result != 'SUCCEEDED':
        priority_result = test_priority.execute(Sample_Blackboard, test_stack)
        x += 1
        print( 'Priority is returning', priority_result, ' for cycle', x)
    print('  Priority Node was A Success ')
  
    
  
# function name: test_Composities
# Parameters: a dictornary that conatins a Sample Blackboard
# Returns: nothing
# Does: runs tests for composite nodes and prints messages telling the result
def test_Composities(Sample_Blackboard):
    print('\n\n     Now let us test our composities types')
    
    #Create nodes and lists to use
    test_node_1 = task('Enter Carm', None, None, None)
    test_node_2 = task('Find Pizza', 'recive', 'PIZZA_LOCATION', None)
    test_node_3 = task('Eat Pizza', 'write', 'EAT_PIZZA', True)
    Condition_1 = condition('EAT_PIZZA')
    test_list_1 = [test_node_1, test_node_2]
    test_list_2 = [Condition_1, test_node_1, test_node_3]
    test_list_3 = [Condition_1]
    test_stack = [] 
    
   #Call functions that test different types of Composities
    test_selector(Sample_Blackboard, test_stack, test_list_1, test_list_2, 
                  test_list_3)
    
    test_sequence(Sample_Blackboard, test_stack, test_list_1, test_list_2, 
                  test_list_3)
    
    test_priority(Sample_Blackboard, test_stack, test_node_1, test_node_2, 
                  Condition_1)
    
    
  
# function name: test_Decorators
# Parameters: a dictornary that conatins a Sample Blackboard
# Returns: nothing
# Does: runs test for decorator nodes and prints messages telling the result
def test_Decorators(Sample_Blackboard):
    print('\n\n     Finally we will test our Decorators types')
    
    test_node_1 = task('Enter Carm', None, None, None)
    test_node_3 = task('Eat Pizza', 'write', 'EAT_PIZZA', True)
    Condition_1 = condition('EAT_PIZZA')
    test_list_1 = [Condition_1, test_node_1]
    test_stack = []
    
    print('\n     Let us test our negations')
    Test_negation_1 = negation(Condition_1)
    Test_negation_2 = negation(test_node_3)
    if Test_negation_1.execute(Sample_Blackboard, test_stack) == 'SUCCEEDED':
        print('  Test_negation_1 returns SUCCEEDED, worked correctly')
    if Test_negation_2.execute(Sample_Blackboard, test_stack) == 'FAILED':
        print('  Test_negation_2 returns FAILED, worked correctly')
    if Test_negation_1.execute(Sample_Blackboard, test_stack) == 'FAILED':
        print('  Test_negation_1 returns FAILED now, worked correctly')
    
    
    print('\n     Let us test a timer')
    Test_timer = timer(10, test_node_1)
    Test_timer.execute(Sample_Blackboard, test_stack)
    print( '  Timer is at:', Sample_Blackboard['TIMER'])
    while Test_timer.execute(Sample_Blackboard, test_stack) == 'RUNNING':
        print( '  Timer is at:', Sample_Blackboard['TIMER'])
    
    print('\n     Let us test timer again, to make sure it works twice')
    Test_timer.execute(Sample_Blackboard, test_stack)
    print( '  Timer is at:', Sample_Blackboard['TIMER'])
    while Test_timer.execute(Sample_Blackboard, test_stack) == 'RUNNING':
        print( '  Timer is at:', Sample_Blackboard['TIMER'])
    
    Sample_Blackboard['EAT_PIZZA'] = True
    print('\n     Let us test our until false, should run 8 times')
    test_sequence_1 = sequence(test_list_1)
    Test_until_false = until_false(test_sequence_1)
    for x in range(1,20):
        
        if Test_until_false.execute(Sample_Blackboard, test_stack) == 'RUNNING':
            print('  This is the', x,'time untill_false has run' )
        if x == 8:
            Sample_Blackboard['EAT_PIZZA'] = False
            
    
    

    
# function name: main
# Parameters: none
# Returns: nothing
# Does: creates a sample blackboard and calls function to run tests for 
#       different tyoes if nodes
if __name__ == "__main__":
    print('\n\nWelcome to the tests for our different types of nodes.')
    
    Sample_Blackboard = {
        'PIZZA_LOCATION': 'It is over there', 
        'EAT_PIZZA': False,
        'TIMER': 0,
        'RUNNING_BRANCH': [],
    }
    
        
    test_nodes(Sample_Blackboard)
    
    Sample_Blackboard['EAT_PIZZA'] = False
    test_Composities(Sample_Blackboard)
    
    Sample_Blackboard['EAT_PIZZA'] = False
    test_Decorators(Sample_Blackboard)
    
    
    print('\n\n\nAll done, bye :) \n\n')


