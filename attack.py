#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread

def printEnemyTypeAndHealth(gameInfo, enemyArrayPosition):

    enemy = gameInfo.enemySlots[enemyArrayPosition]

    if enemy == "Dead":
        print("Enemy health (Dead): " + str(0))

    else:
        print("Enemy Type: " + enemy["type"] + " | " + "Enemy health: " + str(enemy["health"]))

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

                currentEnemy = gameInfo.enemySlots[enemyToAttack]

                distanceToBottle = horn.distanceSensor.distance()
                if log:
                    print("Looking if hit bottle: ", distanceToBottle)
                if distanceToBottle > 400:

                    horn.craneMotor.stop()
                    gameInfo.hornEnergy = gameInfo.hornEnergy - 300
                    currentEnemy["health"] = currentEnemy["health"] - 200

                    if (currentEnemy["health"] <= 0):
                        horn.ev3.speaker.play_file(SoundFile.GENERAL_ALERT)
                        gameInfo.enemySlots[enemyToAttackArrayPosition] = "Dead"

                    printEnemyTypeAndHealth(gameInfo, enemyToAttack)
                    print("Crane attack used. New energy: " + str(gameInfo.hornEnergy))
                    print()
                    return

#* Horn headbutts the bottle and goes backwards
def headbutt(log, horn, calibration, gameInfo, enemyToAttackArrayPosition, followingMovementSpeed)   :

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
                
            enemyToAttack = gameInfo.enemySlots[enemyToAttackArrayPosition]

            horn.robot.stop()
            gameInfo.hornEnergy = gameInfo.hornEnergy - 150
            enemyToAttack["health"] = enemyToAttack["health"] - 100

            if (enemyToAttack["health"]) <= 0:
                horn.ev3.speaker.play_file(SoundFile.GENERAL_ALERT)
                gameInfo.enemySlots[enemyToAttackArrayPosition] = "Dead"

            printEnemyTypeAndHealth(gameInfo, enemyToAttackArrayPosition)

            print("Headbutt attack used. New energy: " + str(gameInfo.hornEnergy))
            print() 
            return
    
#* Horn plays a sound effect
def soundAttack(horn, gameInfo, enemyToAttackArrayPosition):

    print("Starting attack - Sound.")

    enemyToAttack = gameInfo.enemySlots[enemyToAttackArrayPosition]

    horn.ev3.speaker.play_file(SoundFile.BACKING_ALERT)
    gameInfo.hornEnergy = gameInfo.hornEnergy - 50
    enemyToAttack["health"] = enemyToAttack["health"] - 50
    if (enemyToAttack["health"]) <= 0:
        horn.ev3.speaker.play_file(SoundFile.GENERAL_ALERT)
        gameInfo.enemySlots[enemyToAttackArrayPosition] = "Dead"

    printEnemyTypeAndHealth(gameInfo, enemyToAttackArrayPosition)
    print("Sound attack used. New energy: " + str(gameInfo.hornEnergy))
    print()