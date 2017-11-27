#!/usr/bin/env python
#some code adapted from lego nxt for python docs

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

b = nxt.locator.find_one_brick()

#print 'Touch:', Touch(b, PORT_1).get_sample()
#print 'Sound:', Sound(b, PORT_2).get_sample()
#print 'Light:', Light(b, PORT_3).get_sample()
#print 'Ultrasonic:', Ultrasonic(b, PORT_4).get_sample()

def spin_around(b):
    m_left = Motor(b, PORT_B)
    m_left.turn(100, 360)
    m_right = Motor(b, PORT_C)
    m_right.turn(-100, 360)

def goStraight(b):#not really
    m_left = Motor(b, PORT_B)
    #m_left.turn(100, 360)
    m_right = Motor(b, PORT_C)
    m_left.run(100)
    m_right.run(100)
    time.sleep(2)
    m_left.brake()
    m_right.brake()
    #m_right.turn(100, 360)

#colorSense=Color21(b,PORT_1)
#colorSense.set_light_color(Type.COLORFULL)
lightSense=Light(b,PORT_4)
lightSense.set_illuminated(False)
while True:
   light=lightSense.get_lightness()
   #color=colorSense.get_color_name()
   if light>200:
      goStraight(b)
     # spin_around(b)
   else:
      #print color
      print light
      time.sleep(1)

