# This is the Magnolia regional Temporary unfinished autonomous
# Without any gyroscope abilities or anything. 
import networktables
import rev
from components.boom import Boom
from components.drivetrain import DriveTrain
from components.encoders import Encoder
from components.grabber import Grabber
from components.gyro import Gyro
from ctre import NeutralMode
from magicbot import AutonomousStateMachine, state, timed_state

BRAKE_MODE = NeutralMode(2)
COAST_MODE = NeutralMode(1)
class Autonomous(AutonomousStateMachine):
    DEFAULT = False
    MODE_NAME = "timed_state_auto"
    sd: networktables.NetworkTable
    drivetrain: DriveTrain
    boom_arm: Boom
    grabber: Grabber
    gyro: Gyro
    encoder: Encoder
    boom_extender_motor_encoder: rev.SparkMaxRelativeEncoder

    @timed_state(duration=0.75, next_state="grabit", first=True)
    def start(self):
        self.boom_arm.set_rotator(-0.4)
        self.sd.putValue("Mode: ", "Initial Raise")

    @state
    def grabit(self):
        self.boom_arm.set_rotator(0.0)
        self.grabber.solenoid_toggle()
        self.next_state("pause1")

    @timed_state(duration=1, next_state="Rotate")
    def pause1(self):
        self.boom_arm.set_rotator(0)

    @timed_state(duration=2.25, next_state="Drop")
    def Rotate(self):
        self.boom_arm.set_rotator(-0.2)
        self.sd.putValue("Mode: ", "Extending Arm")

    @state
    def Drop(self):
        self.boom_arm.set_rotator(0.0)
        self.grabber.solenoid_toggle()
        self.sd.putValue("Mode: ", "Dropping")
        self.next_state("retract")

    @timed_state(duration=3, next_state="Moveback")
    def retract(self):
        self.boom_arm.set_rotator(0.2)
        self.sd.putValue("Mode: ", "Retracting all previous actions")

    @timed_state(duration=5.5, next_state="Done")
    def Moveback(self):
        self.boom_arm.set_extender(0.0)
        self.boom_arm.set_rotator(0.0)
        self.drivetrain.set_motors(-0.5, 0.0)
        self.sd.putValue("Mode: ", "Taxi for Points")

    # @state(first=True)
    # def start(self):
    #     self.navx = navx.AHRS.create_spi()
    #     self.gyro.reset()
    #     self.boom_extender_motor_encoder.setPosition(0)
    #     self.drivetrain.drivetrain_encoder_left.setPosition(0)
    #     # self.next_state("slight_arm_raise")
    #     self.next_state("move")
    #
    #
    # @timed_state(duration=5.5, next_state="slight_arm_raise", must_finish=True)
    # def move(self):
    #     self.drivetrain.set_motors(0.4, 0)
    #     print(self.drivetrain.drivetrain_encoder_right.getPosition())
    #     # if (self.drivetrain.drivetrain_encoder_left.getPosition() >= 1000):
    #     #     self.drivetrain.set_motors(0, 0)
    #     #     self.next_state("slight_arm_raise")
    #
    #
    # @state
    # def slight_arm_raise(self):
    #     self.drivetrain.set_motors(0, 0)
    #     if (self.boom_arm.boom_rotator_motor.getSelectedSensorPosition() <= -500):
    #         self.boom_arm.set_rotator(-0.2)
    #     else:
    #         self.next_state("clamp")
    #
    # @state
    # def clamp(self):
    #     self.grabber.solenoid_toggle()
    #     self.next_state("rotate_arm")
    #
    #
    # @state
    # def rotate_arm(self):
    #     self.boom_arm.set_rotator(0)
    #     if (self.boom_arm.boom_rotator_motor.getSelectedSensorPosition() <= -2000):
    #         self.boom_arm.set_rotator(-0.2)
    #         # same thing here
    #     else:
    #         # self.next_state("extend")
    #         self.done()

    # Code above is from day 1 of quals

    # @state
    # def extend(self):
    #     self.boom_arm.set_rotator(0)
    #     if (self.boom_extender_motor_encoder.getPosition() <= 5):
    #         self.boom_arm.set_extender(0.2, self.boom_extender_motor_encoder)
    #     else:
    #         self.next_state("drop")
    #
    # @state
    # def drop(self):
    #     self.boom_arm.set_extender(0)
    #     self.grabber.solenoid_toggle()
    #     self.next_state("retract")
    #
    # @state
    # def retract(self):
    #     if (self.boom_extender_motor_encoder.getPosition() <= 0):
    #         self.boom_arm.set_extender(-0.2)
    #     else:
    #         self.next_state("rotate_arm_back")
    #
    # @state
    # def rotate_arm_back(self):
    #     self.boom_arm.set_extender(0)
    #     if (self.boom_arm.boom_rotator_motor.getSelectedSensorPosition() <= 0):
    #         self.boom_arm.set_rotator(0.2)
    #     else:
    #         self.next_state("move_forward")
    #
    # @state
    # def move_forward(self):
    #     self.boom_arm.set_rotator(0)
    #     if (self.drivetrain.drivetrain_encoder_left <= -200):
    #         self.drivetrain.set_motors(-0.5, 0)
    #     else:
    #         self.next_state("balance")
    #
    # @state
    # def balance(self):
    #     self.drivetrain.talon_L_1.setNeutralMode(BRAKE_MODE)
    #     self.drivetrain.talon_L_2.setNeutralMode(BRAKE_MODE)
    #     self.drivetrain.talon_R_1.setNeutralMode(BRAKE_MODE)
    #     self.drivetrain.talon_R_2.setNeutralMode(BRAKE_MODE)
    #     if (self.navx.getRoll() > 5) and (self.navx.getRoll() < -5):
    #         self.gyro.balancing()
    #     else:
    #         self.drivetrain.set_motors(0, 0)
    #         self.boom_arm.set_extender(0)
    #         self.boom_arm.set_rotator(0)
    #         self.sd.putValue("Mode: ", "Completed!")
    #         self.done()