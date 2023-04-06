# This is the Magnolia regional Temporary unfinished autonomous
# Without any gyroscope abilities or anything. 
from components.drivetrain import DriveTrain
from components.grabber import Grabber
from components.boom import Boom
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
    boom_arm: Boom
    grabber: Grabber
    gyro: Gyro

    # @timed_state(duration = 0.75, next_state = "grabit", first = True)
    # def start(self):
    #     self.boom_arm.set_rotator(-0.2)
    #     self.sd.putValue("Mode: ", "Initial Raise")
    
    # @state(next_state = "pause1")
    # def grabit(self):
    #     self.boom_arm.set_rotator(0.0)
    #     self.grabber.solenoid_toggle()
    
    # @timed_state(duration = 1, next_state = "Rotate")
    # def pause1(self):
    #     self.boom_arm.set_rotator(0)
    
    # @timed_state(duration = 2.25, next_state = "Drop")
    # def ExtendArm(self):
    #     self.boom_arm.set_rotator(-0.2)
    #     self.sd.putValue("Mode: ", "Extending Arm")
    
    # @state(next_state = "Retract")
    # def Drop(self):
    #     self.boom_arm.set_rotator(0.0) 
    #     self.grabber.solenoid_toggle()
    #     self.sd.putValue("Mode: ", "Dropping")

    # @timed_state(duration = 3, next_state = "Moveback")
    # def retract(self):
    #     self.boom_arm.set_rotator(0.2)
    #     self.sd.putValue("Mode: ", "Retracting all previous actions")

    # @timed_state(duration = 3, next_state = "Done")
    # def Moveback(self):
    #     self.boom_arm.set_extender(0.0)
    #     self.boom_arm.set_rotator(0.0)
    #     self.drivetrain.set_motors(-0.5, 0.0)
    #     self.sd.putValue("Mode: ", "Taxi for Points")
    '''^^^^^^^^^^^^^^^^^^^ THIS IS OPTION ONE WITHOUT GYRO AS IN NO CHARGEPAD ^^^^^^^^^^^^'''

    # @timed_state(duration = 2, next_state = "balance")
    # def Moveback(self):
    #     self.boom_arm.set_rotator(0.0)
    #     self.drivetrain.set_motors(-0.5, 0.0)
    #     self.sd.putValue("Mode: ", "Moving Back")

    # @timed_state(duration = 6, next_state = "done")
    # def balance(self):
    #     self.navx = navx.AHRS.create_spi()
    #     if (self.navx.getRoll > 5) and (self.navx.getRoll < -5):
    #         self.gyro.balancing()
    #         self.sd.putValue("AUTON: ", "GYRO ENABLED")
    #     # Does the gyro thing in auton yay
    #     else:
    #         self.drivetrain.set_motors(0.0, 0.0)
    #         self.sd.putValue("AUTON: ", "GYRO NOT DETECTING")

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

    # Alternative for Chargepad, I suggest using this.
    # @timed_state(duration = 1.75, next_state = "Balancing", first = True)
    # def begin(self):
    #     self.drivetrain.set_motors(0.6, 0.0)
    #     self.sd.putValue("AUTON: ", "First State...")

    # @state
    # def balancing(self):
    #     self.navx = navx.AHRS.create_spi()
    #     if (self.navx.getRoll > 5) and (self.navx.getRoll < -5):
    #         self.gyro.balancing()
    #         self.sd.putValue("AUTON: ", "GYRO ENABLED")
    #     # Does the gyro thing in auton yay
    #     else:
    #         self.drivetrain.set_motors(0.0, 0.0)
    #         self.sd.putValue("AUTON: ", "GYRO NOT DETECTING")

    #     self.next_state = "COMPLETE"
    
    # @state
    # def COMPLETE(self):
    #     self.drivetrain.set_motors(0.0, 0.0)
    #     self.sd.putValue("AUTON: ", "DONE")


