# This is the Magnolia regional Temporary unfinished autonomous
# Without any gyroscope abilities or anything. 
from components.drivetrain import DriveTrain
from components.grabber import Grabber
from components.boom import Boom
from components.gyro import Gyro
from magicbot import magicrobot

from magicbot import AutonomousStateMachine, tunable, state, timed_state
import networktables
import wpilib
import navx


class autoCharge(AutonomousStateMachine):
    DEFAULT = True
    MODE_NAME = "autodrive"
    sd: networktables.NetworkTable
    drivetrain: DriveTrain
    boom_arm: Boom
    grabber: Grabber
    gyro: Gyro

    
    @timed_state(duration = 3.75, next_state = "pause1",  first = True)
    def RaiseArm(self):
        self.gyro.reset()
        self.boom_arm.set_rotator(-0.2)
        self.sd.putValue("Mode: ", "Raising Arm")
    
    @timed_state(duration = 1, next_state = "ExtendArm")
    def pause1(self):
        self.boom_arm.set_rotator(0)
    
    @timed_state(duration = 3, next_state = "Drop")
    def ExtendArm(self):
        self.boom_arm.set_rotator(0.033)
        self.boom_arm.set_extender(-0.75)
        self.sd.putValue("Mode: ", "Extending Arm")
    
    @timed_state(duration = 3, next_state = "retract")
    def Drop(self):
        self.boom_arm.set_extender(0) 
        self.grabber.solenoid_toggle()
        self.sd.putValue("Mode: ", "Dropping")

    @timed_state(duration = 3, next_state = "Moveback")
    def retract(self):
        self.boom_arm.set_rotator(0.15)
        self.boom_arm.set_extender(0.25)
        self.sd.putValue("Mode: ", "Retracting all previous actions")

    @timed_state(duration = 1, next_state = "Done")
    def Moveback(self):
        self.boom_arm.set_extender(0.0)
        self.boom_arm.set_rotator(0.0)
        self.drivetrain.set_motors(-0.5, 0.0)
        self.sd.putValue("Mode: ", "Taxi for Points")

    @state
    def Done(self):
        self.drivetrain.set_motors(0.0, 0.0)
        self.sd.putValue("Mode: ", "Completed!")


class Cone_Charge(AutonomousStateMachine):
    DEFAULT = True
    MODE_NAME = "autodrive"
    sd: networktables.NetworkTable
    drivetrain: DriveTrain
    boom_arm: Boom
    grabber: Grabber
    gyro: Gyro

    @state(first = True, next_state = "clamp")
    def start(self):
        self.navx = navx.AHRS.create_spi()
        self.gyro.reset()
        self.boom_arm.boom_extender_motor.getEncoder().setPosition(0)
    
    @state(next_state = "rotate_back")
    def clamp(self):
        self.grabber.solenoid_toggle()
    
    @state(next_state = "drop")
    def rotate_arm(self):
        self.boom_arm.boom_rotator_motor
    
    @state(next_state = "retract")
    def drop(self):
        self.grabber.solenoid_toggle()

    @state(next_state = "rotate_arm_back")
    def retract(self):
    
    @state(next_state = "move_forward")
    def rotate_arm_back(self):

    @state(next_state = "balance")
    def move_forward(self):
    
    @state(next_state = "Done")
    def balance(self):
    
    @state
    def Done(self):
        self.drivetrain.set_motors(0, 0)
        self.boom_arm.set_extender(0)
        self.boom_arm.set_rotator(0)
        self.sd.putValue("Mode: ", "Completed!")


        