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
        
        if (gameInfo.hornEnergy == 500):
            print("Horn doesn't need to regain energy.\n")
            return False

        elif ( (gameInfo.hornEnergy < 500) and (gameInfo.usingRemainingEnergy == True) ):
            print("Horn is is using it's remaining energy to attack.\n")
            return False

        elif ( (gameInfo.hornEnergy < 500) and (usingRemainingEnergy.usingRemainingEnergy == False) ):
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

            gameInfo.usingRemainingEnergy = True

            print("There are 4 dead or out of attack enemies. Using remaining energy.")
            print("Checking if a crane attack is viable.")

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
            gameInfo.alreadyAttackedThisTurn = True
            horn.ev3.speaker.beep()
        
            movement.goBackwardsAndRotate(horn, calibration)
            gameInfo.currentPosition = tempEnemyArrayPosition + 1

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

        # Attacking with full energy
        if ( (numberOfArtilleriesReady >= 1) and (gameInfo.hornEnergy == 500) ):

            print("There are artilleries to attack. Attacking with full energy")

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
                gameInfo.alreadyAttackedThisTurn = True
                horn.ev3.speaker.beep()
            
                movement.goBackwardsAndRotate(horn, calibration)
                gameInfo.currentPosition = slotToAttack

        if ( (numberOfArtilleriesReady >= 1) and (gameInfo.hornEnergy > 0) and (gameInfo.usingRemainingEnergy) ):

            print("There are artilleries to attack. Attacking with remaining energy.")

            # Horn can do up to 3 sound attacks per turn and still regain full energy.
            # The artilleries need to be prioritized, and always sound attacked attacked, regardless of energy.
            # If Horn has energy to attack all artilleries, and still sound attack one or more enemies, it sound attacks them.
            numberOfAttacksToNonArtilleries = (gameInfo.hornEnergy/50) - numberOfArtilleriesReady # The number of non artilleries that can be sound attacked and still regain full energy
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
                gameInfo.alreadyAttackedThisTurn = True
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


        # Attack with full energy
        if ( (numberOfEnemies >= 2) and (gameInfo.hornEnergy == 500) ):

            print("There are 2 or more enemies to attack. Attacking with full energy.")
            
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
                        gameInfo.alreadyAttackedThisTurn = True
                        horn.ev3.speaker.beep()
                    
                        movement.goBackwardsAndRotate(horn, calibration)
                        gameInfo.currentPosition = i + 1

                    i += 1      

        # Attack with remaining energy
        if ( (numberOfEnemies >= 2) and (gameInfo.hornEnergy > 0) and (gameInfo.usingRemainingEnergy) ):

            print("There are 2 or more enemies to attack. Attacking with remaining energy.")
            
            while (gameInfo.hornEnergy > 0):


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
                        gameInfo.alreadyAttackedThisTurn = True
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

        #* Attack with full energy
        if ( (numberOfEnemies == 1) and (gameInfo.hornEnergy == 500) ):

            print("There is only 1 enemy. Attacking with full energy.")

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
                    gameInfo.alreadyAttackedThisTurn = True
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
                    print("Sound attacking slot " + str(i+1) + ".\n")

                    movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, i+1)
                    # horn.ev3.speaker.beep()
                    
                    movement.setItselfAndRotate(horn, calibration)
                    
                    #* horn.Robot follows the enemy line until the bottle
                    movement.followEnemyLineUntilBottle(False, False, horn, calibration, calibration.followingMovementSpeed)
                    attack.soundAttack(horn, gameInfo, i)
                    gameInfo.alreadyAttackedThisTurn = True
                    horn.ev3.speaker.beep()
                
                    movement.goBackwardsAndRotate(horn, calibration)
                    gameInfo.currentPosition = i + 1

                    return

                i += 1

        #* Attack with remaining energy
        elif ( (numberOfEnemies == 1) and (gameInfo.usingRemainingEnergy) ):

            print("There is only 1 enemy. Attacking with remaining energy.")

            # Attack one enemy with 100 or more health
            i = 0
            while (i < 6):

                currentEnemy = gameInfo.enemySlots[i]

                if ( enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["health"] >= 100) and (gameInfo.hornEnergy >= 150)):
                    print("The enemy has 100 or more health.")
                    print("Headbutting slot " + str(i+1) + ".")

                    movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, i+1)
                    # horn.ev3.speaker.beep()
                    
                    movement.setItselfAndRotate(horn, calibration)
                    
                    #* horn.Robot follows the enemy line until the bottle
                    movement.followEnemyLineUntilBottle(False, False, horn, calibration, calibration.followingMovementSpeed)
                    attack.headbutt(False, horn, calibration, gameInfo, i, calibration.followingMovementSpeed)
                    gameInfo.alreadyAttackedThisTurn = True
                    horn.ev3.speaker.beep()
                
                    movement.goBackwardsAndRotate(horn, calibration)
                    gameInfo.currentPosition = i + 1

                    return

                i += 1

            # Attack one enemy with 50 health
            i = 0
            while (i < 6):

                currentEnemy = gameInfo.enemySlots[i]

                if ( enemyIsAttackingNextTurn(gameInfo, i) and (currentEnemy["health"] == 50) and (gameInfo.hornEnergy >= 50) ):
                    
                    print("The enemy has 50 health.")
                    print("Sound attacking slot " + str(i+1) + ".\n")

                    movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, i+1)
                    # horn.ev3.speaker.beep()
                    
                    movement.setItselfAndRotate(horn, calibration)
                    
                    #* horn.Robot follows the enemy line until the bottle
                    movement.followEnemyLineUntilBottle(False, False, horn, calibration, calibration.followingMovementSpeed)
                    attack.soundAttack(horn, gameInfo, i)
                    gameInfo.alreadyAttackedThisTurn = True
                    horn.ev3.speaker.beep()
                
                    movement.goBackwardsAndRotate(horn, calibration)
                    gameInfo.currentPosition = i + 1

                    return

                i += 1


    if regainEnergyIfNecessary(gameInfo): return True
    gameInfo.alreadyAttackedThisTurn = False

    if (gameInfo.alreadyAttackedThisTurn == False):
        fourEnemiesKilled(horn, calibration, gameInfo) 
    if (gameInfo.alreadyAttackedThisTurn == False): 
        attackArtilleriesAndRemaining(horn, calibration, gameInfo)      
    if (gameInfo.alreadyAttackedThisTurn == False): 
        attackTwoOrMoreEnemies(horn, calibration, gameInfo)
    if (gameInfo.alreadyAttackedThisTurn == False):
        attackOneEnemy(horn, calibration, gameInfo)

    #! Counts the number of enemies dead or out of attacks
    numberOfDeadOrOutOfAttacksEnemies = 0
    i = 0
    while (i < 6):
        currentEnemy = gameInfo.enemySlots[i]
        if (currentEnemy == "Dead"):
            numberOfDeadAndOutOfAttacksEnemies += 1
        elif ( (currentEnemy != "") and (currentEnemy != "No bottle") and (currentEnemy["n_attacks"] == 0) ):
            numberOfDeadAndOutOfAttacksEnemies += 1
        
        i += 1

    if (numberOfDeadOrOutOfAttacksEnemies == 0):
        while True:
            horn.ev3.speaker.play_file(SoundFile.MAGIC_WAND)

