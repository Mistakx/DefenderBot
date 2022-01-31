#!/usr/bin/env pybricks-micropython
from threading import Thread

from pybricks.ev3devices import (ColorSensor, GyroSensor, InfraredSensor,
                                 Motor, TouchSensor, UltrasonicSensor)
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import ImageFile, SoundFile
from pybricks.parameters import Button, Color, Direction, Port, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

import aesthetics
import attack
import calibration
import game
import movement
import sound


#! Initialization
class Horn:
    ev3 = EV3Brick()
    leftMotor = Motor(Port.A)
    rightMotor = Motor(Port.B)
    craneMotor = Motor(Port.D)
    lineColorSensor = ColorSensor(Port.S1)
    enemyColorSensor = ColorSensor(Port.S3)
    distanceSensor = UltrasonicSensor(Port.S4)
    robot = DriveBase(leftMotor, rightMotor, wheel_diameter=55.5, axle_track=104)

class Calibration:
    mainLineReflection = 10 # Parameter used to walk the main line
    boardReflection = 35 # Parameter used to walk the main line (35)
    boardBlue = 62 # Parameter used to walk the enemy line (65)
    enemyLineBlue = 36 # Parameter used to walk the enemy line (25)
    enemyLineColor= Color.RED
    proportionalGain = 4.5 # Default 4: If the light value deviates from the threshold by 10, the robot steers at 10*1.2 = 12 degrees per second.
    turnCalibrationTo360 = 1000
    negativeTurnCalibration = 1
    followingMovementSpeed = 150

class Game:
    currentTurn = 0
    currentPosition = 0 # Position 0 - Positioned before the first enemy line
    hornHealth = 750
    hornEnergy = 500
    enemySlots = ["","","","","",""]
    usingRemainingEnergy = False
    alreadyAttackedThisTurn = True
    # enemySlots = ['Dead', {'n_attacks': 2, 'health': 50, 'type': 'Infantry'}, 'Dead', 'No bottle', 'No bottle', {'n_attacks': 0, 'health': 100, 'type': 'Tank'}]

calibrationInstance = Calibration()
horn = Horn()
gameInfo = Game()
horn.robot.settings(100, 1000, 100, 1000)


#! Calibration
# horn.robot.turn(1050)
#robot.turn(movement.calibratedTurn(-200*negativeTurnCalibration, turnCalibrationTo360))
# calibration.printLineColorSensor(horn.lineColorSensor)
# calibration.printEnemyColorSensor(horn.enemyColorSensor)
#calibration.printDistance(horn.distanceSensor)

#! Aesthetics
#ev3.speaker.say("For you sir, I'm always ready.")
#ev3.light.on(Color.RED)

# light_thread = Thread(target=aesthetics.light, args=(ev3,))
# light_thread.start()
# logo_thread = Thread(target=aesthetics.logo, args=(ev3,))
# logo_thread.start()
# sound_thread = Thread(target=sound.tokio, args=(horn.ev3,))
# sound_thread.start()
# wait(100000000)

#! Play game
game.playGame(horn, calibrationInstance, gameInfo)
