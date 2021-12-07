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

def followMainLine(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360):

    enemyLinesHavePassed = 0

    threshold = (mainLineReflection + boardReflection) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter 

    while True:

        lineColor = lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter

        lineReflection = lineColorSensor.reflection()
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter

        # Calculate the turn rate.
        turnRate = proportionalGain * deviation
        # print("Turn Rate: " + str(turnRate) + "\n")# TODO: Log Parameter

        # Set the drive base speed and turn rate.
        robot.drive(followingMovementSpeed, turnRate)

        #* When the robot reaches the enemy line
        if (lineColorSensor.color() == enemyLineColor):

            enemyLinesHavePassed += 1

            #* Robot stops, sets itself up, and rotates to the enemy line
            robot.stop()
            ev3.speaker.beep()
            followMainLineTime(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, proportionalGain, followingMovementSpeed, 2000)
            ev3.speaker.beep()
            robot.turn(calibratedTurn(-110 * negativeTurnCalibration, turnCalibrationTo360))
            ev3.speaker.beep()
            
            #* Robot follows the enemy line until the bottle
            followEnemyLineUntilBottle(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed)
            #* Robot goes backwards until the black tape and rotates back to the main line
            ev3.speaker.beep()
            followEnemyLineBackUntilTime(ev3, robot, lineColorSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, 1000)
            ev3.speaker.beep()
            followEnemyLineBackUntilBlack(ev3, robot, lineColorSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed)
            ev3.speaker.beep()
            robot.turn(calibratedTurn(90 * negativeTurnCalibration, turnCalibrationTo360))
            ev3.speaker.beep()

            

            #* Robot keeps following the main line
            
            # followMainLineTime(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, proportionalGain, followingMovementSpeed, 5000)

            # break
           
        # You can wait for a short time or do other things in this loop.
        # wait(1)

def followMainLineTime(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, proportionalGain, followingMovementSpeed, timeToFollow):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (mainLineReflection + boardReflection) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter

    timer = StopWatch()
    timerBeginning = timer.time()
    while (timer.time() - timerBeginning) < timeToFollow: # Start following the line endlessly.

        lineColor = lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter

        lineReflection = lineColorSensor.reflection()
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter

        # Calculate the turn rate.
        turnRate = proportionalGain * deviation
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter

        # Set the drive base speed and turn rate.
        robot.drive(followingMovementSpeed, turnRate)

        # You can wait for a short time or do other things in this loop.
        wait(1)

def followEnemyLineUntilBottle(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (enemyLineBlue + boardBlue) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

    while True:

        lineColor = lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter

        lineReflection = lineColorSensor.rgb()[2]
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter

        # Calculate the turn rate.
        turnRate = proportionalGain * deviation
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter

        # Set the drive base speed and turn rate.
        robot.drive(followingMovementSpeed, turnRate)

        distanceToBottle = distanceSensor.distance()

        # Stop if it reaches a bottle
        print("Distance To Bottle: ", distanceToBottle)
        if (distanceToBottle < 50): 
            robot.stop()
            ev3.speaker.beep()
            print("Horn has reached a bottle.\n")
            color.sayColor(ev3, enemyColorSensor)
            break

        # If the bottle doesn't exist, more than 3 seconds have passed when the robot reaches a black line.
        if ( (timer.time() - followEnemyLineBeginning > 3000) and (lineColorSensor.color() == Color.BLACK) ):
            robot.stop()
            ev3.speaker.beep()
            print("Horn has reached the end of the enemy line and found no bottle.\n")
            ev3.speaker.say("No bottle")
            break
 
        wait(1)

def followEnemyLineBackUntilTime(ev3, robot, lineColorSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, timeToFollow):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (enemyLineBlue + boardBlue) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter 

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

    while ( (timer.time() - followEnemyLineBeginning ) < timeToFollow ):

        lineColor = lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter 

        lineReflection = lineColorSensor.rgb()[2]
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter 

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter 

        # Calculate the turn rate.
        turnRate = (proportionalGain * deviation)
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter 

        # Set the drive base speed and turn rate.
        robot.drive(-followingMovementSpeed, turnRate)

        wait(1)

def followEnemyLineBackUntilBlack(ev3, robot, lineColorSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (enemyLineBlue + boardBlue) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter 

    while True:

        lineColor = lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter 

        lineReflection = lineColorSensor.rgb()[2]
        print("Line Sensor Reflection: ", lineReflection)

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter 

        # Calculate the turn rate.
        turnRate = (proportionalGain * deviation)
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter 

        # Set the drive base speed and turn rate.
        robot.drive(-followingMovementSpeed, turnRate)

        if (lineColor == Color.BLACK):
            robot.stop()
            break

        wait(1)

def goBackToBoardBeginning(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, enemyLineColor, proportionalGain, followingMovementSpeed):

    enemyLinesPassed = 0
    timer = StopWatch()
    timerLastEnemyLinePassed = "" 

    threshold = (mainLineReflection + boardReflection) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter 

    while True:

        lineColor = lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter

        lineReflection = lineColorSensor.reflection()
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter

        # Calculate the turn rate.
        turnRate = -(proportionalGain * deviation)
        # print("Turn Rate: " + str(turnRate) + "\n")# TODO: Log Parameter

        # Set the drive base speed and turn rate.
        robot.drive(followingMovementSpeed, turnRate)

        #* When the robot reaches the enemy line
        if (lineColorSensor.color() == enemyLineColor):

            # The first instant the robot passes the enemy line always counts
            if enemyLinesPassed == 0:
                timerLastEnemyLinePassed = timer.time()
                enemyLinesPassed += 1
                ev3.speaker.beep()
                print("Going back, lines passed: ", enemyLinesPassed)

            # After that, the instant the robot passes the enemy line counts if more than two seconds have passed, to avoid duplicate readings
            else:
                if (timer.time() - timerLastEnemyLinePassed > 2000):
                    timerLastEnemyLinePassed = timer.time()
                    enemyLinesPassed += 1
                    ev3.speaker.beep()
                    print("Going back, lines passed: ", enemyLinesPassed)

        if enemyLinesPassed == 6:
            robot.stop()


    return