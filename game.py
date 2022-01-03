from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random

import movement, calibration, attack

#! Game state
hornHealth = 750
hornEnergy = 500
enemySlots = ["","","","","",""]

#! Heuristics
# Optimum energy point - 333 energy at the end of the turn.
# Life can surpass 750, is worth less than energy

# Artillery (500 dmg, 50 hp):
#   Sound (50 energy)
#   Ratio: 10 Energy/HP
#   Always attack

# Infantry (300 dmg, 50 hp):
#   2 Sound (50 energy, 50 energy and 50 hp)
#   Headbutt (150 energy)
#   Ratio: 2

# Tank (400 dmg, 200hp)
#   Crane (300 energy)
#   Two Headbutt (150 energy, 150 energy and 50hp)
#   Ratio: 1.33

# Cure 1 - Ratio 0.5
# Cure 2 - Ratio 0.66
# Cure 3 - Ratio 1

# Scenarios
#* 6 Infantry: 
# 3 Sounds, 300 + 150 damage

# Worst case scenario: 6 tanks - 

def recognizeBoard(horn, calibration):

    enemyLinesPassed = 0

    #* Horn plays the game until reaching the final line
    while enemyLinesPassed < 6:

        movement.followMainLineUntilNextEnemyLine(False, horn, calibration, calibration.followingMovementSpeed*2)
        horn.ev3.speaker.beep()
        
        print("Following main line. Enemy line reached: ", enemyLinesPassed)

        #* Horn sets itself up, and rotates to the enemy line
        movement.followMainLineTime(horn, calibration, calibration.followingMovementSpeed, 2000)
        horn.ev3.speaker.beep()
        horn.robot.turn(movement.calibratedTurn(-130 * calibration.negativeTurnCalibration, calibration))
        horn.ev3.speaker.beep()
        
        #* horn.Robot follows the enemy line until the bottle
        enemySlots[enemyLinesPassed] = movement.followEnemyLineUntilBottle(False, horn, calibration, calibration.followingMovementSpeed)
        if enemySlots[enemyLinesPassed] == "Error": 
            horn.ev3.speaker.beep()
            print("horn.Robot read invalid color, going back to try again.")
            horn.robot.straight(-200)
            horn.ev3.speaker.beep()
            enemySlots[enemyLinesPassed] = movement.followEnemyLineUntilBottle(False, horn, calibration, calibration.followingMovementSpeed)

        horn.ev3.speaker.beep()
       
        #* Enemy attacks if it reached the bottle, or goes backwards if it reached the final black line
        if enemySlots[enemyLinesPassed] != "No bottle": # Enemy reached a bottle
            attackNumber = random.randint(1, 2)
            if attackNumber == 1:
                print("Crane Attack\n")
                attack.craneAttack(True, horn, calibration, calibration.followingMovementSpeed, 150)
            elif attackNumber == 2:
                print("Headbutt Attack\n")
                attack.headbutt(True, horn, calibration, calibration.followingMovementSpeed)
                horn.ev3.speaker.beep()
                horn.robot.straight(-200) # Doesn't stop after the straight, since it's going to keep going backwards anyways
            elif attackNumber == 3:
                attack.soundAttack(horn.ev3)
        else: # Enemy didn't reach a bottle
            #movement.followEnemyLineBackUntilTime(horn.ev3, horn.robot, horn.lineColorSensor, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, calibration.followingMovementSpeed, 2000)
            horn.robot.straight(-200) # Doesn't stop after the straight, since it's going to keep going backwards anyways
        horn.ev3.speaker.beep()
            
        #* horn.Robot goes backwards until the black tape and rotates back to the main line 
        movement.followEnemyLineBackUntilBlack(horn, calibration, calibration.followingMovementSpeed)
        horn.ev3.speaker.beep()
        horn.robot.turn(movement.calibratedTurn(80 * calibration.negativeTurnCalibration, calibration))
        horn.ev3.speaker.beep()
        enemyLinesPassed += 1


    # After reaching final enemy line, Horn rotates and goes back to the beginning
    print("End of the board reached, going back to the beginning.")
    movement.followMainLineTime(horn, calibration, calibration.followingMovementSpeed, 3000)
    horn.ev3.speaker.beep()
    horn.robot.turn(movement.calibratedTurn(-190, calibration))
    horn.ev3.speaker.beep()
    movement.goBackToFirstEnemyLine(horn, calibration, calibration.followingMovementSpeed*2)
    # Doesn't need a beep because reaching the first enemy line in the last function beeps
    movement.goBackTime(horn, calibration, calibration.followingMovementSpeed, 4000)
    horn.ev3.speaker.beep()
    horn.robot.turn(movement.calibratedTurn(180, calibration))

    print(enemySlots)


def beginTurn(horn, calibration):
    
    #* Regain energy
    hornEnergy = hornEnergy + 0.5 * hornEnergy
    if hornEnergy > 500:
        hornEnergy = 500
    