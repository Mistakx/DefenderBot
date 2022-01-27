from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import color

#! Turn

def calibratedTurn(turnAngle, calibration): 
    #* Positive turn - Left | Negative turn - Right

    # 360 - 900
    # 500 - x

    calibratedTurn = ( (turnAngle * calibration.turnCalibrationTo360) / 360)

    return calibratedTurn


#! Main Line

def followMainLineUntilEnemyLine(log, horn, calibration, gameInfo, followingMovementSpeed, lineToGoTo):

    firstLine = True
    timer = StopWatch()
    timerLastEnemyLinePassed = "" 

    threshold = (calibration.mainLineReflection + calibration.boardReflection) / 2
    if log:
        print("Threshold: ", threshold) 
    
    while True:

        lineColor = horn.lineColorSensor.color()
        if log:
            print("Line Color: ", lineColor) 

        lineReflection = horn.lineColorSensor.reflection()
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

        #* When the horn.robot reaches the enemy line
        if (horn.lineColorSensor.color() == calibration.enemyLineColor):

            # The first instant the horn.robot passes the enemy line always counts
            if firstLine == True:
                timerLastEnemyLinePassed = timer.time()
                gameInfo.currentPosition += 1
                horn.ev3.speaker.beep()

            # After that, the instant the horn.robot passes the enemy line counts if more than two seconds have passed, to avoid duplicate readings
            else:
                if (timer.time() - timerLastEnemyLinePassed > 2000):
                    timerLastEnemyLinePassed = timer.time()
                    gameInfo.currentPosition += 1
                    horn.ev3.speaker.beep()

            print("Following main line, number of lines passed: ", gameInfo.currentPosition)


        if gameInfo.currentPosition == lineToGoTo:
            horn.robot.stop()
            return

def followMainLineTime(horn, calibration, followingMovementSpeed, timeToFollow):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (calibration.mainLineReflection + calibration.boardReflection) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter

    timer = StopWatch()
    timerBeginning = timer.time()
    while (timer.time() - timerBeginning) < timeToFollow: # Start following the line endlessly.

        lineColor = horn.lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter

        lineReflection = horn.lineColorSensor.reflection()
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter

        # Calculate the turn rate.
        turnRate = calibration.proportionalGain * deviation
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter

        # Set the drive base speed and turn rate.
        horn.robot.drive(followingMovementSpeed, turnRate)

        #wait(1)


#! Enemy line
            
def followEnemyLineUntilBottle(log, horn, calibration, followingMovementSpeed):

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

        # Stop if it reaches a bottle
        if log:
            print("Distance To Bottle: ", distanceToBottle)

        if (distanceToBottle < 55): 
            horn.robot.stop()
            horn.ev3.speaker.beep()
            wait(1000) # Waits for the bottle to reset, in case the horn.robot hit it
            enemy = color.identifyEnemy(horn.ev3, horn.enemyColorSensor)
            print("Movement: Horn has reached a bottle.")
            try:
                print("Enemy type: ", enemy["type"])
                print()
                return enemy
            except: 
                print("Movement: Enemy invalid.\n")
                return enemy

        # If the bottle doesn't exist, more than 3 seconds have passed when the horn.robot reaches a black line
        # The horn.robot has to have passed the first line, but not the second.
        # We could detect if the horn.robot passes two black lines.
        # But sometimes the angle it rotates when going from the black to the red line makes it so it misses the first black line.
        # The best aproach is to wait some seconds for it to pass the first black line, and detect the black line after that, which is going to be end line.
        if ( (timer.time() - followEnemyLineBeginning > 3000) and (horn.lineColorSensor.color() == Color.BLACK) ):
            horn.robot.stop()
            print("Horn has reached the end of the enemy line and found no bottle.\n")
            #horn.ev3.speaker.say("No bottle")
            return "No bottle"
 
        # wait(1)

def followEnemyLineBackUntilTime(horn, calibration, followingMovementSpeed, timeToFollow):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (calibration.enemyLineBlue + calibration.boardBlue) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter 

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

    while ( (timer.time() - followEnemyLineBeginning ) < timeToFollow ):

        lineColor = horn.lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter 

        lineReflection = horn.lineColorSensor.rgb()[2]
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter 

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter 

        # Calculate the turn rate.
        turnRate = (calibration.proportionalGain * deviation)
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter 

        # Set the drive base speed and turn rate.
        horn.robot.drive(-followingMovementSpeed, turnRate)

        #wait(1)

