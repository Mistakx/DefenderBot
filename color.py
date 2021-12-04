from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, TouchSensor, ColorSensor
from pybricks.parameters import Port, Button, Color, ImageFile, SoundFile
from pybricks.tools import wait

def sayColor(ev3, enemyColorSensor):

    print("Color: ", enemyColorSensor.color())

    if enemyColorSensor.color() == Color.BLUE:
        ev3.speaker.say('blue')
    elif enemyColorSensor.color() == Color.GREEN:
        ev3.speaker.say('green')
    elif enemyColorSensor.color() == Color.YELLOW:
        ev3.speaker.say('yellow')
    elif enemyColorSensor.color() == Color.RED:
        ev3.speaker.say('red')