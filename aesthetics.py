#!/usr/bin/env pybricks-micropython
from threading import Thread

from pybricks.ev3devices import (
    ColorSensor,
    GyroSensor,
    InfraredSensor,
    Motor,
    TouchSensor,
    UltrasonicSensor,
)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

import sound


def logo(horn):
    while True:
        horn.ev3.screen.load_image("horn39.png")
        wait(100)
        horn.ev3.screen.load_image("horn55.png")
        wait(100)


def light(horn):
    while True:
        horn.ev3.light.on(Color.RED)
        wait(100)
        horn.ev3.light.on(Color.GREEN)
        wait(100)

def turnHornAndCrane(horn):
    horn.robot.settings(1000, 1000, 1000, 1000)
    horn.craneMotor.run(2000)
    horn.robot.turn(100000)

def celebration(horn):
    sound_thread = Thread(target=sound.tokio, args=(horn,))
    sound_thread.start()
    # turn_thread = Thread(target=turnHornAndCrane, args=(horn,))
    # turn_thread.start()