#* Horn goes to the last enemy alive, with our without attacks, if it hasn't passed it yet
def goToLastEnemyAlive(horn, calibration, gameInfo):

    lastEnemyAliveArrayPosition = None
    i = 0
    #! Finds the last enemy alive array position
    while (i < 6):

        currentEnemy = gameInfo.enemySlots[i] 

        if ( (currentEnemy != "") and (currentEnemy != "Dead") and (currentEnemy != "No bottle")): # Only get attacked by valid slots
            lastEnemyAliveArrayPosition = i
        
        i += 1

    if (lastEnemyAliveArrayPosition != None):
        print("There are enemies alive, with or without attacks.")
        print("The last enemy alive is on slot: " + str(lastEnemyAliveArrayPosition+1) + ".\n")
        movement.followMainLineUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed, lastEnemyAliveArrayPosition+1)

    else:
        print("There isn't any enemy alive for Horn to be attacked.\n")

#* Horn skips dead enemies and slots with no bottles
#* Horn gets atacked by the enemies that can attack
#* Horn goes to enemies not dead but out of attacks, and says to the player that they have no attacks
def enemiesAttack(horn, calibration, gameInfo):

    i = 5

    while (i > 0):

        currentEnemy = gameInfo.enemySlots[i] 

        # Horn goes to all alive enemies, with or without attacks left
        if ( (currentEnemy != "") and (currentEnemy != "Dead") and (currentEnemy != "No bottle")): 

            #* Horn goes to the enemy slot that is going to attack
            movement.followMainLineBackUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed*1.0, i+1)
            horn.ev3.speaker.beep()


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

            #* After being attacked, horn stops, letting the timeout of the follow main line function to count the same line twice. Horn walks forwards to avoid it.
            movement.followMainLineTime(horn, calibration, calibration.followingMovementSpeed, 200)

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


        # #! Horn attacks
        #* Finds if there are enemies to attack
        thereAreEnemiesToAttack = False
        i = 0
        while (i < 6):

            currentEnemy = gameInfo.enemySlots[i] 

            if (enemyIsAttackingNextTurn(gameInfo, i)):
                thereAreEnemiesToAttack = True
                break
            
            i += 1

        if thereAreEnemiesToAttack:
            print("There are enemies to attack.")
            attackEnemies(horn, calibration, gameInfo)
        else:
            print("There are no enemies to attack.")











        #! Enemy attacks
        goToLastEnemyAlive(horn, calibration, gameInfo)
        movement.walksForwardsAndRotatesToPointBackward(horn, calibration)
        enemiesAttack(horn, calibration, gameInfo)
        movement.followMainLineBackUntilEnemyLine(False, horn, calibration, gameInfo, calibration.followingMovementSpeed, 1)
        movement.walksBackwardsAndRotatesToPointForward(horn, calibration)
        print(gameInfo.enemySlots)
        print()

    while True:
        horn.ev3.speaker.play_file(SoundFile.MAGIC_WAND)

