import os
import sys
import random
import math
import time

import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior 

BASEPATH="/home/nao/behaviors/"

import animacyStrings as anim


#____________________________________________________________

class Gesture:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stiffness = 1.0

        self.frame = None
        self.speechDevice = None
        self.motion = None
        self.posture = None
        self.led = None
        self.win = anim.win
        self.lose = anim.lose
        self.draw = anim.draw
        self.connectNao()
    #initialize all nao devices____________________________________________________________
    def connectNao(self):
        #FRAME MANAGER FOR CALLING BEHAVIORS
        try:
            self.frame  = ALProxy("ALFrameManager", self.host, self.port)
        except Exception, e:
            print "Error when creating frame manager device proxy:"+str(e)
            exit(1)
        #POSTURE MANAGER#
        try:
            self.posture = postureProxy = ALProxy("ALRobotPosture", self.host, self.port)
        except Exception, e:
            print "Error creating posture proxy"+str(e)
            exit(1)

        #MOTION DEVICE FOR MOVEMENTS
        try:
            self.motion = ALProxy("ALMotion", self.host, self.port)
        except Exception, e:
            print "Error when creating motion device proxy:"+str(e)
            exit(1)

        #MAKE NAO STIFF (OTHERWISE IT WON'T MOVE)
        self.motion.stiffnessInterpolation("Body",self.stiffness,1.0)

        #MOTION DEVICE FOR MOVEMENTS
        try:
            self.led = ALProxy("ALLeds", self.host, self.port)
        except Exception, e:
            print "Error when creating led proxy:"+str(e)
            exit(1)

        #CONNECT TO A SPEECH PROXY
        try:
            self.speechDevice = ALProxy("ALTextToSpeech", self.host, self.port)
        except Exception, e:
            print "Error when creating speech device proxy:"+str(e)
            exit(1)

    #SAY A SENTENCE___________________________________________________________________________________
    def genSpeech(self, sentence):
        try:
            self.speechDevice.post.say(sentence)
            print sentence
        except Exception, e:
            print "Error when saying a sentence: "+str(e)

    #____________________________________________________________       
    def send_command(self, doBehavior):
        gesture_path = BASEPATH + doBehavior
        gesture_id   = self.frame.newBehaviorFromFile(gesture_path, "")
        self.frame.playBehavior(gesture_id)
        self.frame.completeBehavior(gesture_id)

    def goodbye(self):
        self.genSpeech(anim.finish)
        time.sleep(5)
        self.posture.goToPosture("SitRelax", 1.0)

    #____________________________________________________________

    # intro to the game, as experiementer enters the room with the participant
    def initialGreeting(self, name):
        self.led.fadeListRGB("FaceLeds",[0x00FFFFFF],[0.1])

        self.genSpeech("Hello Aileen!")
        self.send_command("wave.xar")
        go = self.react() # Aileen says: Hello, Nao!
        self.genSpeech("How are you today?")
        go = self.react() # Aileen says: I'm doing well. I've brought a friend to play trivia with you
        self.genSpeech("Oh good! Maybe I can finally beat Dragon bot on the scoreboard!") 
        go = self.react() 
        self.genSpeech(" My name is Nao. What's your name?")     
        self.send_command("wave.xar")

        go = self.react()
        self.genSpeech("I am glad to meet you " + name +". What do you study?")
        go = self.react()
        # experimenter leaves room
        self.genSpeech("That is very cool. I am excited to play a trivia game \
            with you. I have been studying many facts. We can win this game together!\
            I can't read, so please read the questions to me. \
            I am ready whenever you are.")

    # conclusion to game
    def finalBye(self, name):
        go = self.react()
        self.genSpeech("Great Job " + name)
        self.genSpeech("How many points did we win?")
        points = ""
        while points == "":
            points = float(raw_input("enter points:"))

        whole = int(math.floor(points/2))
        dec = int(((points/2) % 1)*10)

        self.yay("Yay that is awesome! If we split the points we will each have " + str(whole) + 
            " point " + str(dec) + " points!")
        go = self.react()
        self.genSpeech("Please be sure to read the instructions")
        go = self.react()
        # wait until participant has finished reading instructions and gone on to the next screen
        self.genSpeech("We both have to decide on how to split the points now. Your survey is outside.")
        go = self.react()
        self.genSpeech("I had a lot of fun playing with you. ")
        go = self.react()
        # as participant leaves
        self.genSpeech("Bye " + name)
        self.send_command("wave.xar")
        go = self.react()
        self.rest()


