from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait

def sayColor(ev3, enemyColorSensor):

    # TODO: Exception if the color isn't one of the correct ones.
    # TODO: The yellow will probably be detected as brown sometimes. Implement correct behaviour.

    enemyColor = enemyColorSensor.color()
    print("Color reached: ", enemyColor)

    if enemyColor == Color.BLUE:
        #ev3.speaker.say('Blue')
        return Color.BLUE

    elif enemyColor == Color.GREEN:
        #ev3.speaker.say('Green')
        return Color.GREEN

    elif enemyColor == Color.YELLOW or enemyColor == Color.BROWN:
        #ev3.speaker.say('Yellow')
        return Color.YELLOW

    elif enemyColor == Color.RED:
        #ev3.speaker.say('Red')
        return Color.RED

    
