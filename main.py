#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor, InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from threading import Thread

import movement, calibration, game, attack, sound, aesthetics

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
    boardBlue = 65 # Parameter used to walk the enemy line (65)
    enemyLineBlue = 30 # Parameter used to walk the enemy line (25)
    enemyLineColor= Color.RED
    proportionalGain = 4 # Default 4: If the light value deviates from the threshold by 10, the robot steers at 10*1.2 = 12 degrees per second.
    turnCalibrationTo360 = 930
    negativeTurnCalibration = 1.1
    followingMovementSpeed = 100

class Game: 
    currentPosition = 0 # Position 0 - Positioned before the first enemy line
    hornHealth = 750
    hornEnergy = 500
    enemySlots = ["","","","","",""]
    # enemySlots = [{'n_attacks': 2, 'health': 200, 'type': 'Tank'}, {'n_attacks': 2, 'health': 200, 'type': 'Tank'}, {'strength': 500, 'type': 'Artillery', 'health': 50, 'n_attacks': 1}, {'strength': 500, 'type': 'Artillery', 'health': 50, 'n_attacks': 1}, {'n_attacks': 3, 'health': 100, 'type': 'Infantry'}, {'n_attacks': 2, 'health': 200, 'type': 'Tank'}]
    # enemySlots = ["Dead","","Dead","","Dead",""]

calibrationInstance = Calibration()
horn = Horn()
gameInfo = Game()
horn.robot.settings(100, 1000, 100, 1000)


#! Calibration
# horn.robot.turn(900)
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
# movement.goBackToFirstEnemyLine(horn, calibration, calibration.followingMovementSpeed*2, gameInfo)

