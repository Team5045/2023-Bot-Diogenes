import rev
from ctre import WPI_TalonFX
from networktables import NetworkTable
from tools.utils import Lim

from wpilib import MotorControllerGroup

# from components.encoders import encoders

CHAIN_LEN = 40  # (encoder ticks)
BUFFER_DISTANCE = 2  # (encoder ticks)


class Boom:
    boom_extender_motor: rev.CANSparkMax
    boom_rotator_motor1: WPI_TalonFX
    boom_rotator_motor2: WPI_TalonFX

    sd: NetworkTable

    # get sparks from main robot via variable injection

    def setup(self):
        """instead of __init__(), use setup() to initialize values (works with magicrobot variable injection)"""
        self.rotation_motors: MotorControllerGroup = MotorControllerGroup(
            self.boom_rotator_motor1, self.boom_rotator_motor2
        )

        self.extender_speed = 0
        self.rotator_speed = 0


    def set_extender(self, motor_speed: float, encoder: rev.SparkMaxRelativeEncoder):
        if (motor_speed > 0):
            if (encoder.getPosition() < (CHAIN_LEN)):
                self.extender_speed = Lim.limit(motor_speed, [0, 1])
            # if (encoder.getPosition() < (CHAIN_LEN - BUFFER_DISTANCE)):
            #     self.extender_speed = Lim.limit(motor_speed, [0, 1])
            # elif (encoder.getPosition() < CHAIN_LEN):
            #     self.extender_speed = Lim.limit(motor_speed, [0, 1]) / 5
            else:
                self.extender_speed = 0
        elif (motor_speed < 0):
            if (encoder.getPosition() > 0):
                self.extender_speed = Lim.limit(motor_speed, [-1, 0])
            # if (encoder.getPosition() > BUFFER_DISTANCE):
            #     self.extender_speed = Lim.limit(motor_speed, [-1, 0])
            # elif (encoder.getPosition() > 0):
            #     self.extender_speed = Lim.limit(motor_speed, [-1, 0]) / 5
            else:
                self.extender_speed = 0
        else:
            self.extender_speed = 0

        # self.extender_speed = Lim.limit(motor_speed, [-1, 1])

        self.sd.putValue("Boom Extender Speed: ", self.extender_speed)
        self.sd.putValue("Boom Extender Position: ", encoder.getPosition())

    def set_rotator(self, motor_speed: float):
        self.rotator_speed = Lim.limit(motor_speed, [-0.7, 0.7])

        self.sd.putValue("Boom Rotator Speed: ", self.rotator_speed)

    def get_arm_angle(self):
        # NOTE: dunno if position of both motors need to be taken into account, or if one is fine
        return self.boom_rotator_motor1.getSelectedSensorPosition()

    def execute(self):
        self.boom_extender_motor.set(self.extender_speed)
        self.rotation_motors.set(self.rotator_speed)
        