#!/usr/bin/env python

import nxt.locator
from nxt.motor import *
from nxt.sensor import *
import time

class Color21(Color20):
    def get_color_name(self):
        color=self.get_color()
        if color==1:
                return 'black'
        elif color==2:
                return 'blue'
        elif color==3:
                return 'green'
        elif color==4:
                return 'yellow'
        elif color==5:
                return 'red'
        else:
                return 'white'

class robot():
    def __init__(self):
        self.bot = nxt.locator.find_one_brick()
        self.lMotor=Motor(self.bot, PORT_B)
        self.rMotor=Motor(self.bot, PORT_C)
        self.clubMotor=Motor(self.bot,PORT_A)
        self.colorSense=Color21(self.bot,PORT_1)
        self.colorSense.set_light_color(Type.COLORFULL)

    def moveRobot2(self,power=100,degrees=360):#might be more
        self.lMotor.weak_turn(power, degrees)#wheel is C=18cm 
        self.rMotor.weak_turn(power, degrees)#block is 3.5cm
        time.sleep(1)

    def moveRobot(self,power=100,dist=1):
        self.lMotor.run(power)
        self.rMotor.run(power)
        time.sleep(dist)
        self.lMotor.brake()
        self.rMotor.brake()

    def swingBatter(self,power=100,degrees=45):
        self.clubMotor.turn(-power,degrees)
        time.sleep(1)
        self.clubMotor.turn(power,degrees)
        time.sleep(1)



#localization from Lesson 1 Q26
BATCH=3
COLORS=3
COLOR_NAMES=['red','green','blue']

p=[1./(BATCH*COLORS) for prob in range(BATCH*COLORS)]
world=[COLOR_NAMES[num/3] for num in range(BATCH*COLORS)]

#measurements = ['red', 'red','white','green','green','green','white','blue','blue']

#sense probabilities
pHit = 0.6
pMiss = 0.2

#move probabilities
pExact = 0.8
pOvershoot = 0.1
pUndershoot = 0.1

def sense(p, Z):
    q=[]
    for i in range(len(p)):
        hit = (Z == world[i])
        q.append(p[i] * (hit * pHit + (1-hit) * pMiss))
    s = sum(q)
    for i in range(len(q)):
        q[i] = q[i] / s
    return q

def move(p, U):
    q = []
    for i in range(len(p)):
        s = pExact * p[(i-U) % len(p)]
        s = s + pOvershoot * p[(i-U-1) % len(p)]
        s = s + pUndershoot * p[(i-U+1) % len(p)]
        q.append(s)
    return q

done=False
k=0
bot=robot()
motion=1
bSize=75#degrees
while not k==len(world)-1:
    #print k
    #measurement=measurements[k]
    time.sleep(.5)
    measurement=bot.colorSense.get_color_name()
    print measurement,k
    p = sense(p, measurement)
    time.sleep(.5)
    if measurement!=world[k]:#bad block found
        bot.moveRobot2(-70,bSize-10)#moves further backwards?
        p=move(p,-1)
        bot.swingBatter()
        #print "swing the golf club"
        print measurement, " is not ", world[k]
        bot.moveRobot2(70,bSize)
        p=move(p,1)
        #measurements[k]=world[k]
    p = move(p, motion)
    bot.moveRobot2(motion*70,bSize)#(motion*100,.5)
    k=p.index(max(p))

    print p         
