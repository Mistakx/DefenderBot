#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import movement, calibration, game, attack

def speak(ev3):
    ev3.speaker.set_volume(100, which='_all_')
    ev3.speaker.set_speech_options(language="pt", voice=None, speed=20, pitch=None)
    ev3.speaker.say("TRAVA NA POSE OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!")

def tokio(ev3):
    # ev3.speaker.play_file("tokio1.rsf")
    # ev3.speaker.play_file("tokio2.rsf")
    # ev3.speaker.play_file("tokio3.rsf")
    # ev3.speaker.play_file("tokioOriginal.rsf")
    # ev3.speaker.play_file("tokioBoost15.rsf")
    # ev3.speaker.play_file("original.rsf")
    ev3.speaker.play_file("toppppp.rsf")
    # ev3.speaker.play_file("tokioBoostMax.rsf")



