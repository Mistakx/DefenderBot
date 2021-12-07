from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import movement, calibration

def playGame(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360):

    enemyLinesPassed = 0

    #* Horn plays the game until reaching the final line
    while enemyLinesPassed < 6:

        movement.followMainLineUntilEnemyLine(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, enemyLineColor, proportionalGain, followingMovementSpeed*4)
        enemyLinesPassed += 1
        ev3.speaker.beep()
        
        print("Following main line. Enemy lines passed: ", enemyLinesPassed)

        #* Horn sets itself up, and rotates to the enemy line
        movement.followMainLineTime(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, proportionalGain, followingMovementSpeed, 2000)
        ev3.speaker.beep()
        robot.turn(movement.calibratedTurn(-130 * negativeTurnCalibration, turnCalibrationTo360)) # TODO
        ev3.speaker.beep()
        
        #* Robot follows the enemy line until the bottle
        movement.followEnemyLineUntilBottle(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed*4)
       
        #* Robot goes backwards until the black tape and rotates back to the main line
        ev3.speaker.beep()
        movement.followEnemyLineBackUntilTime(ev3, robot, lineColorSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, 1000)
        ev3.speaker.beep()
        movement.followEnemyLineBackUntilBlack(ev3, robot, lineColorSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed*4)
        ev3.speaker.beep()
        robot.turn(movement.calibratedTurn(90 * negativeTurnCalibration, turnCalibrationTo360))
        ev3.speaker.beep()

    # After reaching final enemy line, Horn rotates and goes back to the beginning
    print("End of the board reached, going back to the beginning.")
    movement.followMainLineTime(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, proportionalGain, followingMovementSpeed, 3000)
    ev3.speaker.beep()
    robot.turn(movement.calibratedTurn(-190, turnCalibrationTo360))
    ev3.speaker.beep()
    movement.goBackToFirstEnemyLine(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, enemyLineColor, proportionalGain, followingMovementSpeed*4)
    ev3.speaker.beep()
    movement.followMainLineTime(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, proportionalGain, followingMovementSpeed, 3000)
    ev3.speaker.beep()
    robot.turn(movement.calibratedTurn(180, turnCalibrationTo360))

