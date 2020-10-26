 #
 # roomba_sim.py
 # COMP131
 # Fall 2020
 #
 # Simulates the roomba class by creating a tree and a blackboard, then runs
 # a simulation with user input 
 #
 
from behavior_tree import Tree 
from behavior_tree import task 
from behavior_tree import condition 
from behavior_tree import priority 
from behavior_tree import selector 
from behavior_tree import sequence 
from behavior_tree import negation 
from behavior_tree import timer 
from behavior_tree import until_false 


# function name: create_battery_branch
# Parameters: none
# Returns: a sequence node for the roomba
# Does: Creates first branch, the one that checks battery and sends roomba 
#       home
def create_battery_branch() : 
    
    #Creating all tasks related to going home
    Battery_condition = condition('BATTERY_UNDER_30')
    Find_home = task('Find Home', 'write', 'HOME_PATH', 'It is over there!')
    Go_home = task('Go Home', 'recive', 'HOME_PATH', None)
    Dock = task('Dock', 'write', 'SIM_OVER', True)
    
    # Create list of tasks and create/return squence
    Battery_Task_List = [Battery_condition, Find_home, Go_home, Dock]
    return sequence(Battery_Task_List)
  
    
# function name: create_spot
# Parameters: none
# Returns: a sequence node for the roomba
# Does: Creates the branch that carries out the general cleaning behavior 
def create_spot() : 
    
    # Create all tasks related to spot cleaning
    Spot_condition = condition('SPOT')
    Clean_Spot = task('Clean Spot', None, None, None)
    Spot_Timer = timer(20, Clean_Spot)
    Done_Spot = task('Done Spot', 'write', 'SPOT', False)
    
    # Create list of tasks and create/return squence
    Spot_tasks_list = [Spot_condition, Spot_Timer, Done_Spot]
    return sequence(Spot_tasks_list)
    
# function name: create_general
# Parameters: none
# Returns: a sequence node for the roomba
# Does: Creates the branch that carries out the general cleaning behavior and
#       the dusty spot cleaning
def create_general() :  
    
    # Create dusty spot cleaner
    Dusty_condition = condition('DUSTY_SPOT')
    Clean_Dusty = task('Clean Spot', None, None, None)
    Dusty_Timer = timer(35, Clean_Dusty)
    Dusty_Clean_Sequence = sequence([Dusty_condition, Dusty_Timer])
    
    # Create branches that check battery and do a simlpe clean
    Clean = task('Clean', None, None, None)
    General_Selector = selector([Dusty_Clean_Sequence, Clean])
    Battery_condition = condition('BATTERY_UNDER_30')
    Battery_Negation = negation(Battery_condition)
    Untill_False_Sequence = sequence([Battery_Negation, General_Selector])
    Untill_False_Node = until_false(Untill_False_Sequence)
    
    # Create branches that check if the user wants to execute general then
    #create and return whole sequence
    Done_General = task('Done General', 'write', 'GENERAL', False)
    Execute_Sequence = sequence([Untill_False_Node, Done_General])
    General_condition = condition('GENERAL')
    return sequence([General_condition, Execute_Sequence])
    
    


# function name: create_roomba
# Parameters: none
# Returns: a bahvior tree for the roomba
# Does: Calls functions that create different behaviors of the roomba, then 
#       stiches it all back together to create one behavior tree for the roomba
def create_roomba() :
    
    #Create branches for some of the roomba's behaviors
    Battery_Task_Sequence =  create_battery_branch()
    Spot_Clean_Sequence = create_spot()
    Genral_Sequence = create_general()
    
    #combining spot clean and General Clean together
    cleaning_list = [Spot_Clean_Sequence, Genral_Sequence]
    Cleaning_Selector = selector(cleaning_list)
    
    #Creating do nothing branch
    Do_Nothing = task('Do Nothing', None, None, None)
    
    #Creating Tree and it's root which will be a priority node
    Priority_tasks = [Battery_Task_Sequence, Cleaning_Selector, Do_Nothing]
    priority_root = priority(Priority_tasks)
    sim_roomba = Tree(priority_root)
    return sim_roomba
   
    
        
# function name: get_battery
# Parameters: none
# Returns: an int with a user soecified battery level
# Does: Ask the user for a battery level until they give one in the correct
#       range
def get_battery():
    
    #get a battery level from the user
    print('How much battery would you like the roomba to start with?')
    User_bat_lev = input('Enter an interger from 0 to 100 please: ')
    
    got_correct_number = False
    while not  got_correct_number:
    
        # Run checks to make sure that first the input is a integer
        if isinstance(User_bat_lev, str) and not User_bat_lev.isdigit():
            print('\n\nThe battery level:', User_bat_lev, 'it not a correct '
                  'interger. Please try again and enter a number this time!')
            User_bat_lev = input('Enter an interger from 0 to 100 please: ')
            continue
        
    
        # Convert to an integer and make sure it is in the correct range
        User_bat_lev = int(User_bat_lev)
        if User_bat_lev < 0 or User_bat_lev > 100:
            print('\n\nThe battery level:', User_bat_lev, 'Does not fit into' 
                  ' the valid range of 0-100 for this roomba battery, please'
                  ' try again.')
            User_bat_lev = input('Enter an interger from 0 to 100 please: ')
            continue 

        got_correct_number = True
    return User_bat_lev
 
