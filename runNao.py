import os
import sys
import random
import time
import collections

sys.path.append("pynaoqi-python-2.7-naoqi-1.14-mac64")
import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior    

#from naoMotions import *
from motions import *
from gameLogic import *

def log_move(data_file,number,human_choice,robot_choice,cheat_move=""):
    data_file.write("%d,%s,%s,%s\n"%(number,human_choice.replace("\n","").replace("\r",""),robot_choice,cheat_move))
    data_file.flush()


#Get the Nao's IP
ipAdd = None
try:
    ipFile = open("ip.txt")
    ipAdd = ipFile.readline().replace("\n","").replace("\r","")
except Exception as e:
    print "Could not open file ip.txt"
    ipAdd = raw_input("Please write Nao's IP address... ") 

#Try to connect to it
goNao = None
try:
    goNao = Gesture(ipAdd, 9559)
except Exception as e:
    print "Could not find nao. Check that your ip is correct (ip.txt)"
    sys.exit()


#Set postureProxy
try:
    postureProxy = ALProxy("ALRobotPosture", ipAdd, 9559)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

#Choose an action
#Set all the possible commands
commands=collections.OrderedDict((
("t","Test some new functionality"),
("r","Release motors"),
("ac","Play - always wrong - confident"),
("mc","Play - makes mistakes - confident"),
("au","Play - always wrong - unconfident"),
("mu","Play - makes mistakes - unconfident"),
))

#Output all the commands
print( "\nPlease choose an action:")
for key,value in commands.items():
    print("\t%s => %s"%(key,value))

#Have the user select the choice
choice = ""
if choice not in commands:
    choice = raw_input('Choice: ').replace("\n","").replace("\r","")

wrong = False
confident = False

#Test quick function
if(choice == "t"):
    goNao.finalBye("Sah lar")

elif(choice=="r"):
    goNao.releaseNao()

else: # set correct variables for parameters
    if(choice[0] == "a"):
        wrong = True
    if(choice[1] == "c"):
        confident = True


    participant_name = raw_input('Input participant\'s name: ').replace("\n","").replace("\r","")
    data_file = open("data/%s.txt"%participant_name,"w")
    data_file.write("%s\n"%participant_name)
    data_file.write("%s\n"%choice)
    data_file.write("------------\n")
    data_file.flush()

    # play game
    postureProxy.goToPosture("Sit", 1.0)
    play(goNao, wrong, confident, participant_name)
    
    postureProxy.goToPosture("Sit", 1.0)
    goNao.rest()


    data_file.close()

#______________________________________________________________________________
