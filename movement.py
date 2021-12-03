def calibrated_turn(turn_angle): 

    # 360 - 900
    # 500 - x

    calibrated_turn = ( (turn_angle * 920) / 360)

    return calibrated_turn

def follow_line():

    line_sensor = ColorSensor(Port.S1)

    black = 10
    white = 40
    threshold = (black + white) / 2 # 25

    # For example, if the light value deviates from the threshold by 10, the robot
    # steers at 10*1.2 = 12 degrees per second.
    PROPORTIONAL_GAIN = 1.2

    # Start following the line endlessly.
    while True:
        # Calculate the deviation from the threshold.
        deviation = line_sensor.reflection() - threshold 
        print("LINE SENSOR: ", line_sensor.reflection())
        print("DEVIATION: ", deviation)

        # Calculate the turn rate.
        turn_rate = PROPORTIONAL_GAIN * deviation
        print("turn_rate: ", turn_rate)
        print("\n")


        # Set the drive base speed and turn rate.
        robot.drive(100, turn_rate)

        # You can wait for a short time or do other things in this loop.
        wait(10)


