# This is the Magnolia regional Temporary unfinished autonomous
# Without any gyroscope abilities or anything. 
from components.drivetrain import DriveTrain
# from components.grabber import Grabber
# from components.boom import Boom
from magicbot import magicrobot
from components.gyro import Gyro

from magicbot import AutonomousStateMachine, tunable, state, timed_state
import networktables
import wpilib
import navx


class Autonomous(AutonomousStateMachine):
    DEFAULT = True
    MODE_NAME = "autodrive"
    sd: networktables.NetworkTable
    drivetrain: DriveTrain
    # boom_arm: Boom
    # grabber: Grabber
    gyro: Gyro

    
    # @timed_state(duration = 3.75, next_state = "pause1",  first = True)
    # def RaiseArm(self):
    #     self.boom_arm.set_rotator(-0.2)
    #     self.sd.putValue("Mode: ", "Raising Arm")
    
    # @timed_state(duration = 1, next_state = "ExtendArm")
    # def pause1(self):
    #     self.boom_arm.set_rotator(0)
    
    # @timed_state(duration = 3, next_state = "Drop")
    # def ExtendArm(self):
    #     self.boom_arm.set_rotator(0.033)
    #     self.boom_arm.set_extender(-0.75)
    #     self.sd.putValue("Mode: ", "Extending Arm")
    
    # @timed_state(duration = 3, next_state = "retract")
    # def Drop(self):
    #     self.boom_arm.set_extender(0) 
    #     self.grabber.solenoid_toggle()
    #     self.sd.putValue("Mode: ", "Dropping")

    # @timed_state(duration = 3, next_state = "Moveback")
    # def retract(self):
    #     self.boom_arm.set_rotator(0.15)
    #     self.boom_arm.set_extender(0.25)
    #     self.sd.putValue("Mode: ", "Retracting all previous actions")

    # @timed_state(duration = 1, next_state = "Done")
    # def Moveback(self):
    #     self.boom_arm.set_extender(0.0)
    #     self.boom_arm.set_rotator(0.0)
    #     self.drivetrain.set_motors(-0.5, 0.0)
    #     self.sd.putValue("Mode: ", "Taxi for Points")

    # @state
    # def Done(self):
    #     self.drivetrain.set_motors(0.0, 0.0)
    #     self.sd.putValue("Mode: ", "Completed!")


    ''' IN THE ASSUMPTION THAT WE DO NOT HAVE A WORKING ARM...'''
    ''' ANYTHING ABOVE IS ONLY IN CASE WE ACTUALLY HAVE AN ARM!!!!!!!!!'''
    '''comment out when you are trying to switch modes'''
    # will add additional chargepad stuff cuz we have gyro
    # @timed_state(duration = 3, next_state = "COMPLETE", first = True)
    # def noArm(self):
    #     self.drivetrain.set_motors(0.6, 0.0)
    #     self.sd.putValue("AUTON: ", "MOVING...")

    # Alternative for Chargepad
    @timed_state(duration = 1.75, next_state = "Balancing", first = True)
    def begin(self):
        self.drivetrain.set_motors(0.6, 0.0)
        self.sd.putValue("AUTON: ", "First State...")

    @state
    def balancing(self):
        self.navx = navx.AHRS.create_spi()
        if (self.navx.getRoll > 5) and (self.navx.getRoll < -5):
            self.gyro.balancing()
            self.sd.putValue("AUTON: ", "GYRO ENABLED")
        # Does the gyro thing in auton yay
        else:
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue("AUTON: ", "GYRO NOT DETECTING")
        self.next_state = "COMPLETE"
    
    @state
    def COMPLETE(self):
        self.drivetrain.set_motors(0.0, 0.0)
        self.sd.putValue("AUTON: ", "DONE")


