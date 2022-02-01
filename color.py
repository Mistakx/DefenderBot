from pybricks.ev3devices import ColorSensor, Motor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button, Color, ImageFile, Port, SoundFile
from pybricks.tools import wait


def identifyEnemy(printEnemyInfo, ev3, enemyColorSensor):

    # TODO: Exception if the color isn't one of the correct ones.

    enemyColor = enemyColorSensor.color()
    
    if printEnemyInfo:
        print("Color reached: ", enemyColor)

    if enemyColor == Color.BLUE: # Error
        #ev3.speaker.say('Blue')
        return "Error"

    elif enemyColor == Color.GREEN or enemyColor == Color.WHITE: # Infantry
        #ev3.speaker.say('Green')
        infantry = {
            "type": "Infantry",
            # "strength": 100,
            "n_attacks": 3,
            "health": 100,
            # "positioned_this_turn": True
        }
        return infantry

    elif enemyColor == Color.YELLOW or enemyColor == Color.BROWN: # Artillery
        #ev3.speaker.say('Yellow')
        artillery = {
            "type": "Artillery",
            "strength": 500,
            "n_attacks": 1,
            "health": 50,
            # "positioned_this_turn": True
        }
        return artillery

    elif enemyColor == Color.RED: # Tank
        #ev3.speaker.say('Red')
        tank = {
            "type": "Tank",
            # "strength": 200,
            "n_attacks": 2,
            "health": 200,
            # "positioned_this_turn": True
        }
        return tank

    elif enemyColor == Color.BLACK: # Error
        #ev3.speaker.say('Blue')
        return "Error"

    else:
        return "Error"

    
