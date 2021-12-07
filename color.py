from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait

def sayColor(ev3, enemyColorSensor):

    print("Color: ", enemyColorSensor.color())

    if enemyColorSensor.color() == Color.BLUE:
        ev3.speaker.say('Blue')
    elif enemyColorSensor.color() == Color.GREEN:
        ev3.speaker.say('Green')
    elif enemyColorSensor.color() == Color.YELLOW:
        ev3.speaker.say('Yellow')
    elif enemyColorSensor.color() == Color.RED:
        ev3.speaker.say('Red')