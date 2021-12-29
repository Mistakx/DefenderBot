from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random

import movement, calibration, attack

def recognizeBoard(enemySlots, ev3, robot, craneMotor, lineColorSensor, enemyColorSensor, distanceSensor, followingMovementSpeed, negativeTurnCalibration):

    enemyLinesPassed = 0

    #* Horn plays the game until reaching the final line
    while enemyLinesPassed < 6:

        movement.followMainLineUntilEnemyLine(False, ev3, robot, lineColorSensor, followingMovementSpeed*2)
        ev3.speaker.beep()
        
        print("Following main line. Enemy line reached: ", enemyLinesPassed)

        #* Horn sets itself up, and rotates to the enemy line
        movement.followMainLineTime(ev3, robot, lineColorSensor, followingMovementSpeed, 2000)
        ev3.speaker.beep()
        robot.turn(movement.calibratedTurn(-130 * negativeTurnCalibration))
        ev3.speaker.beep()
        
        #* Robot follows the enemy line until the bottle
        enemySlots[enemyLinesPassed] = movement.followEnemyLineUntilBottle(False, enemySlots, enemyLinesPassed, ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, followingMovementSpeed)
        if enemySlots[enemyLinesPassed] == "Error": 
            ev3.speaker.beep()
            print("Robot read invalid color, going back to try again.")
            robot.straight(-200)
            ev3.speaker.beep()
            enemySlots[enemyLinesPassed] = movement.followEnemyLineUntilBottle(False, enemySlots, enemyLinesPassed, ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, followingMovementSpeed)

        ev3.speaker.beep()
       
        #* Enemy attacks if it reached the bottle, or goes backwards if it reached the final black line
        if enemySlots[enemyLinesPassed] != "No bottle": # Enemy reached a bottle
            attackNumber = random.randint(1, 2)
            if attackNumber == 1:
                print("Crane Attack\n")
                attack.craneAttack(True, ev3, robot, craneMotor, lineColorSensor, distanceSensor, followingMovementSpeed, 150)
            elif attackNumber == 2:
                print("Headbutt Attack\n")
                attack.headbutt(True, ev3, robot, lineColorSensor, distanceSensor, followingMovementSpeed)
                ev3.speaker.beep()
                robot.straight(-200) # Doesn't stop after the straight, since it's going to keep going backwards anyways
            elif attackNumber == 3:
                attack.soundAttack(ev3)
        else: # Enemy didn't reach a bottle
            #movement.followEnemyLineBackUntilTime(ev3, robot, lineColorSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, 2000)
            robot.straight(-200) # Doesn't stop after the straight, since it's going to keep going backwards anyways
        ev3.speaker.beep()
            
        #* Robot goes backwards until the black tape and rotates back to the main line 
        movement.followEnemyLineBackUntilBlack(ev3, robot, lineColorSensor, followingMovementSpeed)
        ev3.speaker.beep()
        robot.turn(movement.calibratedTurn(80 * negativeTurnCalibration))
        ev3.speaker.beep()
        enemyLinesPassed += 1


    # After reaching final enemy line, Horn rotates and goes back to the beginning
    print("End of the board reached, going back to the beginning.")
    movement.followMainLineTime(ev3, robot, lineColorSensor, followingMovementSpeed, 3000)
    ev3.speaker.beep()
    robot.turn(movement.calibratedTurn(-190))
    ev3.speaker.beep()
    movement.goBackToFirstEnemyLine(ev3, robot, lineColorSensor, followingMovementSpeed*2)
    # Doesn't need a beep because reaching the first enemy line in the last function beeps
    movement.goBackTime(ev3, robot, lineColorSensor, followingMovementSpeed, 4000)
    ev3.speaker.beep()
    robot.turn(movement.calibratedTurn(180))
