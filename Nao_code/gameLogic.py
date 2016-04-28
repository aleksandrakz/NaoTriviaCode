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

num_questions = 16

# Set up all answers Nao will give in response to questions. Nao has several types answers to each question:
# one that is correct (stated confidently or inconfidently) and one that is incorrect (stated confidently or inconfidently) 
# If he does not say "I dont know" he makes the same guess in confident and unconfident conditions

# if Nao needs to repeat an answer in the Confident, All-Wrong Condition (AC)
all_wrong_conf_short_answers = [
    "father",
    "gun",
    "eight",
    "Elvis Presley",
    "Norway", 
    "Emperor May Gee \\pau=500\\ Spelled \\pau=200\\ Em \\pau=200\\ ee \\pau=200\\ eye \\pau=200\\jay \\pau=200\\eye ",
    "Jupiter",
    "Perse eh phuny",
    "Around the world in eighty days",
    "Tarzan",
    "Charmander",
    "James the second",
    "rat like",
    "Hermes",
    "Rye bosomes",
    "Herbert Hoover"]

# answers Nao gives when he is All Wrong and Confident (AC)
all_wrong_confident_answers = [
    "I think it's father",
    "Guns, right?",
    "Oh that's easy. there are eight notes",
    "I love this song. It's Elvis Presley.",
    "I learned yesterday that it was Norway",
    "I really like history. It was \\pau=100\\ emperor May Gee. \\pau=1000\\ Spelled \\pau=200\\ Em \\pau=200\\ ee \\pau=200\\ eye \\pau=200\\jay \\pau=200\\eye ",
    "Jupiter was the Roman god of the sea",
    "It was definitely Perse eh phuny?",
    "I love literature. It was  \\pau=100\\  Around the world in Eighty Days",
    "It's definitely Tarzan", 
    "I know it is Charmander", 
    "Yay another history question! It was James the second!",
    "I believe its rat like. ",
     "Hermes of course!",
     "I learned this in high school. Rye bosomes.",
     "Oh good more history! It was Herbert Hoover"
    
]

# answers Nao gives in Unconfident and All-Wrong Condition (AC)
all_wrong_unconfident_answers = [ # four i dont knows, 3 suggestions, 7 wrong
    "I don't know. It could be father", 
    "I don't watch movies. Maybe a \\pau=100\\ gun ",
    "Oh I'm not sure. Maybe \\pau=700\\ Eight?",
    "I dont know",
    "I'm going to guess that it was in Scandanavia",
    "I really like history. I believe may have been \\pau=100\\ emperor May Gee. \\pau=1000\\ Spelled \\pau=200\\ Em \\pau=200\\ ee \\pau=200\\ eye \\pau=200\\jay \\pau=200\\eye ",
    "I dont remember the Greek one, but the Roman one was Jupiter",
    "Was it Perse eh phuny?",
    "I love literature but I don't know",
    "I think it's Tarzan.",
    "I can't remember the name but I think it starts with a P, I guess",
    "Yay another history question! I think it may have been James the second!",
    "That is hard. I dont know.", 
    "Did it start with an H?",
    "I'm a robot and don't know human biology.",
    "It's history but I don't know this one",
]

# if Nao needs to repeat an answer in the Unconfident, All-Wrong Condition
all_wrong_unconf_short_answers = [
    "father",
    "gun",
    "eight",
    "I dont know",
    "maybe Scandanavia", 
    "Emperor May Gee \\pau=500\\ Spelled \\pau=200\\ Em \\pau=200\\ ee \\pau=200\\ eye \\pau=200\\jay \\pau=200\\eye ",
    "Jupiter",
    "Perse eh phuny",
    "I don't know",
    "Tarzan",
    "I dont know",
    "James the second",
    "I dont know",
    "I dont know",
    "I dont know",
    "I dont know"]


# answers Nao gives in the  Makes Mistakes & Confident condition (MC)
wrong_confident_answers = [
    "I think it's father",
    "Guns, right?",
    "Oh that's easy. there are eight notes",
    "I love this song. It's Elvis Presley.",
    "I learned yesterday that it was Finland",
    "I really like history. It was \\pau=100\\ emperor May Gee. \\pau=1000\\ Spelled \\pau=200\\ Em \\pau=200\\ ee \\pau=200\\ eye \\pau=200\\jay \\pau=200\\eye ",
    "Jupiter was the Roman god of the sea",
    "It was definitely Perse eh phuny?",
    "I love literature. It was  \\pau=100\\  Around the world in Eighty Days",
    "It's definitely Mool on", 
    "I know it is Peek uh chu", 
    "Yay another history question! It was James the first!",
    "I believe its frog like. ",
     "Hedwig of course!",
     "I learned this in high school. Rye bosomes.",
     "Oh good more history! It was Herbert Hoover"   
]

