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

            #* Robot stops, sets itself up, and rotates to the enemy line
            robot.stop()
            ev3.speaker.beep()
            followMainLineTime(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, enemyLineReflection, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360, 2000)
            ev3.speaker.beep()
            robot.turn(calibratedTurn(-110 * negativeTurnCalibration, turnCalibrationTo360))
            
            #* Robot follows the enemy line until the bottle
            followEnemyLineUntilBottle(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360)

            #* Robot goes backwards until the black tape and rotates back to the main line
            ev3.speaker.beep()
            followEnemyLineUntilTime(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360, 1000)
            #robot.straight(-100)
            followEnemyLineBackUntilBlack(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360)
            ev3.speaker.beep()
            robot.turn(calibratedTurn(90 * negativeTurnCalibration, turnCalibrationTo360))

            #* Robot keeps following the main line
            followMainLineTime(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, enemyLineReflection, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360, 5000)

            break
           
        # You can wait for a short time or do other things in this loop.
        # wait(1)

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

def followEnemyLineUntilBottle(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (enemyLineBlue + boardBlue) / 2
    print("Threshold: ", threshold)

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

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

        # Stop if it reaches a bottle
        print("Distance To Bottle: ", distanceToBottle)
        if (distanceToBottle < 50): 
            robot.stop()
            color.sayColor(ev3, enemyColorSensor)
            break

        # If the bottle doesn't exist, more than 5 seconds have passed when the robot reaches a black line.
        if ( (timer.time() - followEnemyLineBeginning > 3000) and (lineColorSensor.color() == Color.BLACK) ):
            robot.stop()
            # ev3.speaker.say("No bottle")
            break
 
        wait(1)

def followEnemyLineBackUntilTime(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360, timeToFollow):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (enemyLineBlue + boardBlue) / 2
    print("Threshold: ", threshold)

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

    while ( (timer.time() - followEnemyLineBeginning ) < timeToFollow ):

        lineColor = lineColorSensor.color()
        print("Line Color: ", lineColor)

        lineReflection = lineColorSensor.rgb()[2]
        print("Line Sensor Reflection: ", lineReflection)

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        print("Deviation: ", deviation)

        # Calculate the turn rate.
        turnRate = -(proportionalGain * deviation)
        print("Turn Rate: " + str(turnRate) + "\n")

        # Set the drive base speed and turn rate.
        robot.drive(-followingMovementSpeed, turnRate)

        wait(1)

def followEnemyLineBackUntilBlack(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360):

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
        turnRate = -(proportionalGain * deviation)
        print("Turn Rate: " + str(turnRate) + "\n")

        # Set the drive base speed and turn rate.
        robot.drive(-followingMovementSpeed, turnRate)

        if (lineColor == Color.BLACK):
            robot.stop()
            break

        wait(1)

def goBackToBoardBeginning():
    return