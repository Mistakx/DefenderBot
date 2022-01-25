from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import random

import movement, calibration, attack

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


#* Horn recognizes the necessary board slots, and saves the enemies to the corresponding slots
def recognizeBoard(horn, calibration, gameInfo):

    i = 0

    while i < 6:

        if ( (gameInfo.enemySlots[i] == "") and (gameInfo.enemySlots[i] != "Dead") ): # Only recognize valid slots
           
            print("Slot "+ str(i+1) + " needs to be recognized.\n")
            movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*2, i+1)
            # horn.ev3.speaker.beep()
            
            #* Horn sets itself up, and rotates to the enemy line
            movement.followMainLineTime(horn, calibration, calibration.followingMovementSpeed, 2000)
            horn.ev3.speaker.beep()
            horn.robot.turn(movement.calibratedTurn(-130 * calibration.negativeTurnCalibration, calibration))
            horn.ev3.speaker.beep()
            
            #* horn.Robot follows the enemy line until the bottle
            gameInfo.enemySlots[i] = movement.followEnemyLineUntilBottle(False, horn, calibration, calibration.followingMovementSpeed)
            if gameInfo.enemySlots[i] == "Error": 
                horn.ev3.speaker.beep()
                print("Recognition: Horn read invalid color, going back to try again.")
                horn.ev3.speaker.say("INVALID COLOR, REPOSITION BOTTLE")
                wait(1000) # Waits for player to reposition bottle
                horn.robot.straight(-200)
                horn.ev3.speaker.beep()
                gameInfo.enemySlots[i] = movement.followEnemyLineUntilBottle(False, horn, calibration, calibration.followingMovementSpeed)
                if gameInfo.enemySlots[i] == "Error": # After reading bottle again, if it is still invalid, treat it as artillery
                    print("Recognition: Enemy still invalid. Treating it as Artillery.")
                    gameInfo.enemySlots[i] = {
                    "type": "Artillery",
                    "strenght": 500,
                    "n_attacks": 1,
                    "health": 50,
                    "positioned_this_turn": True
                    }
            horn.ev3.speaker.beep()
        
            #* horn.Robot goes backwards until the black tape and rotates back to the main line 
            horn.robot.straight(-200) # Doesn't stop after the straight, since it's going to keep going backwards anyways
            movement.followEnemyLineBackUntilBlack(horn, calibration, calibration.followingMovementSpeed)
            horn.ev3.speaker.beep()
            horn.robot.turn(movement.calibratedTurn(80 * calibration.negativeTurnCalibration, calibration))
            horn.ev3.speaker.beep()
            gameInfo.currentPosition = i + 1

        i+= 1

#* Horn regains 50% of it's current energy, never exceeding 500
def regainEnergy(horn, gameInfo):

    print("Regaining Energy")

    horn.ev3.speaker.play_file(SoundFile.READY)
    
    gameInfo.hornEnergy = gameInfo.hornEnergy + 0.5 * gameInfo.hornEnergy
    if gameInfo.hornEnergy > 500:
        gameInfo.hornEnergy = 500

    print("Horn Energy:", gameInfo.hornEnergy)
    
#* Horn attacks the enemies according to the defined heuristics
def attackEnemies(horn, calibration, gameInfo):

    def attackArtilleries(horn, calibration, gameInfo):

        i = 0

        while (i < 6):
            
            if (gameInfo.enemySlots[i] != "") and (gameInfo.enemySlots[i] != "Dead"):

                if (gameInfo.enemySlots[i])["type"] == "Artillery":
                        
                    print("Slot "+ str(i + 1) + " has artillery so it needs to be attacked.\n")
                
                    movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*2, i+1)
                    # horn.ev3.speaker.beep()
                    
                    #* Horn sets itself up, and rotates to the enemy line
                    movement.followMainLineTime(horn, calibration, calibration.followingMovementSpeed, 2000)
                    horn.ev3.speaker.beep()
                    horn.robot.turn(movement.calibratedTurn(-130 * calibration.negativeTurnCalibration, calibration))
                    horn.ev3.speaker.beep()
                    
                    #* horn.Robot follows the enemy line until the bottle
                    movement.followEnemyLineUntilBottle(False, horn, calibration, calibration.followingMovementSpeed)
                    attack.soundAttack(horn, gameInfo, i)
                    horn.ev3.speaker.beep()
                
                    #* horn.Robot goes backwards until the black tape and rotates back to the main line 
                    horn.robot.straight(-200) # Doesn't stop after the straight, since it's going to keep going backwards anyways
                    movement.followEnemyLineBackUntilBlack(horn, calibration, calibration.followingMovementSpeed)
                    horn.ev3.speaker.beep()
                    horn.robot.turn(movement.calibratedTurn(80 * calibration.negativeTurnCalibration, calibration))
                    horn.ev3.speaker.beep()
                    gameInfo.currentPosition = i + 1

            i = i + 1

    attackArtilleries(horn, calibration, gameInfo)      

#* Horn gets atacked by the enemies
def enemiesAttack(horn, calibration, gameInfo):
    
    i = 0

    while i < 6:

        if ( (gameInfo.enemySlots[i] != "") and (gameInfo.enemySlots[i] != "Dead") ): # Only get attacked by valid slots
           
            #* Horn goes to the enemy line that is going to attack
            movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*2, i+1)
            # horn.ev3.speaker.beep()

            #* Horn gets attacked
            # TODO: Different sound for each enemy
            if (gameInfo.enemySlots[i])["n_attacks"] > 0:
                gameInfo.hornHealth = gameInfo.hornHealth - (gameInfo.enemySlots[i])["strenght"]
                (gameInfo.enemySlots[i])["n_attacks"] = (gameInfo.enemySlots[i])["n_attacks"] - 1
                horn.ev3.speaker.say("Horn was attacked.")
            else:
                horn.ev3.speaker.say("Enemy is out of attacks.")

            print("Horn Health:", gameInfo.hornHealth)
            # horn.robot.straight(200)

        
        i = i + 1



            

    return

#* Horn plays the game
def playGame(horn, calibration, gameInfo):

    #! Energy regain
    regainEnergy(horn, gameInfo)
    print("Horn Health:", gameInfo.hornHealth)
    print()

    #! Board recognition
    #* If all enemies are enemies dead, scanned already, or a mixture of the two, then Horn doesn't need to recognize the board.
    boardNeedsRecognition = False
    i = 0
    while i < 6:
        if (gameInfo.enemySlots[i] == ""):
            boardNeedsRecognition = True
        i = i + 1

    if boardNeedsRecognition:
        recognizeBoard(horn, calibration, gameInfo)
        movement.rotateAndGoToBeggining(horn, calibration, gameInfo)
    print(gameInfo.enemySlots)

    #! Horn attacks
    attackEnemies(horn, calibration, gameInfo)
    movement.rotateAndGoToBeggining(horn, calibration, gameInfo)
    print(gameInfo.enemySlots)

    #! Enemy attacks
    enemiesAttack(horn, calibration, gameInfo)
