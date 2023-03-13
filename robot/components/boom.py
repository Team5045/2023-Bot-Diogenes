from networktables import NetworkTable
import rev
from utils import limit
from ctre import WPI_TalonFX


STRING_LEN = 28.5  # (inches)


class Boom:

    boom_extender_motor: rev.CANSparkMax
    boom_rotator_motor: WPI_TalonFX

    sd: NetworkTable

    # get sparks from main robot via variable injection

    def setup(self):
        """instead of __init__(), use setup() to initialize values (works with magicrobot variable injection)"""
        self.extender_speed = 0
        self.rotator_speed = 0

    def set_extender(self, motor_speed: float):
        self.extender_speed = limit(motor_speed, [-1, 1])

        self.sd.putValue("Boom Extender Speed: ", self.extender_speed)

    def set_rotator(self, motor_speed: float):
        self.rotator_speed = limit(motor_speed, [-1, 1])

        self.sd.putValue("Boom Rotator Speed: ", self.rotator_speed)

    def execute(self):

        self.boom_extender_motor.set(self.extender_speed)
        self.boom_rotator_motor.set(self.rotator_speed)
