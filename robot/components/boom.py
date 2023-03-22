from networktables import NetworkTable
import rev
from tools.utils import Lim
from ctre import TalonFX
from components.encoders import encoders


STRING_LEN = 28.5  # (inches)


class Boom:

    # get sparks from main robot via variable injection
    boom_extender_spark: rev.CANSparkMax
    boom_rotator_spark: TalonFX

    sd: NetworkTable

    def setup(self):
        """instead of __init__(), use setup() to initialize values (works with magicrobot variable injection)"""
        self.extender_speed = 0
        self.rotator_speed = 0

        # self.extender_hall_encoder = self.boom_extender_spark.getEncoder()
        # self.extender_hall_encoder.setPosition(0)

        # for now, there are not limits to how much you can wind the string (with extender)
        #   in the future, add safety mechanism to ensure string is not overwound
        # self.slack = STRING_LEN

    def set_extender(self, motor_speed: float):
        self.extender_speed = Lim.limit(motor_speed, [-1, 1])

        self.sd.putValue("Boom Extender Speed: ", self.extender_speed)

    def set_rotator(self, motor_speed: float):
        self.rotator_speed = Lim.limit(motor_speed, [-1, 1])

        self.sd.putValue("Boom Rotator Speed: ", self.rotator_speed)

    def execute(self):

        self.boom_extender_spark.set(self.extender_speed)
        self.boom_rotator_spark.set(self.rotator_speed)
        

