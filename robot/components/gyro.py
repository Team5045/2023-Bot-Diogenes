# time for a pro gyro no lie
import navx
from components.drivetrain import DriveTrain
import wpilib
import ctre
import networktables
from networktables import NetworkTable
from magicbot import MagicRobot
from ctre import WPI_TalonFX
from ctre import NeutralMode
# Various imports

BRAKE_MODE = NeutralMode(2)
COAST_MODE = NeutralMode(1)

class Gyro():
    # MagicBot Variable Injection
    sd: networktables.NetworkTable
    drivetrain: DriveTrain
    talon_L_1: WPI_TalonFX
    talon_L_2: WPI_TalonFX
    talon_R_1: WPI_TalonFX
    talon_R_2: WPI_TalonFX
    
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

        self.sd.putValue("ANGLE_RETURN: ", angle)
        # Puts angle return in SD

        try:
        # try and except 
            if (angle < MAX_RANGE_LIM_HI) and (angle > MAX_RANGE_LIM_LOW):
                # PRECHECK TO MAKE SURE GYRO IS IN GOOD CONDITION

                if (angle < DEFAULT_LOW) and (angle > MAX_RANGE_LIM_LOW):
                    
                    self.drivetrain.set_motors(0.33, 0.0)
                    self.sd.putValue("gyro_status: ", "Moving Forward")
                    # Forward

                elif (angle > DEFAULT_HI) and (angle < MAX_RANGE_LIM_HI):

                    self.drivetrain.set_motors(-0.33, 0.0)
                    self.sd.putValue("gyro_status: ", "Moving Backward")
                    # Backward

                elif (angle < DEFAULT_HI) and (angle > DEFAULT_LOW):
                    
                    self.drivetrain.set_motors(0.0, 0.0)
                    self.sd.putValue("gyro_status: ", "Balanced!")
                    print(self.navx.getPitch())
                    # Braking after balancing :)
                    self.talon_L_1.setNeutralMode(BRAKE_MODE)
                    self.talon_L_2.setNeutralMode(BRAKE_MODE)
                    self.talon_R_1.setNeutralMode(BRAKE_MODE)
                    self.talon_R_2.setNeutralMode(BRAKE_MODE)
                    # Balanced
            else:
                # In this case: Either bot is flipped, or error values
                print("ERROR: OUT OF BOUNDS: E.1")
                self.drivetrain.set_motors(0.0, 0.0)
                self.sd.putValue("gyro_status: ", "GYRO ERROR")
        except:
            print("ERROR: EXTERNAL ISSUE: E.2")

    # Try and except statement in case something goes bad, this is an effort to protect motors and the robot during autonomous

    def reset(self):
        self.navx.reset()
        self.sd.putValue("gyro_status: ", "navx_reset")

    def execute(self):
        # just passes through this to execute gyro in robot.py
        pass
            

        
        