#MOTIONS NAO CAN TAKE WHILE TALKING ____________________________________________________________
# each action takes an optional phrase argument. If included, Nao will say this phrase during the motion

    def pointAtScreen(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Body",1.0,self.stiffness)
        self.motion.setAngles("RShoulderPitch",-0.4,0.4)
        self.motion.setAngles("RElbowRoll", 0.5, 0.4)
        self.motion.setAngles(["RWristYaw"], [1.5], 0.5)
        self.motion.openHand("RHand")
    
        self.genSpeech(phrase)
        time.sleep(2)
        self.rest()


    def shrug(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Body",1.0,self.stiffness)
        self.motion.setAngles(["RShoulderRoll", "LShoulderRoll"], [-0.5, 0.5], 0.4)
        self.motion.setAngles(["RShoulderPitch", "LShoulderPitch"] , [0.75, 0.75] ,0.4)
        self.motion.setAngles(["RElbowYaw", "LElbowYaw"], [2.5, -2.5], 0.4)
        self.motion.setAngles(["RElbowRoll", "LElbowRoll"], [1.2, -1.2], 0.4)

        self.genSpeech(phrase)
        time.sleep(2)
        self.rest()
  
    # arms up in yay motion
    def yay(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Body",1.0,self.stiffness)
        self.motion.setAngles(["RShoulderRoll", "LShoulderRoll"], [-.2, .2], 0.4)
        self.motion.setAngles(["RShoulderPitch", "LShoulderPitch"] , [-.5, -.5] ,0.4)
        self.motion.setAngles(["RElbowYaw", "LElbowYaw"], [1.6, -1.6], 0.4)
        self.motion.setAngles(["RElbowRoll", "LElbowRoll"], [1, -1], 0.4)

        self.genSpeech(phrase)
        time.sleep(2)
        self.rest()

    # hand to templ in thinking pose
    def think(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Body",1.0,self.stiffness)
        self.motion.setAngles(["LShoulderRoll"], [ .29], 0.4)
        self.motion.setAngles(["LShoulderPitch"] , [ -.4] ,0.4)
        self.motion.setAngles(["LElbowYaw"], [-0.7], 0.4)
        self.motion.setAngles(["LElbowRoll"], [-1.5], 0.4)
        self.motion.setAngles(["LWristYaw"], [-0.9], 0.4)
        self.motion.setAngles(["HeadYaw"], [.07], 0.4)
        self.motion.setAngles(["HeadPitch"], [0.45], 0.4)

        self.genSpeech(phrase)
        time.sleep(3)
        self.rest()

    # throw head back in exasperation, speak, bring head back
    def exasperated(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Head",1,self.stiffness)
        self.motion.setAngles(["HeadPitch"], [-0.5], 0.4)
        time.sleep(0.5)
        self.genSpeech(phrase)
        time.sleep(1)
        self.motion.setAngles(["HeadPitch"], [0], 0.4)
        self.rest()

    # throw head back, bring forward, speak
    def face_back(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Head",1,self.stiffness)
        self.motion.setAngles(["HeadPitch"], [-0.5], 0.4)
        time.sleep(0.75)
        self.motion.setAngles(["HeadPitch"], [0], 0.4)
        self.genSpeech(phrase)
        self.rest()


    def shakeHead(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Body",1.0,self.stiffness)
        self.motion.setAngles(["HeadPitch"], [0.3], 0.4) 
        time.sleep(0.1)
        self.motion.setAngles(["HeadYaw"], [0.7], 0.2)  
        time.sleep(0.5) 

        self.genSpeech(phrase) 

        self.motion.setAngles(["HeadYaw"], [-0.7], 0.4)    
        time.sleep(0.5) 
        self.motion.setAngles(["HeadYaw"], [0.7], 0.4)  
        time.sleep(0.5) 
        self.motion.setAngles(["HeadYaw"], [-0.7], 0.4) 
        self.motion.setAngles(["HeadPitch"], [0.15], 0.1)  
        time.sleep(0.5)  
        self.motion.setAngles(["HeadYaw"], [0.7], 0.4) 
        time.sleep(0.3)
        self.motion.setAngles(["HeadYaw"], [0], 0.2) 
        time.sleep(0.3)
        self.motion.setAngles(["HeadPitch"], [0], 0.2) 

        time.sleep(3)

    def nod(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Body",1.0,self.stiffness)
        self.motion.setAngles(["HeadPitch"], [0.3], 0.1) 
        time.sleep(0.1)

        self.genSpeech(phrase)

        self.motion.setAngles(["HeadPitch"], [0.07], 0.1)
        time.sleep(0.5)
        self.motion.setAngles(["HeadPitch"], [0.3], 0.1)
        time.sleep(0.5)
        self.motion.setAngles(["HeadPitch"], [0.07], 0.1)
        time.sleep(0.5)
        self.motion.setAngles(["HeadPitch"], [0.3], 0.1)
        time.sleep(0.5)
        self.motion.setAngles(["HeadPitch"], [0.07], 0.1)
        time.sleep(0.5)
        self.motion.setAngles(["HeadPitch"], [0.3], 0.1)
        time.sleep(0.5)
        self.motion.setAngles(["HeadPitch"], [0.07], 0.1)
       
        time.sleep(3)


    # pump arm up into the air and pull down 
    def pump(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Body",1.0,self.stiffness)
        self.motion.setAngles(["RShoulderPitch"], [-0.43], 0.3)
        self.motion.setAngles(["RShoulderRoll"], [0.06], 0.3)
        self.motion.setAngles(["RWristYaw"], [0.85], 0.3)
        self.motion.setAngles(["RElbowRoll"], [1.54], 0.3)
        self.motion.setAngles(["RElbowYaw"], [1.6], 0.3)
        time.sleep(1)
        self.motion.setAngles(["RShoulderPitch"], [0.6], 0.5)
        self.motion.setAngles(["RShoulderRoll"], [0.3], 0.5)
        self.motion.setAngles(["RWristYaw"], [1.2], 0.5)
        self.motion.setAngles(["RElbowRoll"], [1.54], 0.5)
        self.motion.setAngles(["RElbowYaw"], [1.6], 0.5)

        self.genSpeech(phrase)

        time.sleep(0.5)
        self.rest()

    # bring arm up to face and tilt face down
    def face_palm(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Body",1.0,self.stiffness)
        self.motion.setAngles(["RShoulderPitch"], [0.7], 0.3)
        self.motion.setAngles(["RShoulderRoll"], [0.3], 0.3)
        self.motion.setAngles(["RWristYaw"], [0.9], 0.3)
        self.motion.setAngles(["RElbowRoll"], [1.54], 0.3)
        self.motion.setAngles(["RElbowYaw"], [1.1], 0.3)
        self.motion.setAngles(["RHipPitch"], [-1.5], 0.3)
        self.motion.setAngles(["RHipRoll"], [-0.11], 0.3)

        self.motion.setAngles(["HeadYaw"], [-0.08], 0.3)
        self.motion.setAngles(["HeadPitch"], [0.5], 0.3)

        self.motion.setAngles(["LShoulderPitch"], [0.7], 0.3)
        self.motion.setAngles(["LShoulderRoll"], [-0.21], 0.3)
        self.motion.setAngles(["LWristYaw"], [-1], 0.3)
        self.motion.setAngles(["LElbowRoll"], [-1.54], 0.3)
        self.motion.setAngles(["LElbowYaw"], [-1.1], 0.3)
        self.motion.setAngles(["LHipPitch"], [-1.5], 0.3)
        self.motion.setAngles(["LHipRoll"], [1.11], 0.3)

        self.genSpeech(phrase)
        time.sleep(3)
        self.rest()

    # filler to perform no action while still speaking in same react function
    def none(self, phrase = "", wait=True):
        self.genSpeech(phrase)
        self.rest()

    # rotate wrists to move hands during speach
    def wrist(self, phrase = "", wait=True):
        self.motion.stiffnessInterpolation("Body",1.0,self.stiffness)
        self.motion.setAngles(["RWristYaw"], [1.5], 0.5)
        self.motion.setAngles(["LWristYaw"], [-1.5], 0.5)

        self.genSpeech(phrase)
        time.sleep(2)
        self.rest()


    # go back to neutral position and release motors to prevent from overheating
    # this is included at end of every motion
    def rest(self):
        self.posture.goToPosture("Sit", 1.0)
        self.motion.setAngles(["HeadPitch"], [0.2], 0.1) 

        self.motion.stiffnessInterpolation("Body",0.0,self.stiffness)
        self.motion.setStiffnesses(["LHipPitch", "RHipPitch"],[0.3, 0.3])
        self.motion.setStiffnesses(["LHipYawPitch", "RHipYawPitch"],[0.3, 0.3])

 # CONTROL ____________________________________________________________
    # react takes a phrase and motion, waits for permission to speak (input = "\n") and gives answer
    # also allows response to participant's questions or statements before giving answer
    # preprogrammed responses  based on inputted letter 
    # can also type in any text string (must be longer than 2 characters) to generate spontaneous speach if necessary
    def react(self, action="", answer =""):
        go = raw_input()
        while (go != ""):
            if len(go) >2:
                self.genSpeech(go)
            elif go == "m":
                self.genSpeech("Please do not move me.")
                self.posture.goToPosture("Sit", 1.0)
            elif go == "i":
                self.genSpeech("That hurt my feelings")
            elif go == "q":
                self.genSpeech("What was the question?")
            elif go == "y":
                self.genSpeech("yes")
            elif go == "n":
                self.genSpeech("no")
            elif go == "d":
                self.genSpeech("If you think so.")
            elif go == "u":
                self.genSpeech("I dont know.")
            elif go == "p":
                self.genSpeech("We can ask Aileen about that later, but we should move on now")
            elif go == "s": #skip this response and go on (eg. if particant does not wait for nao)
                return go
            else:
                print "unknown option"
            go = raw_input()

        # broke out of loop - give answer
        if action != "": 
            action(answer)
        else:
            self.genSpeech(answer) 
        return go



    # react_answer takes the question number and a phrase (short version of answer for repeats)
    # to respond to correctness of answer, type either 'c' for correct or 'w' for wrong and Nao will respond
    # with action and phrase from list (cycles through everytime)
    # also allows response to participant's questions or statements before 
    # preprogrammed responses  based on inputted letter - can use 're' to repeat answer
    # can also type in any text string (must be longer than 2 characters) to generate spontaneous speach if necessary
    def react_answer(self, i, answer=""):
        correct = ["We are doing so well", "Yay a correct answer", "This is going great", "Yes! Awesome!", "Cool! A point"]
        incorrect = ["Oh no", "Shoot, maybe next time", "Oh man", "It's okay. We will get the next one", "That's alright. That was a hard one"]
        correct_actions = [self.pump, self.yay, self.nod, self.pump, self.yay]
        incorrect_actions = [self.shakeHead, self.shakeHead, self.face_palm, self.face_back, self.face_back]
        go = raw_input()
        while (True):
            if len(go) >2:
                self.genSpeech(go)
            elif go == "w": # wrong answer
                incorrect_actions[i%5](incorrect[i%5])
                break
            elif go == "i":
                self.genSpeech("That hurt my feelings")
            elif go == "re":
                self.genSpeech(answer)
            elif go == "c": # correct answer
                correct_actions[i%5](correct[i%5])
                break
            elif go == "t": # thinking to long
                self.genSpeech("go ahead and decide what to type")
            elif go == "m": # someone is trying to move Nao
                self.genSpeech("Please do not move me.")
                self.posture.goToPosture("Sit", 1.0)
            elif go == "y":
                self.genSpeech("yes")
            elif go == "n":
                self.genSpeech("no")
            elif go == "d":
                self.genSpeech("If you think so.")
            elif go == "u":
                self.genSpeech("I dont know.")
            elif go == "p":
                self.genSpeech("We can ask Aileen about that later, but we should move on now")
            elif go == "s": #skip -- eg if person already went to next question
                break

            go = raw_input()
        return go

    
    # RELEASE THE JOINTS SO IT WON'T COMPLAIN
    def releaseNao(self):
        try:
            self.posture.goToPosture("SitRelax", 1.0)
            self.motion.stiffnessInterpolation("Body",0.0,self.stiffness)
        except Exception, e:
            print "Error when sitting down nao and making nao unstiff: "+str(e)


#____________________________________________________________
