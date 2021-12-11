#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread

def craneAttack(log, ev3, robot, craneMotor, lineColorSensor, distanceSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, distanceToStop):

    threshold = (enemyLineBlue + boardBlue) / 2
    if log:
        print("Threshold: ", threshold)

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

    while True:

        lineColor = lineColorSensor.color()
        if log:
            print("Line Color: ", lineColor) 

        lineReflection = lineColorSensor.rgb()[2]
        if log:
            print("Line Sensor Reflection: ", lineReflection) 

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        if log:
            print("Deviation: ", deviation)

        # Calculate the turn rate.
        turnRate = proportionalGain * deviation
        if log:
            print("Turn Rate: " + str(turnRate) + "\n") 

        # Set the drive base speed and turn rate.
        robot.drive(-followingMovementSpeed, turnRate)

        distanceToBottle = distanceSensor.distance()

        # Stop if it reaches a bottle
        if log:
            print("Distance To Bottle: ", distanceToBottle) 

        if (distanceToBottle > distanceToStop): 
            
            robot.stop()

            # Keep spinning until bottle gets hit
            craneMotor.run(-200)
            while True:

                distanceToBottle = distanceSensor.distance()
                if log:
                    print("Looking if hit bottle: ", distanceToBottle)
                if distanceToBottle > 300:
                    craneMotor.stop()
                    return

def headbutt(log, ev3, robot, lineColorSensor, distanceSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, distanceToStop)   :

    threshold = (enemyLineBlue + boardBlue) / 2
    if log:
        print("Threshold: ", threshold)

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

    while True:

        lineColor = lineColorSensor.color()
        if log:
            print("Line Color: ", lineColor) 

        lineReflection = lineColorSensor.rgb()[2]
        if log:
            print("Line Sensor Reflection: ", lineReflection) 

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        if log:
            print("Deviation: ", deviation)

        # Calculate the turn rate.
        turnRate = proportionalGain * deviation
        if log:
            print("Turn Rate: " + str(turnRate) + "\n") 

        # Set the drive base speed and turn rate.
        robot.drive(followingMovementSpeed, turnRate)

        distanceToBottle = distanceSensor.distance()

        # Stop if headbutts reaches a bottle
        if log:
            print("Distance To Bottle: ", distanceToBottle) 

        if (distanceToBottle > distanceToStop): 
            
            robot.stop()
            return

def soundAttack(ev3):
    ev3.speaker.play_file(SoundFile.BACKING_ALERT)

            


         
