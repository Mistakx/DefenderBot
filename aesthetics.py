#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread

import movement, calibration, game, attacks, sound, aesthetics

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
