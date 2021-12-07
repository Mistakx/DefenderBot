#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

import movement, calibration, game

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


#! Following line calibration settings
mainLineReflection = 10 # Parameter used to walk the main line
boardReflection = 35 # Parameter used to walk the main line
boardBlue = 64 # Parameter used to walk the enemy line
enemyLineBlue = 27 # Parameter used to walk the enemy line
enemyLineColor= Color.RED
proportionalGain = 4 # If the light value deviates from the threshold by 10, the robot steers at 10*1.2 = 12 degrees per second.
followingMovementSpeed = 100

#! Movement calibration
turnCalibrationTo360 = 1000
negativeTurnCalibration = 1.1

#! Calibration
# robot.turn(movement.calibratedTurn(-200*negativeTurnCalibration, turnCalibrationTo360))
#calibration.printColorSensor(lineColorSensor)
#calibration.printEnemyColorSensor(enemyColorSensor)

# movement.followMainLine(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360)
#movement.goBackToBoardBeginning(ev3, robot, lineColorSensor, mainLineReflection, boardReflection, enemyLineColor, proportionalGain, followingMovementSpeed)
game.playGame(ev3, robot, lineColorSensor, enemyColorSensor, distanceSensor, mainLineReflection, boardReflection, boardBlue, enemyLineBlue, enemyLineColor, proportionalGain, followingMovementSpeed, negativeTurnCalibration, turnCalibrationTo360)

#robot.settings(1000, 1000, 100, 1000)
#robot.straight(1000)
#robot.stop()