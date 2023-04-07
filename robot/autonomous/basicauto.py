# This is the Magnolia regional Temporary unfinished autonomous
# Without any gyroscope abilities or anything. 
import networktables
from components.boom import Boom
from components.drivetrain import DriveTrain
from components.grabber import Grabber
from components.gyro import Gyro
from components.encoders import Encoder
from magicbot import AutonomousStateMachine, state, timed_state
import navx
import rev
from ctre import NeutralMode

BRAKE_MODE = NeutralMode(2)
COAST_MODE = NeutralMode(1)
class Autonomous(AutonomousStateMachine):
    DEFAULT = True
    MODE_NAME = "autodrive"
    sd: networktables.NetworkTable
    drivetrain: DriveTrain
    boom_arm: Boom
    grabber: Grabber
    gyro: Gyro
    encoder: Encoder
    boom_extender_motor_encoder: rev.SparkMaxRelativeEncoder

    @state(first = True, next_state = "slight_arm_raise")
    def start(self):
        self.navx = navx.AHRS.create_spi()
        self.gyro.reset()
        self.boom_extender_motor_encoder.setPosition(0)
    
    @state(next_state = "clamp")
    def slight_arm_raise(self):
        if (self.boom_arm.boom_rotator_motor.getSelectedSensorPosition() <= -500):
            self.boom_arm.set_rotator(0.2)
        else:
            self.next_state_now("clamp")

    @state(next_state = "rotate_back")
    def clamp(self):
        self.grabber.solenoid_toggle()
    
    
    @state(next_state = "extend")
    def rotate_arm(self):
        self.boom_arm.set_rotator(0)
        if (self.boom_arm.boom_rotator_motor.getSelectedSensorPosition() <= -2000):
            self.boom_arm.set_rotator(0.2)
        else:
            self.next_state_now("extend")
    
    @state(next_state = "drop")
    def extend(self):
        self.boom_arm.set_rotator(0)
        if (self.boom_extender_motor_encoder.getPosition() <= 5):
            self.boom_arm.set_extender(0.2)
        else:
            self.next_state_now("drop")

    @state(next_state = "retract")
    def drop(self):
        self.boom_arm.set_extender(0)
        self.grabber.solenoid_toggle()

    @state(next_state = "rotate_arm_back")
    def retract(self):
        if (self.boom_extender_motor_encoder.getPosition() <= 0):
            self.boom_arm.set_extender(-0.2)
        else:
            self.next_state_now("rotate_arm_back")

    @state(next_state = "move_forward")
    def rotate_arm_back(self):
        self.boom_arm.set_extender(0)
        if (self.boom_arm.boom_rotator_motor.getSelectedSensorPosition() <= 0):
            self.boom_arm.set_rotator(-0.2)
        else:
            self.next_state_now("move_forward")

    @state(next_state = "balance")
    def move_forward(self):
        self.boom_arm.set_rotator(0)
        if (self.drivetrain.drivetrain_encoder_left <= -200):
            self.drivetrain.set_motors(-0.5, 0)
        else:
            self.next_state_now("balance")

    @state(next_state = "Done")
    def balance(self):
        self.drivetrain.talon_L_1.setNeutralMode(BRAKE_MODE)
        self.drivetrain.talon_L_2.setNeutralMode(BRAKE_MODE)
        self.drivetrain.talon_R_1.setNeutralMode(BRAKE_MODE)
        self.drivetrain.talon_R_2.setNeutralMode(BRAKE_MODE)
        if (self.navx.getRoll > 5) and (self.navx.getRoll < -5):
            self.gyro.balancing()
        else:
            self.next_state_now("Done")
    @state
    def Done(self):
        self.drivetrain.set_motors(0, 0)
        self.boom_arm.set_extender(0)
        self.boom_arm.set_rotator(0)
        self.sd.putValue("Mode: ", "Completed!")
