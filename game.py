# cesar.dias@olx.com
# Stand virtual, Imo virtual, Propria OLX
import random

from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

import attack
import calibration
import movement

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

#* There is still an enemy attacking next turn
def enemyIsAttackingNextTurn(gameInfo, enemyArrayPosition):
    enemy = gameInfo.enemySlots[enemyArrayPosition]
    return ( (enemy != "") and (enemy != "No bottle") and (enemy != "Dead") and (enemy["n_attacks"] > 0) )

#* Checks if the game isn't over
def gameIsStillOn(gameInfo):
    
    gameInfo.currentTurn += 1

    if (gameInfo.currentTurn <= 6):

        print("Current turn: " + str(gameInfo.currentTurn))

        gameIsStillOn = False

        i = 0

        while (i < 6):

            currentEnemy = gameInfo.enemySlots[i]

            if ( (currentEnemy == "") or (currentEnemy == "No bottle") ): # Slot still hasn't had enemy, so the game is still on
                gameIsStillOn = True

            elif enemyIsAttackingNextTurn(gameInfo, i):
                gameIsStillOn = True

            i += 1

        return gameIsStillOn

    return False

#* Horn recognizes the necessary board slots, and saves the enemies to the corresponding slots
def recognizeBoard(horn, calibration, gameInfo):

    i = 0

    while (i < 6):
        
        currentEnemy = gameInfo.enemySlots[i]

        if ( (currentEnemy == "") or (currentEnemy == "No bottle") ): # Only recognize valid slots
           
            print("Slot "+ str(i+1) + " needs to be recognized.\n")
            movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, i+1)
            # horn.ev3.speaker.beep()
            
            movement.setItselfAndRotate(horn, calibration)
            
            #* horn.Robot follows the enemy line until the bottle
            gameInfo.enemySlots[i] = movement.followEnemyLineUntilBottle(False, True, horn, calibration, calibration.followingMovementSpeed)
            if gameInfo.enemySlots[i] == "Error": 
                horn.ev3.speaker.beep()
                print("Recognition: Horn read invalid color, going back to try again.")
                horn.ev3.speaker.say("INVALID COLOR, REPOSITION BOTTLE")
                wait(1000) # Waits for player to reposition bottle
                horn.robot.straight(-200)
                horn.ev3.speaker.beep()
                gameInfo.enemySlots[i] = movement.followEnemyLineUntilBottle(False, True, horn, calibration, calibration.followingMovementSpeed)
                if gameInfo.enemySlots[i] == "Error": # After reading bottle again, if it is still invalid, treat it as artillery
                    print("Recognition: Enemy still invalid. Treating it as Artillery.")
                    gameInfo.enemySlots[i] = {
                    "type": "Artillery",
                    "strength": 500,
                    "n_attacks": 1,
                    "health": 50,
                    # "positioned_this_turn": True
                    }
            horn.ev3.speaker.beep()
        
            movement.goBackwardsAndRotate(horn, calibration)
            gameInfo.currentPosition = i + 1

        i+= 1

#* Horn regains 50% of it's current energy, never exceeding 500
def regainEnergy(horn, gameInfo):

    print("Regaining energy.")

    horn.ev3.speaker.play_file(SoundFile.READY)
    
    gameInfo.hornEnergy = gameInfo.hornEnergy + 0.5 * gameInfo.hornEnergy
    if gameInfo.hornEnergy > 500:
        gameInfo.hornEnergy = 500

    print("Horn Energy:", gameInfo.hornEnergy)
    
