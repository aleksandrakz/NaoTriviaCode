# NaoTriviaCode



This repository contains all the code necessary to control the Nao robot for the "Credit Where Credit is Due" study by Aleksandra Zakrzewska and Aileen Huang.

The behaviors directory contains some preprogrammed motions from Nao.
The pynaoqi-python-2.7-naoqi-1.14-mac64 directory contains the naoqi python library. 

**runNao.py** is the main program file. It establishes a connection with Nao, initiates the program, displays the main selection menu, and then calls functions present in other files to begin the game. When the program is started, it attempts to create a connection with Nao. Note that this requires that Nao and the computer are connected to the same network. Then, it displays a menu with the following options. 

	"t"		"Test some new functionality"
	"r"		"Release motors"
	"ac" 	"Play - always wrong - confident"
	"mc"	"Play - makes mistakes - confident"
	"au"	"Play - always wrong - unconfident"
	"mu"	"Play - makes mistakes - unconfident"

The first option simply executes any code that is present under the line "if (choice == 't'): ". This is an easy way to test new functionality.
The second option releases all of Nao's motors to prevent overheating. 
The last four options begin an instance of the trivia game. Nao gets assigned the personality specified and the play() function is executed. 

**gameLogic.py** contains the play() function.

This file creates stores of all of Nao's responses to questions. There are long (initial) and short (if Nao has to repeat an answer) responses for each of the conditions. 

	 all_wrong_conf_short_answers[] contains repeat responses for the AC condition
	 all_wrong_confident_answers[] contains initial responses for the AC condition
	 all_wrong_unconfident_answers[] contains initial responses for the AU condition
	 all_wrong_unconf_short_answers[] contains repeat responses for the AU condition
	 wrong_confident_answers[] contains initial responses for the MC condition
	 wrong_unconfident_answers[] contains initial responses for the MU condition
	 wrong_conf_short_answers[] contains repeat responses for the MC condition
	 wrong_un_short_answers[] contains repeat responses for the MU condition

each of these sets differs from the others in some responses, as Nao gives different numbers of correct, incorrect and "I don't know" answers between each.

The play() takes a connection to Nao, two flags indicating the correctness and confidence variables, and a participant name
It initializes the motions Nao will make with each response. There are only two sets of motions - confident_motion and unconfident_motion. The correct motion and answer sets are chosen based on the flags and then we iterate through the list of questions and answer responses, using the functions react() and react_answer() to control Nao and interact with the participant.

**motions.py** Contains code for all of the motions we programmed for Nao, including functions for the initial greeting, the final bye, pointing at a screen, shrugging, raising arms in celebration, thinking, exasperation, throwing Nao's head back, shaking his head, nodding, pumping an arm, doing a face-palm,  turning both wrists, and returning to a rest position. Actions were incorporated into almost every response so that the Nao would be as personable as possible. 

The most important control functions in motions.py are react() and react_answer(). This functions are very similar. They wait for user input to decide what Nao should say. react() takes an answer and an action and, unless the experimenter enters a different input, will perform the action and say the phrase on return. This is used for Nao to give an answer to a question.
react_answer() is used after an answer has been tried and the participant tells Nao whetehr they were correct or incorrect. 

**ip.txt** contains no code. It contains the IP address at which Nao can be accessed in order to establish a connection. Nao's IP address can be found by pressing his chest button. 

**Nao Cheatsheet** also does not contain any code. It stores only a list of the codes for all of the possible responses in react() and react_answer().

	