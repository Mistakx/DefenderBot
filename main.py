#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import movement, calibration

#! Initialization
ev3 = EV3Brick()
leftMotor = Motor(Port.A)
rightMotor = Motor(Port.B)
craneMotor = Motor(Port.D)
lineColorSensor = ColorSensor(Port.S1)
enemyColorSensor = ColorSensor(Port.S3)
distanceSensor = UltrasonicSensor(Port.S4)
robot = DriveBase(leftMotor, rightMotor, wheel_diameter=55.5, axle_track=104)
#robot.settings(1000, 1000, 100, 1000)


#! Following line calibration settings
mainLineReflection = 10 # Parameter used to walk the main line
boardReflection = 35 # Parameter used to walk the main line
boardBlue = 64 # Parameter used to walk the enemy line
enemyLineBlue = 27 # Parameter used to walk the enemy line
enemyLineColor= Color.RED
proportionalGain = 5 # If the light value deviates from the threshold by 10, the robot steers at 10*1.2 = 12 degrees per second.
followingMovementSpeed = 100

#! Movement calibration
turnCalibrationTo360 = 1000
negativeTurnCalibration = 1.1

#! Calibration
# robot.turn(-1000*negativeTurnCalibration)
# robot.turn(calibration.calibratedTurn(360, turnCalibrationTo360))
# robot.turn(movement.calibratedTurn(90, turnCalibrationTo360))
# robot.straight(-400)
# robot.Stop()
robot.settings(100, 1000, 100, 1000)
# calibration.printColorSensor(lineColorSensor)
#calibration.printEnemyColorSensor(enemyColorSensor)


# notes = ['A4/4', 'A4/4', 'A4/4', 'A4/4', 'A4/6', 'D4/4','d4/6', 'A3/6', 'A3/6']
# ev3.speaker.play_notes(notes, tempo=120)

# movement.followMainLine(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360)
movement.goBackToBoardBeginning(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, enemyLineColor, proportionalGain, followingMovementSpeed)
#robot.drive(100,1)