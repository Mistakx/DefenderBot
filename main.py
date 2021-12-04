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
boardBlue = 60 # Parameter used to walk the enemy line
enemyLineReflection = 50 # TODO: Remove 
enemyLineBlue = 36 # Parameter used to walk the enemy line
enemyLineColor= Color.RED
proportionalGain = 1.5 # If the light value deviates from the threshold by 10, the robot steers at 10*1.2 = 12 degrees per second.
followingMovementSpeed = 100

#! Movement calibration
turnCalibrationTo360 = 1000
negativeTurnCalibration = 1.0

#! Calibration
# robot.turn(movement.calibratedTurn(90, turnCalibrationTo360))
# robot.straight(-400)
# robot.Stop()
robot.settings(100, 1000, 100, 1000)
#calibration.printColor(lineColorSensor)
#calibration.printColorSensor(lineColorSensor)

movement.followMainLine(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineReflection, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360)

#robot.drive(100,1)