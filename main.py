#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread

import movement, calibration, game, attacks, sound, aesthetics

#! Game state
enemySlots = ["","","","","",""]

#! Initialization
ev3 = EV3Brick()
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.B)
craneMotor = Motor(Port.D)
lineColorSensor = ColorSensor(Port.S1)
enemyColorSensor = ColorSensor(Port.S3)
distanceSensor = UltrasonicSensor(Port.S4)
robot = DriveBase(leftMotor, rightMotor, wheel_diameter=55.5, axle_track=104)
robot.settings(100, 1000, 100, 1000)

#! Calibration
followingMovementSpeed = 100
negativeTurnCalibration = 1.1
#robot.turn(1050)
#robot.turn(movement.calibratedTurn(-200*negativeTurnCalibration, turnCalibrationTo360))
#calibration.printLineColorSensor(lineColorSensor)
#calibration.printEnemyColorSensor(enemyColorSensor)
#calibration.printDistance(distanceSensor)

#! Aesthetics
#ev3.speaker.say("For you sir, I'm always ready.")
#ev3.light.on(Color.RED)

# light_thread = Thread(target=aesthetics.light, args=(ev3,))
# light_thread.start()
# logo_thread = Thread(target=aesthetics.logo, args=(ev3,))
# logo_thread.start()
# sound_thread = Thread(target=sound.tokio, args=(ev3,))
# sound_thread.start()
# wait(100000000)

#! Play game
while True:
    game.recognizeBoard(enemySlots, ev3, robot, craneMotor, lineColorSensor, enemyColorSensor, distanceSensor, followingMovementSpeed, negativeTurnCalibration)
    print(enemySlots)

