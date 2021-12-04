from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import color

#* Positive turn - Left | Negative turn - Right
def calibratedTurn(turnAngle, turnCalibrationTo360): 

    # 360 - 900
    # 500 - x

    calibratedTurn = ( (turnAngle * turnCalibrationTo360) / 360)

    return calibratedTurn

def followMainLine(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (mainLineReflection + boardReflection) / 2
    print("Threshold: ", threshold)

    while True:

        lineColor = lineColorSensor.color()
        print("Line Color: ", lineColor)

        lineReflection = lineColorSensor.reflection()
        print("Line Sensor Reflection: ", lineReflection)

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        print("Deviation: ", deviation)

        # Calculate the turn rate.
        turnRate = proportionalGain * deviation
        print("Turn Rate: " + str(turnRate) + "\n")

        # Set the drive base speed and turn rate.
        robot.drive(followingMovementSpeed, turnRate)

        if (lineColorSensor.color() == enemyLineColor):
            robot.stop()
            ev3.speaker.beep()

            followMainLineTime(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, enemyLineReflection, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360, 2000)
            ev3.speaker.beep()

            robot.turn(calibratedTurn(-110 * negativeTurnCalibration, turnCalibrationTo360))
            followEnemyLineUntilBottle(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360)
            break
            # #* Walk to bottle
            # timer = StopWatch()
            # walkToBottleBeginning = timer.time()
            # walkUntilBottle(robot, distanceSensor)
            # timeWalked = timer.time() - walkToBottleBeginning
            # color.sayColor(ev3, enemyColorSensor)
            # ev3.speaker.say('Bottle')

            # #* Walk back to line
            # print("Time Walked: ", timeWalked)
            # # robot.straight(- int(timeWalked)) # Walk backwards the same amount o time it did until reaching the bottle 
            # walkBackToLine(robot, timeWalked)
            # robot.turn(calibratedTurn(90, turnCalibrationTo360))
            # robot.straight(100)
           
        # You can wait for a short time or do other things in this loop.
        wait(1)

def followMainLineTime(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, enemyLineReflection, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360, timeToFollow):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (mainLineReflection + boardReflection) / 2
    print("Threshold: ", threshold)

    timer = StopWatch()
    timerBeginning = timer.time()
    while (timer.time() - timerBeginning) < timeToFollow: # Start following the line endlessly.

        lineColor = lineColorSensor.color()
        print("Line Color: ", lineColor)

        lineReflection = lineColorSensor.reflection()
        print("Line Sensor Reflection: ", lineReflection)

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        print("Deviation: ", deviation)

        # Calculate the turn rate.
        turnRate = proportionalGain * deviation
        print("Turn Rate: " + str(turnRate) + "\n")

        # Set the drive base speed and turn rate.
        robot.drive(followingMovementSpeed, turnRate)

        # You can wait for a short time or do other things in this loop.
        wait(1)

# def walkBackToLine(robot, timeWalked):
#     robot.turn(calibration.calibratedTurn(180, turnCalibrationTo360))


def followEnemyLineUntilBottle(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (enemyLineBlue + boardBlue) / 2
    print("Threshold: ", threshold)

    while True:

        lineColor = lineColorSensor.color()
        print("Line Color: ", lineColor)

        lineReflection = lineColorSensor.rgb()[2]
        print("Line Sensor Reflection: ", lineReflection)

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        print("Deviation: ", deviation)

        # Calculate the turn rate.
        turnRate = proportionalGain * deviation
        print("Turn Rate: " + str(turnRate) + "\n")

        # Set the drive base speed and turn rate.
        robot.drive(followingMovementSpeed, turnRate)

        distanceToBottle = distanceSensor.distance()

        print("Distance To Bottle: ", distanceToBottle)
        if (distanceToBottle < 50): 
            robot.stop()
            ev3.speaker.beep()
            color.sayColor(ev3, enemyColorSensor)
            break

        wait(1)

def followEnemyLineUntilBlack(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (enemyLineBlue + boardBlue) / 2
    print("Threshold: ", threshold)

    while True:

        lineColor = lineColorSensor.color()
        print("Line Color: ", lineColor)

        lineReflection = lineColorSensor.rgb()[2]
        print("Line Sensor Reflection: ", lineReflection)

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        print("Deviation: ", deviation)

        # Calculate the turn rate.
        turnRate = proportionalGain * deviation
        print("Turn Rate: " + str(turnRate) + "\n")

        # Set the drive base speed and turn rate.
        robot.drive(followingMovementSpeed, turnRate)

        if (lineColor == Color.BLACK):
            robot.stop()
            ev3.speaker.beep()
            robot.turn(calibration.calibratedTurn(90, turnCalibrationTo360))


        wait(1)