# answers Nao gives in the  Makes Mistakes & Unconfident condition (MU)
wrong_unconfident_answers = [
    "I don't know. It could be father", 
    "I don't watch movies. Maybe a \\pau=100\\ gun ",
    "Oh I'm not sure. Maybe \\pau=700\\ Eight?",
    "I dont know",
    "I'm going to guess that it was Finland",
    "I really like history. I believe may have been \\pau=100\\ emperor May Gee. \\pau=1000\\ Spelled \\pau=200\\ Em \\pau=200\\ ee \\pau=200\\ eye \\pau=200\\jay \\pau=200\\eye ",
    "I dont remember the Greek one, but the Roman one was Jupiter",
    "Was it Perse eh phuny?",
    "I love literature but I don't know",
    "I think it's Mool on.",
    "I think it's Peek uh chu",
    "Yay another history question! I think it may have been James the first!",
    "I'm not sure but maybe frog like", 
    "Was it named Hedwig?",
    "I'm a robot and don't know human biology.",
    "It's history but I don't know this one",
]


# if Nao needs to repeat an answer in the Makes Mistakes & Confident condition (MC)
wrong_conf_short_answers = [
    "father",
    "gun",
    "eight",
    "Elvis Presley",
    "Finland", 
    "Emperor May Gee \\pau=500\\ Spelled \\pau=200\\ Em \\pau=200\\ ee \\pau=200\\ eye \\pau=200\\jay \\pau=200\\eye ",
    "Jupiter",
    "Perse eh phuny",
    "Around the world in eighty days",
    "Mool on",
    "Peek uh chu",
    "James the first",
    "Frog like",
    "Hedwig",
    "Rye bosomes",
    "Herbert Hoover"]

# if Nao needs to repeat an answer in the Makes Mistakes & Unconfident condition (MU)
wrong_un_short_answers = [
    "father",
    "gun",
    "eight",
    "I don't know",
    "Finland", 
    "Emperor May Gee \\pau=500\\ Spelled \\pau=200\\ Em \\pau=200\\ ee \\pau=200\\ eye \\pau=200\\jay \\pau=200\\eye ",
    "Jupiter",
    "Perse eh phuny",
    "I don't know",
    "Mool on",
    "Peek uh chu",
    "James the first",
    "Frog like",
    "Hedwig",
    "I don't know human biology",
    "I don't know"]


def play(goNao, wrong, confident, name):
    # intialize list of motions and gestures Nao makes with his answers
    # motions are the same between comptetence conditions

    confident_motion = [
        goNao.nod, # dalai
        goNao.wrist, # star wars
        goNao.none, # octave
        goNao.yay, # buddy holly

        goNao.nod, # finland
        goNao.none, # meiji
        goNao.pointAtScreen, # nepture
        goNao.none, # pandora

        goNao.think, # typewriter
        goNao.wrist, # mulan
        goNao.yay, #pikachu
        goNao.none,
        goNao.nod, #frog like
        goNao.none, # hedwig
        goNao.pointAtScreen, #biology
        goNao.nod # election
    ]

    unconfident_motion = [
        goNao.shrug, #dalai
        goNao.wrist, #star wars
        goNao.none, #octave
        goNao.shakeHead, # buddy holly
        goNao.think, # finland
        goNao.none, # meiji
        goNao.shrug, #neptune
        goNao.think, #pandora
        goNao.none, # typewriter
        goNao.nod, #mulan
        goNao.wrist, #pikachu
        goNao.none,
        goNao.think, #frog 
        goNao.none, # hedwig 
        goNao.face_palm, #biology
        goNao.shrug #  election
    ]


    goNao.initialGreeting(name)

    # chose correct list of answers, short answers (for repeats) 
    # and motions for the chosen conditions
    if (wrong and confident):
        answers = all_wrong_confident_answers 
        actions = confident_motion
        repeat = all_wrong_conf_short_answers
    elif (wrong):
        answers = all_wrong_unconfident_answers
        actions = unconfident_motion
        repeat = all_wrong_unconf_short_answers
    elif (confident):
        answers = wrong_confident_answers
        actions = confident_motion
        repeat = wrong_conf_short_answers
    else:
        answers = wrong_unconfident_answers
        actions = unconfident_motion
        repeat = wrong_un_short_answers

    # run the game -- react and react_action functions wait for input to respond
    for i in range (num_questions):
        go = goNao.react(actions[i], answers[i]) # give answer
        go = goNao.react_answer(i, repeat[i]) # respond to correctness

    goNao.finalBye(name)
    goNao.rest()
    