def followEnemyLineBackUntilBlack(horn, calibration, followingMovementSpeed):

    # When black            # When white 
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20 
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (calibration.enemyLineBlue + calibration.boardBlue) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter 

    while True:

        lineColor = horn.lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter 

        lineReflection = horn.lineColorSensor.rgb()[2]
        #print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter 

        # Calculate the turn rate.
        turnRate = (calibration.proportionalGain * deviation)
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter 

        # Set the drive base speed and turn rate.
        horn.robot.drive(-followingMovementSpeed, turnRate)

        if (lineColor == Color.BLACK):
            horn.robot.stop()
            return

        #wait(1)


#! Back to beginning

def goBackToFirstEnemyLine(horn, calibration, followingMovementSpeed, gameInfo):

    enemyLinesPassed = 0
    timer = StopWatch()
    timerLastEnemyLinePassed = "" 

    threshold = (calibration.mainLineReflection + calibration.boardReflection) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter 

    while True:

        lineColor = horn.lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter

        lineReflection = horn.lineColorSensor.reflection()
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter

        # Calculate the turn rate.
        turnRate = -(calibration.proportionalGain * deviation)
        # print("Turn Rate: " + str(turnRate) + "\n")# TODO: Log Parameter

        # Set the drive base speed and turn rate.
        horn.robot.drive(followingMovementSpeed, turnRate)

        #* When the horn.robot reaches the enemy line
        if (horn.lineColorSensor.color() == calibration.enemyLineColor):

            # The first instant the horn.robot passes the enemy line always counts
            if enemyLinesPassed == 0:
                timerLastEnemyLinePassed = timer.time()
                enemyLinesPassed += 1
                horn.ev3.speaker.beep()
                print("Going back, lines passed: ", enemyLinesPassed)

            # After that, the instant the horn.robot passes the enemy line counts if more than two seconds have passed, to avoid duplicate readings
            else:
                if (timer.time() - timerLastEnemyLinePassed > 2000):
                    timerLastEnemyLinePassed = timer.time()
                    enemyLinesPassed += 1
                    horn.ev3.speaker.beep()
                    print("Going back, lines passed: ", enemyLinesPassed)

        # Horn stops when it reaches the final line (when it passes the same number of lines of its current position)
        if enemyLinesPassed == gameInfo.currentPosition:
            gameInfo.currentPosition = 0 
            horn.robot.stop()
            print() # New line after the last going back print
            return

def goBackTime(horn, calibration, followingMovementSpeed, timeToFollow):

    threshold = (calibration.mainLineReflection + calibration.boardReflection) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter

    timer = StopWatch()
    timerBeginning = timer.time()

    while (timer.time() - timerBeginning) < timeToFollow: # Start following the line endlessly.

        lineColor = horn.lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter

        lineReflection = horn.lineColorSensor.reflection()
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold 
        # print("Deviation: ", deviation) # TODO: Log Parameter

        # Calculate the turn rate.
        turnRate = -(calibration.proportionalGain * deviation)
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter

        # Set the drive base speed and turn rate.
        horn.robot.drive(followingMovementSpeed, turnRate)

        #wait(1)


#! Multiple movements

#* Horn rotates, goes back to beggining, and rotates again  
def rotateAndGoToBeggining(horn, calibration, gameInfo):
 
    # print("End of the board reached, going back to the beginning.")
    followMainLineTime(horn, calibration, calibration.followingMovementSpeed, 3000)
    horn.ev3.speaker.beep()
    horn.robot.turn(calibratedTurn(-190, calibration))
    horn.ev3.speaker.beep()
    goBackToFirstEnemyLine(horn, calibration, calibration.followingMovementSpeed*2, gameInfo)
    # Doesn't need a beep because reaching the first enemy line in the last function beeps
    goBackTime(horn, calibration, calibration.followingMovementSpeed, 4000)
    horn.ev3.speaker.beep()
    horn.robot.turn(calibratedTurn(180, calibration))

#* Horn goes backwards until the black tape and rotates back to the main line 
def goBackwardsAndRotate(horn, calibration):
    horn.robot.straight(-200) # Doesn't stop after the straight, since it's going to keep going backwards anyways
    movement.followEnemyLineBackUntilBlack(horn, calibration, calibration.followingMovementSpeed)
    horn.ev3.speaker.beep()
    horn.robot.turn(movement.calibratedTurn(80 * calibration.negativeTurnCalibration, calibration))
    horn.ev3.speaker.beep()
    gameInfo.currentPosition = i + 1