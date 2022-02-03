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
    horn.craneMotor.run_angle(400, 325000, then=Stop.HOLD, wait=False)
    horn.leftMotor.run(150)
    horn.rightMotor.run(-150)
    horn.ev3.speaker.set_volume(10000, which='_all_')
    horn.ev3.speaker.play_file("./tokio/primeiro.rsf")
    horn.ev3.speaker.play_file("./tokio/segundo.rsf")
    horn.ev3.speaker.play_file("./tokio/terceiro.rsf")
    horn.ev3.speaker.play_file("./tokio/quarto.rsf")
    horn.ev3.speaker.play_file("./tokio/quinto.rsf")
    horn.ev3.speaker.play_file("./tokio/sexto.rsf")
    horn.ev3.speaker.play_file("./tokio/setimo.rsf")
    horn.ev3.speaker.play_file("./tokio/oitavo.rsf")
    horn.ev3.speaker.play_file("./tokio/nono.rsf")
    horn.ev3.speaker.play_file("./tokio/decimo.rsf")

def celebration(horn):
    sound_thread = Thread(target=sound.tokio, args=(horn,))
    sound_thread.start()
    turn_thread = Thread(target=turnHornAndCrane, args=(horn,))
    turn_thread.start()



