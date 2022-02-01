from pybricks.ev3devices import (
    ColorSensor,
    GyroSensor,
    InfraredSensor,
    Motor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

import color


#! Turn


def calibratedTurn(turnAngle, calibration):
    # * Positive turn - Left | Negative turn - Right

    # 360 - 900
    # 500 - x

    calibratedTurn = (turnAngle * calibration.turnCalibrationTo360) / 360

    return calibratedTurn


#! Main Line


def followMainLineUntilEnemyLine(
    log, horn, calibration, gameInfo, followingMovementSpeed, lineToGoTo
):

    if gameInfo.currentPosition == lineToGoTo:  # Horn already at position to go to.
        print("Horn already at position to go to.")
        return

    elif gameInfo.currentPosition > lineToGoTo:  # Horn already past position to go to.
        print("Horn already past position to go to.\n")
        return

    timer = StopWatch()
    timerLastEnemyLinePassed = None

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

        # * When the Horn reaches the enemy line
        if horn.lineColorSensor.color() == calibration.enemyLineColor:

            # The first instant the Horn passes the enemy line always counts
            if timerLastEnemyLinePassed == None:
                timerLastEnemyLinePassed = timer.time()
                gameInfo.currentPosition += 1
                horn.ev3.speaker.beep()

            # After that, the instant the Horn passes the enemy line counts if more than two seconds have passed, to avoid duplicate readings
            else:
                if timer.time() - timerLastEnemyLinePassed > 2000:
                    timerLastEnemyLinePassed = timer.time()
                    gameInfo.currentPosition += 1
                    horn.ev3.speaker.beep()

            # ? print("Following main line, line passed: ", gameInfo.currentPosition)

        if gameInfo.currentPosition == lineToGoTo:
            horn.robot.stop()
            # ? print()
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
    while (
        timer.time() - timerBeginning
    ) < timeToFollow:  # Start following the line endlessly.

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

        # wait(1)


def followMainLineBackUntilEnemyLine(
    log, horn, calibration, gameInfo, followingMovementSpeed, lineToGoTo
):

    # Horn already at position to go back to.
    if (gameInfo.currentPosition + 1) == lineToGoTo:
        print("Horn already at position to go back to.")
        return

    # Horn already passed position to go back to.
    elif (gameInfo.currentPosition + 1) < lineToGoTo:
        print("Horn already passed position to go back to.")
        return

    timer = StopWatch()
    timerLastEnemyLinePassed = None

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
        turnRate = -(calibration.proportionalGain * deviation)
        if log:
            print("Turn Rate: " + str(turnRate) + "\n")

        # Set the drive base speed and turn rate.
        horn.robot.drive(followingMovementSpeed, turnRate)

        # * When the Horn reaches the enemy line
        if horn.lineColorSensor.color() == calibration.enemyLineColor:

            # The first instant the Horn passes the enemy line always counts
            if timerLastEnemyLinePassed == None:
                timerLastEnemyLinePassed = timer.time()
                gameInfo.currentPosition -= 1
                horn.ev3.speaker.beep()

            # After that, the instant the Horn passes the enemy line counts if more than two seconds have passed, to avoid duplicate readings
            else:
                if timer.time() - timerLastEnemyLinePassed > 2000:
                    timerLastEnemyLinePassed = timer.time()
                    gameInfo.currentPosition -= 1
                    horn.ev3.speaker.beep()

            # If Horn is on slot 3 for example, passing 1 line backwards doesn't leave it on the 2nd line, but on the 3rd.
            # ? print("Following main line back, line passed: ", gameInfo.currentPosition + 1)

        if gameInfo.currentPosition + 1 == lineToGoTo:
            horn.robot.stop()
            # ? print()
            return


def followMainLineBackTime(horn, calibration, followingMovementSpeed, timeToFollow):

    threshold = (calibration.mainLineReflection + calibration.boardReflection) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter

    timer = StopWatch()
    timerBeginning = timer.time()

    while (
        timer.time() - timerBeginning
    ) < timeToFollow:  # Start following the line endlessly.

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

        # wait(1)


#! Enemy line


def followEnemyLineUntilBottle(
    log, printEnemyInfo, horn, calibration, followingMovementSpeed
):

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

        if distanceToBottle < 55:
            horn.robot.stop()
            horn.ev3.speaker.beep()
            wait(1000)  # Waits for the bottle to reset, in case the horn.robot hit it
            enemy = color.identifyEnemy(printEnemyInfo, horn.ev3, horn.enemyColorSensor)

            print("Movement: Horn has reached a bottle.")

            try:
                if printEnemyInfo:
                    print("Enemy type: ", enemy["type"])
                    print()
                return enemy

            except:

                if printEnemyInfo:
                    print("Movement: Enemy invalid.\n")

                return enemy

        # If the bottle doesn't exist, more than 3 seconds have passed when the horn.robot reaches a black line
        # The horn.robot has to have passed the first line, but not the second.
        # We could detect if the horn.robot passes two black lines.
        # But sometimes the angle it rotates when going from the black to the red line makes it so it misses the first black line.
        # The best aproach is to wait some seconds for it to pass the first black line, and detect the black line after that, which is going to be end line.
        if (timer.time() - followEnemyLineBeginning > 3000) and (
            horn.lineColorSensor.color() == Color.BLACK
        ):
            horn.robot.stop()
            print("Horn has reached the end of the enemy line and found no bottle.\n")
            # horn.ev3.speaker.say("No bottle")
            return "No bottle"

        # wait(1)


def followEnemyLineBackUntilTime(
    horn, calibration, followingMovementSpeed, timeToFollow
):

    # When black            # When white
    # Sensor: 2             # Sensor: 7SS
    # Deviation -23         # Deviation -20
    # Turn Rate: -27        # Turn Rate: -25

    threshold = (calibration.enemyLineBlue + calibration.boardBlue) / 2
    # print("Threshold: ", threshold) # TODO: Log Parameter

    timer = StopWatch()
    followEnemyLineBeginning = timer.time()

    while (timer.time() - followEnemyLineBeginning) < timeToFollow:

        lineColor = horn.lineColorSensor.color()
        # print("Line Color: ", lineColor) # TODO: Log Parameter

        lineReflection = horn.lineColorSensor.rgb()[2]
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold
        # print("Deviation: ", deviation) # TODO: Log Parameter

        # Calculate the turn rate.
        turnRate = calibration.proportionalGain * deviation
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter

        # Set the drive base speed and turn rate.
        horn.robot.drive(-followingMovementSpeed, turnRate)

        # wait(1)


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
        # print("Line Sensor Reflection: ", lineReflection) # TODO: Log Parameter

        # Calculate the deviation from the threshold.
        deviation = lineReflection - threshold
        # print("Deviation: ", deviation) # TODO: Log Parameter

        # Calculate the turn rate.
        turnRate = calibration.proportionalGain * deviation
        # print("Turn Rate: " + str(turnRate) + "\n") # TODO: Log Parameter

        # Set the drive base speed and turn rate.
        horn.robot.drive(-followingMovementSpeed, turnRate)

        if lineColor == Color.BLACK:
            horn.robot.stop()
            return

        # wait(1)


#! Multiple movements

# * Horn walks backwards a little, and rotates to point forwards
def walksBackwardsAndRotatesToPointForward(horn, calibration):
    followMainLineBackTime(horn, calibration, calibration.followingMovementSpeed, 2700)
    horn.ev3.speaker.beep()
    horn.robot.turn(calibratedTurn(170, calibration))


# * Horn walks forwards a little, and rotates to point backwards
def walksForwardsAndRotatesToPointBackward(horn, calibration):
    followMainLineTime(horn, calibration, calibration.followingMovementSpeed, 2200)
    horn.ev3.speaker.beep()
    horn.robot.turn(
        calibratedTurn(-170 * calibration.negativeTurnCalibration, calibration)
    )


# * Horn is pointing forward. Rotates, goes back to beginning, walks a little backwards, and rotates to point forward again.
def rotateAndGoToBeggining(horn, calibration, gameInfo):

    # print("End of the board reached, going back to the beginning.")
    walksForwardsAndRotatesToPointBackward(horn, calibration)
    horn.ev3.speaker.beep()
    followMainLineBackUntilEnemyLine(
        False, horn, calibration, gameInfo, calibration.followingMovementSpeed * 1.0, 1
    )
    # Doesn't need a beep because reaching the first enemy line in the last function beeps
    walksBackwardsAndRotatesToPointForward(horn, calibration)


# * Horn is on the enemy line. Goes backwards until the black tape and rotates back to the main line.
def goBackwardsAndRotate(horn, calibration):
    horn.robot.straight(
        -350
    )  # Doesn't stop after the straight, since it's going to keep going backwards anyways
    followEnemyLineBackUntilBlack(horn, calibration, calibration.followingMovementSpeed)
    horn.ev3.speaker.beep()
    horn.robot.turn(
        calibratedTurn(90 * calibration.negativeTurnCalibration, calibration)
    )
    horn.ev3.speaker.beep()


# * Horn crossed enemy line. Sets itself up by walking forward a little, and then rotates to the enemy line.
def setItselfAndRotate(horn, calibration):
    followMainLineTime(horn, calibration, calibration.followingMovementSpeed, 1200)
    horn.ev3.speaker.beep()
    horn.robot.turn(
        calibratedTurn(-120 * calibration.negativeTurnCalibration, calibration)
    )
    horn.ev3.speaker.beep()
