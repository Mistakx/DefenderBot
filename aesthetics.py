#!/usr/bin/env pybricks-micropython
from threading import Thread

from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

import sound


def logo(ev3):
    while True:
        ev3.screen.load_image("horn39.png")
        wait(100)
        ev3.screen.load_image("horn55.png")
        wait(100)

def light(ev3):
    while True:
        ev3.light.on(Color.RED)
        wait(100)
        ev3.light.on(Color.GREEN)
        wait(100)

def celebration(ev3, robot):
    return