#* Horn attacks the enemies according to the defined heuristics
def attackEnemies(horn, calibration, gameInfo):

    # Detects if Horn needs to skip it's turn to regain energy 
    def regainEnergyIfNecessary(gameInfo):
        
        if gameInfo.hornEnergy == 500:
            print("Horn doesn't need to regain energy.\n")
            return False

        elif gameInfo.hornEnergy < 500:
            print("Horn is skipping it's turn to regain energy.\n")
            return True

    # If 4 enemies were killed or are out of attacks, crane attack the enemy on the board with more health
    def fourEnemiesKilled(horn, calibration, gameInfo):


        # Counts the number of dead enemies
        numberOfDeadEnemies = 0
        i = 0
        while (i < 6):
            currentEnemy = gameInfo.enemySlots[i]
            if (currentEnemy == "Dead"):
                numberOfDeadEnemies += 1
            i += 1


        # Counts the number of enemies out of attacks
        numberOfEnemiesOutOfAttacks = 0
        i = 0
        while (i < 6):
            currentEnemy = gameInfo.enemySlots[i]
            if ( (currentEnemy != "Dead") and (currentEnemy != "") and (currentEnemy != "No bottle") and (currentEnemy["n_attacks"] == 0) ):
                numberOfEnemiesOutOfAttacks += 1
            i += 1


        # Counts the number of enemies that are attacking next turn
        numberOfEnemiesAttackingNextTurn = 0
        i = 0
        while (i < 6):
            currentEnemy = gameInfo.enemySlots[i]
            if (enemyIsAttackingNextTurn(gameInfo, i)):
                numberOfEnemiesAttackingNextTurn += 1
            i += 1


        #! If 4 enemies were killed or are out of attacks, crane attack the enemy on the board with more health if the board doesn't have two enemies with 50 health
        if ( ((numberOfDeadEnemies + numberOfEnemiesOutOfAttacks) >= 4) and (numberOfEnemiesAttackingNextTurn >= 1) ):

            print("There are 4 dead or out of attack enemies. Checking if a crane attack is viable.")

            # Counts the number of enemies alive that have 50 health
            numberOfEnemiesAttackingNextTurnWith50Health = 0
            i = 0
            while (i < 6):
                currentEnemy = gameInfo.enemySlots[i]
                if (enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["health"] == 50)):
                    numberOfEnemiesAttackingNextTurnWith50Health += 1
                i += 1

            #! If two enemies are attacking next turn and both have 50 life, Horn doesn't use the crane attack
            #! Using the crane attack in this situation would leave one of the enemies alive
            if (numberOfEnemiesAttackingNextTurnWith50Health == 2):
                print("There are 2 remaining enemies alive, but both have 50 health. Not using crane attack.")
                return

            i = 0
            tempEnemyHealth = 0
            tempEnemyArrayPosition = 0
            
            # Changes temp variables to the variables corresponding to the enemy attacking next turn with more health
            while (i < 6):

                currentEnemy = gameInfo.enemySlots[i]

                if ( enemyIsAttackingNextTurn(gameInfo, i) and currentEnemy["health"] > tempEnemyHealth):
                    tempEnemyHealth = currentEnemy["health"]
                    tempEnemyArrayPosition = i

                i += 1

            print("Crane attacking remaining slot " + str(tempEnemyArrayPosition + 1) + ".\n")

            movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, tempEnemyArrayPosition + 1)
            # horn.ev3.speaker.beep()
            
            movement.setItselfAndRotate(horn, calibration)
            
            #* Horn follows the enemy line until the bottle
            movement.followEnemyLineUntilBottle(False, False, horn, calibration, calibration.followingMovementSpeed)
            attack.craneAttack(False, horn, calibration, gameInfo, tempEnemyArrayPosition, calibration.followingMovementSpeed, 150)
            horn.ev3.speaker.beep()
        
            movement.goBackwardsAndRotate(horn, calibration)
            gameInfo.currentPosition = tempEnemyArrayPosition + 1
            
            return

    # If there are artilleries, sound attack them, and use the remaining energy to sound attack the remaining enemies
    def attackArtilleriesAndRemaining(horn, calibration, gameInfo):

        #! Counts the number of artilleries
        numberOfArtilleriesReady = 0
        i = 0
        while (i < 6):
            currentEnemy = gameInfo.enemySlots[i]
            if ( enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["type"] == "Artillery") ):
                numberOfArtilleriesReady += 1
            i += 1


        #! Counts the number of non artilleries
        numberOfNonArtilleriesReady = 0
        i = 0
        while (i < 6):
            currentEnemy = gameInfo.enemySlots[i]
            if ( enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["type"] == "Infantry") ):
                numberOfNonArtilleriesReady += 1
            elif ( enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["type"] == "Tank") ):
                numberOfNonArtilleriesReady += 1
            i += 1


        #! There are artilleries to attack this turn
        if (numberOfArtilleriesReady >= 1):

            print("There are artilleries to attack.")

            # Horn can do up to 3 sound attacks per turn and still regain full energy.
            # The artilleries need to be prioritized, and always sound attacked attacked, regardless of energy.
            # If Horn has energy to attack all artilleries, and still sound attack one or more enemies, it sound attacks them.
            numberOfAttacksToNonArtilleries = 3 - numberOfArtilleriesReady # The number of non artilleries that can be sound attacked and still regain full energy
            numberOfNonArtilleriesAddedToArray = 0 # The number of non artilleries queued to be attacked the same turn as the artilleries 
            slotsToSoundAttack = []


            #! Add non artilleries to be attacked to the array
            i = 0

            # Add to the array while:
            # Number of non artilleries added hasn't reached the number of attacks possible
            # Number of non artilleries added hasn't reached the number of total non artilleries in the board
            # TODO: Verify
            while ( (numberOfNonArtilleriesAddedToArray < numberOfAttacksToNonArtilleries) and (numberOfNonArtilleriesAddedToArray < numberOfNonArtilleriesReady) ):
                currentEnemy = gameInfo.enemySlots[i]
                if ( enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["type"] != "Artillery") ):
                    # slotsToSoundAttack[numberOfNonArtilleriesAddedToArray] = i + 1
                    slotsToSoundAttack.append(i+1)
                    print("Non Artillery queued to be attacked. Slot: " + str(i +1))
                    numberOfNonArtilleriesAddedToArray += 1

                i += 1

            
            #! Added artilleries to be attacked to the array
            i = 0
            currentArrayIndex = numberOfNonArtilleriesAddedToArray
            while (i < 6):

                currentEnemy = gameInfo.enemySlots[i]

                if (enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["type"] == "Artillery") ):
                    # slotsToSoundAttack[currentArrayIndex] = i + 1
                    slotsToSoundAttack.append(i+1)
                    print("Artillery queued to be attacked. Slot: " + str(i +1))
                    currentArrayIndex += 1
                
                i += 1

            print() # Space after the last artillery queued print

            #! Sort the array that contains the slots to attack, so they are attacked in the correct order
            slotsToSoundAttack.sort()


            #! Sound attack the queued enemies
            for slotToAttack in slotsToSoundAttack:
                
                movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, slotToAttack)
                # horn.ev3.speaker.beep()
                
                movement.setItselfAndRotate(horn, calibration)
                
                #* horn.Robot follows the enemy line until the bottle
                movement.followEnemyLineUntilBottle(False, False, horn, calibration, calibration.followingMovementSpeed)
                attack.soundAttack(horn, gameInfo, slotToAttack - 1)
                horn.ev3.speaker.beep()
            
                movement.goBackwardsAndRotate(horn, calibration)
                gameInfo.currentPosition = slotToAttack

    # If there are 2 or more enemies, sound attack them until energy reaches 350
    def attackTwoOrMoreEnemies(horn, calibration, gameInfo):

        #! Counts the number of enemies
        numberOfEnemies = 0
        i = 0
        while (i < 6):
            currentEnemy = gameInfo.enemySlots[i]
            if (enemyIsAttackingNextTurn(gameInfo, i)):
                numberOfEnemies += 1
            i += 1

        if (numberOfEnemies >= 2):

            print("There are 2 or more enemies to attack.")

            while (gameInfo.hornEnergy > 350):


                i = 0
                while (i < 6):

                    currentEnemy = gameInfo.enemySlots[i]

                    if ( enemyIsAttackingNextTurn(gameInfo, i) ):
        
                        movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, i+1)
                        # horn.ev3.speaker.beep()
                        
                        movement.setItselfAndRotate(horn, calibration)
                        
                        #* Horn follows the enemy line until the bottle
                        movement.followEnemyLineUntilBottle(False, False, horn, calibration, calibration.followingMovementSpeed)
                        attack.soundAttack(horn, gameInfo, i)
                        horn.ev3.speaker.beep()
                    
                        movement.goBackwardsAndRotate(horn, calibration)
                        gameInfo.currentPosition = i + 1

                    i += 1      

    # Attack an enemy if non of the other conditions apply
    def attackOneEnemy(horn, calibration, gameInfo):

        #! Counts the number of enemies
        numberOfEnemies = 0
        i = 0
        while (i < 6):
            currentEnemy = gameInfo.enemySlots[i]
            if (enemyIsAttackingNextTurn(gameInfo, i)):
                numberOfEnemies += 1
            i += 1

        if (numberOfEnemies == 1):

            print("There is only 1 enemy.")

            # Attack one enemy with 100 or more health
            i = 0
            while (i < 6):

                currentEnemy = gameInfo.enemySlots[i]

                if ( enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["health"] >= 100) ):
                    print("The enemy has 100 or more health.")
                    print("Headbutting slot " + str(i+1) + ".")

                    movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, i+1)
                    # horn.ev3.speaker.beep()
                    
                    movement.setItselfAndRotate(horn, calibration)
                    
                    #* horn.Robot follows the enemy line until the bottle
                    movement.followEnemyLineUntilBottle(False, False, horn, calibration, calibration.followingMovementSpeed)
                    attack.headbutt(False, horn, calibration, gameInfo, i, calibration.followingMovementSpeed)
                    horn.ev3.speaker.beep()
                
                    movement.goBackwardsAndRotate(horn, calibration)
                    gameInfo.currentPosition = i + 1

                    return

                i += 1

            # Attack one enemy with 50 health
            i = 0
            while (i < 6):

                currentEnemy = gameInfo.enemySlots[i]

                if ( enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["health"] == 50) ):
                    
                    print("The enemy has 50 health.")
                    print("Sound attacking slot " + str(i+1) + ".")

                    movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, i+1)
                    # horn.ev3.speaker.beep()
                    
                    movement.setItselfAndRotate(horn, calibration)
                    
                    #* horn.Robot follows the enemy line until the bottle
                    movement.followEnemyLineUntilBottle(False, False, horn, calibration, calibration.followingMovementSpeed)
                    attack.soundAttack(horn, gameInfo, i)
                    horn.ev3.speaker.beep()
                
                    movement.goBackwardsAndRotate(horn, calibration)
                    gameInfo.currentPosition = i + 1

                    return

                i += 1


    if regainEnergyIfNecessary(gameInfo): return True

    fourEnemiesKilled(horn, calibration, gameInfo)
    attackArtilleriesAndRemaining(horn, calibration, gameInfo)      
    attackTwoOrMoreEnemies(horn, calibration, gameInfo)
    attackOneEnemy(horn, calibration, gameInfo)