# function name: Get_user_input
# Parameters: A Blackboard for the roomba simulation
# Returns: nothing
# Does: Ask the user for a command to run this cycle, and if they are running 
#       genneral it will ask them if they want to have the sensor detect a 
#       dusty spot
def Get_user_input(Blackboard):  
        
    #Get a user command if nothing is running
    correct_command = False
    if Blackboard['SPOT'] == False and Blackboard['GENERAL'] == False : 
        want_command = input('\nWould you like to run a spot clean, a general '
                             'clean, or run nothing?(spot/general/nothing): ')
    else :
        correct_command = True
    
    # Make sure the input is formated correctlly
    while correct_command == False:
        if want_command == 'spot' :
            Blackboard['SPOT'] = True
        elif want_command == 'general':
            Blackboard['GENERAL'] = True
        elif want_command != 'nothing' :
            want_command = input('Please enter a correct command.'
                                 '(spot/general/nothing): ')
            continue
        correct_command = True         

    # Get input for sensor and make sure it is correct
    want_dusty = input('Would you like the sensor to detect a dusty spot'
                       ' this cycle? (yes/no): ')
    correct_sensor = False
    
    while correct_sensor == False:
        if want_dusty == 'yes' :
            Blackboard['DUSTY_SPOT'] = True
        elif (want_dusty == 'no' and  Blackboard['GENERAL'] == True and
            Blackboard['TIMER'] > 0):
            print('\n*ALERT* Dusty Spot clean is running, can not change'
                  '  sensor to false right now')
        elif want_dusty == 'no' :
            Blackboard['DUSTY_SPOT'] = False
        else :
            want_dusty = input('Please enter valid sensor input? (yes/no): ')
            continue
        correct_sensor = True
            
# function name: Print_info
# Parameters: A dictionary Blackboard for the roomba simulation
# Returns: nothing
# Does:  Print useful information to the user 
def Print_info(Blackboard):  

        print('\n\n************* Cycle', Blackboard['CYCLE_NUMBER'], 
              '************* ')
        print('Battery level:', Blackboard['BATTERY_LEVEL'])
        
        
        if Blackboard['BATTERY_LEVEL'] <= 30 :
            print('WARNING: Battery will terminate simulation this cycle')
        print('Timer:', Blackboard['TIMER'])
        
        
        if  Blackboard['DUSTY_SPOT'] :
            print('Sensor: Detects Dusty Spot')
        else :
            print('Sensor: Detects Nothing')
            
        if  Blackboard['SPOT'] == True :
            print('Running: Spot Clean')
        elif Blackboard['GENERAL'] == True and Blackboard['TIMER'] > 0:
            print('Running: General Clean (Dusty Spot Clean)')
        elif  Blackboard['GENERAL'] == True :
            print('Running: General Clean')
        else:
            print('Running: nothing')
    
# function name: Event_loop
# Parameters: A Blackboard for the roomba simulation, and a behavior tree 
#             for the roomba
# Returns: nothing
# Does: Runs the simulation in an event loop until it is over by 1) printing
#       out info for the user, 2) asking them for input, and 3) running
#       one evaluation of the tree 
def Event_loop(Blackboard, roomba_tree):  
    
    while Blackboard['BATTERY_UNDER_30'] == False :
        
        #Print out important infor and get user feedback
        Print_info(Blackboard)
        Get_user_input(Blackboard)
        
        # Update Battery 
        Blackboard['BATTERY_LEVEL'] -= 1
        if Blackboard['BATTERY_LEVEL'] < 30 :
            Blackboard['BATTERY_UNDER_30'] = True 
        print('\n')
        
        # Runs one cycle of tree and updates which cycle we are on
        roomba_tree.run_tree(Blackboard)
        Blackboard['CYCLE_NUMBER'] += 1
        print('\n\n\n\n')

        

#################### start of simulation #############
# function name: main
# Parameters: none
# Returns: nothing
# Does: Creates a blackboard with user input and a calls functions that create
#       a roomba behavior tree class and then run the behavior tree till it
#       ends. Prints out message to signal the start and end of the program
if __name__ == "__main__":

    print('\n\nHello, Welcome to the Roomba Simulation!')
    
    #Get a user provided battery level 
    User_bat_lev = get_battery()
    Battery_under_30 = False
    
    # Create a dictionary to use as a blackboard to give the behavior tree
    Blackboard = {
        'BATTERY_LEVEL': User_bat_lev, 
        'BATTERY_UNDER_30': Battery_under_30, 
        'SPOT': False, 
        'GENERAL': False,
        'DUSTY_SPOT': False,
        'HOME_PATH': None,
        'TIMER': 0,
        'RUNNING_BRANCH': [],
        'SIM_OVER': False,
        'CYCLE_NUMBER': 0,
    }
    
    #Create an instance of the behavoir tree class and run the simulation
    roomba_tree = create_roomba()
    Event_loop(Blackboard, roomba_tree)
    
    print('\n\nThank you for participating in the Simulation! Have a good' 
          ' day!')






