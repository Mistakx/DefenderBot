#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
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



