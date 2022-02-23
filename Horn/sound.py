#!/usr/bin/env pybricks-micropython
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

import attack
import calibration
import game
import movement


def speak(ev3):
    ev3.speaker.set_volume(100, which="_all_")
    ev3.speaker.set_speech_options(language="pt", voice=None, speed=20, pitch=None)
    ev3.speaker.say("TRAVA NA POSE OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!")


def tokio(horn):
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
