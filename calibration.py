from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

def printLineColorSensor(lineColorSensor):

    while True:
        print(lineColorSensor.color())
        #print(lineColorSensor.reflection())
        #print(lineColorSensor.ambient())
        #print(lineColorSensor.rgb())
        #print()
        wait(1000)

def printEnemyColorSensor(enemyColorSensor):

    while True:
        print(enemyColorSensor.color())
        #print(enemyColorSensor.reflection())
        #print(enemyColorSensor.ambient())
        #print(enemyColorSensor.rgb())
        #print()
        wait(1000)

#! RGB
# (6, 16, 19) BLACK
# (40, 40, 60) BOARD
# (51, 22, 36) RED