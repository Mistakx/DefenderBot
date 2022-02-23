from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait


def printLineColorSensor(lineColorSensor):

    while True:
        #print(lineColorSensor.color())
        #print(lineColorSensor.reflection())
        #print(lineColorSensor.ambient())
        print(lineColorSensor.rgb())
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

def printDistance(distanceSensor):
    while True:
        print(distanceSensor.distance())
        wait(1000)

#! RGB
# (6, 16, 19) BLACK
# (40, 40, 60) BOARD
# (51, 22, 36) RED
