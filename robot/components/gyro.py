# time for a pro gyro no lie
import navx
from components.drivetrain import DriveTrain
import wpilib
import ctre
import networktables
from networktables import NetworkTable
from magicbot import MagicRobot
# Various imports

class Gyro():
    # MagicBot Variable Injection
    sd: networktables.NetworkTable
    drivetrain: DriveTrain
    
    def setup(self):
        self.navx = navx.AHRS.create_spi()
        # Sets up the navx AHRS system

    def balancing(self):
        MAX_RANGE_LIM_HI = 180
        MAX_RANGE_LIM_LOW = -180
        DEFAULT_LOW = -5
        DEFAULT_HI = 5
        angle = self.navx.getRoll()
        # Various variables that are used in the calculations
        ''' Just making things a bit easier to read here with variables'''
        # This should provide constant adjustment to the speeds so it won't jerk the robot

        print(f'ANGLE_RETURN: {angle}')

        try:
        # try and except 
            if (angle < MAX_RANGE_LIM_HI) and (angle > MAX_RANGE_LIM_LOW):
                # PRECHECK TO MAKE SURE GYRO IS IN GOOD CONDITION
                if (angle < DEFAULT_LOW) and (angle > MAX_RANGE_LIM_LOW):
                    self.drivetrain.set_motors(0.33, 0.0)
                    self.sd.putValue("Mode: ", "Moving Forward")
                    print("MODE: ST1")
                    # Forward

                elif (angle > DEFAULT_HI) and (angle < MAX_RANGE_LIM_HI):
                    self.drivetrain.set_motors(-0.33, 0.0)
                    self.sd.putValue("Mode: ", "Moving Backward")
                    print("MODE: ST2")
                    # Backward

                elif (angle < DEFAULT_HI) and (angle > DEFAULT_LOW):
                    self.drivetrain.set_motors(0.0, 0.0)
                    self.sd.putValue("Mode: ", "Balanced!")
                    print("balanced!")
                    print(self.navx.getPitch())
                    # Balanced
            else:
                # In this case: Either bot is flipped, or error values
                print("ERROR: OUT OF BOUNDS: E.1")
                self.drivetrain.set_motors(0.0, 0.0)
                self.sd.putValue("Mode: ", "GYRO ERROR")
        except:
            print("ERROR: EXTERNAL ISSUE: E.2")

    # Try and except statement in case something goes bad, this is an effort to protect motors and the robot during autonomous

    def reset(self):
        self.navx.reset()
        print("STATE: RESETTING NAVX")
    
    def execute(self):
        pass
            

        
        