#* Horn skips dead enemies and slots with no bottles
#* Horn gets atacked by the enemies that can attack
#* Horn goes to enemies not dead but out of attacks and says to the player
def enemiesAttack(horn, calibration, gameInfo):

    i = 6

    while (i > 0):

        currentEnemy = gameInfo.enemySlots[i] 

        if ( (currentEnemy != "") and (currentEnemy != "Dead") and (currentEnemy != "No bottle")): # Only get attacked by valid slots
           
            #* Horn goes to the enemy line that is going to attack
            movement.goBackToEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, i+1)
            # horn.ev3.speaker.beep()

            #* Horn gets attacked
            # TODO: Different sound for each enemy
            if currentEnemy["n_attacks"] > 0:

                # Infantry gives as much damage as its health
                if (currentEnemy["type"] == "Infantry"):

                    gameInfo.hornHealth = gameInfo.hornHealth - currentEnemy["health"]
                    currentEnemy["n_attacks"] = currentEnemy["n_attacks"] - 1
                    horn.ev3.speaker.play_file("./sounds/infantry.rsf")

                # Tank gives as much damage as its health
                if (currentEnemy["type"] == "Tank"):
                    gameInfo.hornHealth = gameInfo.hornHealth - currentEnemy["health"]
                    currentEnemy["n_attacks"] = currentEnemy["n_attacks"] - 1
                    horn.ev3.speaker.play_file("./sounds/tank.rsf")

                # If artillery attacks, it always gives 500 damage
                elif currentEnemy["type"] == "Artillery":
                    gameInfo.hornHealth = gameInfo.hornHealth - 500
                    currentEnemy["n_attacks"] = currentEnemy["n_attacks"] - 1
                    horn.ev3.speaker.play_file(SoundFile.SONAR)
                    horn.ev3.speaker.play_file("./sounds/artillery.rsf")

            else:
                horn.ev3.speaker.say("Enemy is out of attacks.")

            print("Horn Health:", gameInfo.hornHealth)
            print()
            if (gameInfo.hornHealth <= 0):
                horn.ev3.speaker.play_file("./sounds/gameOver.rsf")
                while True:
                    horn.ev3.light.on(Color.RED)
                    wait(100)
                    horn.ev3.light.on(Color.GREEN)
                    wait(100)
        
        i -= 1

    return

