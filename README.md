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


	