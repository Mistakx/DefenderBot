#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import movement

ev3 = EV3Brick()


enemy_color_sensor = ColorSensor(Port.S3)
# distance_sensor = UltrasonicSensor() # Port 4



# Write your program here.
ev3.speaker.set_volume(100, which='_all_')
ev3.speaker.set_speech_options(language="pt", voice=None, speed=20, pitch=None)
#ev3.speaker.say("TRAVA NA POSE OOOOOOOOOOOOOOOOOOOOOOOOOOOOOO!")

left_motor = Motor(Port.A)
right_motor = Motor(Port.B)
crane_motor = Motor(Port.D)
robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)
robot.settings(10000, 10000, 10000, 10000)

#robot.turn(movement.calibrated_turn(180)) 
#robot.straight(1500)

notes = ['A4/4', 'A4/4', 'A4/4', 'A4/4', 'A4/4', 'B4/4','D4/5', 'A4/4']
ev3.speaker.play_notes(notes, tempo=120)

#speaker.play_file("tokio.wav")
# robot.straight(1500)
#ev3.speaker.beep()


