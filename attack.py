#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread

def printEnemyTypeAndHealth(gameInfo, enemyArrayPosition):

    if gameInfo.enemySlots[enemyArrayPosition] == "Dead":
        print("Enemy health: " + str(0))

    else:
        print("Enemy Type: " + (gameInfo.enemySlots[enemyArrayPosition])["type"] + " | " + "Enemy health: " + str((gameInfo.enemySlots[enemyArrayPosition])["health"]))

#* Horn goes backwards until it is in a position to attack with the crane, then keeps attacking until the enemy falls.
def craneAttack(log, horn, calibration, gameInfo, enemyToAttack, followingMovementSpeed, distanceToStop):

    print("Starting attack - Crane.")

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
                    gameInfo.hornEnergy = gameInfo.hornEnergy - 300
                    (gameInfo.enemySlots[enemyToAttack])["health"] = (gameInfo.enemySlots[enemyToAttack])["health"] - 200
                    if (gameInfo.enemySlots[enemyToAttack])["health"] <= 0:
                        horn.ev3.speaker.play_file(SoundFile.GENERAL_ALERT)
                        gameInfo.enemySlots[enemyToAttack] = "Dead"
                    printEnemyTypeAndHealth(gameInfo, enemyToAttack)
                    print("Crane attack used. New energy: " + str(gameInfo.hornEnergy))
                    return

#* Horn headbutts the bottle and goes backwards
def headbutt(log, horn, calibration, gameInfo, enemyToAttack, followingMovementSpeed)   :

    print("Starting attack - Headbutt.")

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
            gameInfo.hornEnergy = gameInfo.hornEnergy - 150
            (gameInfo.enemySlots[enemyToAttack])["health"] = (gameInfo.enemySlots[enemyToAttack])["health"] - 100
            if (gameInfo.enemySlots[enemyToAttack])["health"] <= 0:
                horn.ev3.speaker.play_file(SoundFile.GENERAL_ALERT)
                gameInfo.enemySlots[enemyToAttack] = "Dead"
            printEnemyTypeAndHealth(gameInfo, enemyToAttack)

            print("Headbutt attack used. New energy: " + str(gameInfo.hornEnergy))
            return
    
#* Horn plays a sound effect
def soundAttack(horn, gameInfo, enemyToAttack):

    print("Starting attack - Sound.")

    horn.ev3.speaker.play_file(SoundFile.BACKING_ALERT)
    gameInfo.hornEnergy = gameInfo.hornEnergy - 50
    (gameInfo.enemySlots[enemyToAttack])["health"] = (gameInfo.enemySlots[enemyToAttack])["health"] - 50
    if (gameInfo.enemySlots[enemyToAttack])["health"] <= 0:
        horn.ev3.speaker.play_file(SoundFile.GENERAL_ALERT)
        gameInfo.enemySlots[enemyToAttack] = "Dead"
    printEnemyTypeAndHealth(gameInfo, enemyToAttack)
    print("Sound attack used. New energy: " + str(gameInfo.hornEnergy))

            


         