#! Horn plays the game
def playGame(horn, calibration, gameInfo):

    while gameIsStillOn(gameInfo):

        #! Energy regain
        regainEnergy(horn, gameInfo)
        print("Horn Health:", gameInfo.hornHealth)
        print()

        #! Board recognition
        #* If all enemies are enemies dead, scanned already, or a mixture of the two, then Horn doesn't need to recognize the board.
        boardNeedsRecognition = False
        i = 0
        while (i < 6):
            currentEnemy = gameInfo.enemySlots[i]
            if ( (currentEnemy == "") or (currentEnemy == "No bottle") ):
                boardNeedsRecognition = True
            i = i + 1

        if boardNeedsRecognition:
            print("Board needs recognition.")
            recognizeBoard(horn, calibration, gameInfo)
            print(gameInfo.enemySlots)
            print()
            movement.rotateAndGoToBeggining(horn, calibration, gameInfo)
        else:
            print("Board doesn't need recognition.")

        #! Horn attacks
        attackEnemies(horn, calibration, gameInfo)
        movement.walksForwardsAndRotatesToPointBackward(horn, calibration)
        # print(gameInfo.enemySlots)
        # print()

        #! Enemy attacks
        enemiesAttack(horn, calibration, gameInfo)
        movement.walksBackwardsAndRotatesToPointForward(horn, calibration)
        print(gameInfo.enemySlots)
        print()

    while True:
        horn.ev3.speaker.play_file(SoundFile.MAGIC_WAND)
