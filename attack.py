#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread

# Horn goes backwards until it is in a position to attack with the crane, then keeps attacking until the enemy falls.
def craneAttack(log, horn, calibration, followingMovementSpeed, distanceToStop):

    threshold = (calibration.enemyLineBlue + calibration.boardBlue) / 2
    if log:
        print("Threshold: ", threshold)

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

    while True:

        lineColor = horn.lineColorSensor.color()
        if log:
            print("Line Color: ", lineColor) 

        lineReflection = horn.lineColorSensor.rgb()[2]
        if log:
            print("Line Sensor Reflection: ", lineReflection) 

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        if log:
            print("Deviation: ", deviation)

        # Calculate the turn rate.
        turnRate = calibration.proportionalGain * deviation
        if log:
            print("Turn Rate: " + str(turnRate) + "\n") 

        # Set the drive base speed and turn rate.
        horn.robot.drive(-followingMovementSpeed, turnRate)

        distanceToBottle = horn.distanceSensor.distance()

        # Stop if it reaches a bottle
        if log:
            print("Distance To Bottle: ", distanceToBottle) 

        if (distanceToBottle > distanceToStop): 
            
            horn.robot.stop()

            # Keep spinning until bottle gets hit
            horn.craneMotor.run(-200)
            while True:

                distanceToBottle = horn.distanceSensor.distance()
                if log:
                    print("Looking if hit bottle: ", distanceToBottle)
                if distanceToBottle > 400:
                    horn.craneMotor.stop()
                    return

def headbutt(log, horn, calibration, followingMovementSpeed)   :

    threshold = (calibration.enemyLineBlue + calibration.boardBlue) / 2
    if log:
        print("Threshold: ", threshold)

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

    while True:

        lineColor = horn.lineColorSensor.color()
        if log:
            print("Line Color: ", lineColor) 

        lineReflection = horn.lineColorSensor.rgb()[2]
        if log:
            print("Line Sensor Reflection: ", lineReflection) 

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        if log:
            print("Deviation: ", deviation)

        # Calculate the turn rate.
        turnRate = calibration.proportionalGain * deviation
        if log:
            print("Turn Rate: " + str(turnRate) + "\n") 

        # Set the drive base speed and turn rate.
        horn.robot.drive(followingMovementSpeed, turnRate)

        distanceToBottle = horn.distanceSensor.distance()

        if (distanceToBottle > 400): # Stop if headbutts reaches a bottle 
                    
            if log:
                print("Distance To Bottle: ", distanceToBottle) 
                
            horn.robot.stop()
            return

def soundAttack(horn):
    horn.ev3.speaker.play_file(SoundFile.BACKING_ALERT)

            


         
