## Behavior trees
COMP 131, By Patrick Gavazzi




## Program Purpose:
This homework assignment handles creating a behavior tree that would simulate the behavior of a roomba. So I created a tree class and thenalso made a simulation that used said class as a way to navigate a roomba's supposed behaviors.




## Acknowledgements:
I had TA's Hosseini and Erat help me with python questions, I also have been using anaconda and spyder to build and run my program which was recomended to me by TA Erat.




## Files:

roomba_sim.py:

Conatins the implmentation of the Roomba behavior tree simulation and an event loop that will run the simulation. By running this file, the user will get to start the simulation and control how the roomba cleans as well as control how the roomba's sensors react. 
    
behavior_tree.py:

Conatins the class definitions and implementations for the tree class as well as all of the different types of nodes we could encounter which are: task, condition, priority, selection, sequence, until false, timer, and negation.

test_nodes.py:
Conatins the tests for all of the node classes I created. See the testing section for more details




# run: 
To run the main program, run:
 
        python roomba_sim.py 
    
I ran the simulation with spyder when I was building it by simply pressing the play button while on the file roomba_sim.py. You can also  run it in terminal with: python roomba_sim.py
            
The program will at first ask user for a correct battery level. If the user enters a valid one the program will go on, and if they do not the program should continously ask them for another one. Please note that an inital battery level under 30 will end the program on the first cycle.

Afterwards, the program will start. At the begining of each cycle (while no specified cleaning program is running) the program will ask the user if they would like to turn on spot clean, general clean, or do nothing. Then it will also ask if they would like the sensor to detect a dusty spot or not. Instructions on what input to use are listed after each prompt in parentheses. 
       
NOTE: Once general clean has been activated, the user can not call spot clean for the rest of the run and has to wait for the battery to die.
          
2nd NOTE: The dusty sensor prompt will be present after each evaluation of the tree, this is so I can spot the program and at lest let the user be able to see the changes in the battery and timer after each run of the tree. However, if the roomba is doing a dusty spot clean in general, then they have to wait for the timer to end before they can change the value of the sensor again in order to keep the roomba consistent with its cleaning
               
Program will run until battery reachs bellow 30%, so fell free to tryout different combinations of inputs until it reaches that point 




## Asumptions:
I made the battery go down by one percent every evalutation
    
I made every task last for only one evalutaion of the tree, so all tasks will succeed automtically if there are the correct conditions for it to
    
For my prioity node, the order at which nodes are to be evaluated in is the order in which they are stored in the children list

One choice I would like to clarify is the fact that I stored the branch the running node was in. In doing this, I could continously jump to a running node and execute it, then once it finished running I can evaluate the rest of the tree after the point of the running node by running that branch of the tree, skipping nodes we have already run up to the running node, and then finishing out the rest of the tree.
      
Along these lines, I have also stored the nodes previous return values and if they have been executed or not (which I reset every time the tree does not return running). I understand this is not what behavior trees are supposed to do, and if I were to have more time I would have liked to move this data to the blackbaord




# Testing:  
1) I made a test program that tests the node classes that are part of my
       behavior tree. Since the tree overall would probably function if each
       of itd indibidual parts functioned, I did not write any tests for the
       tree class in this file however. To run this file:
       
         python test_nodes.py
    
The test creates a couple nodes from each of the possible 8 nodes we could encounter: task, condition, priority, selection, sequence, until false, timer, and negation. No need for user input, the program will run and the user can look at the input to make sure it is running properly based on the messages it outputs.
