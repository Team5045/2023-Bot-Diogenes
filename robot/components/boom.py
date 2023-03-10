from networktables import NetworkTable
import rev
from utils import limit
from ctre import WPI_TalonFX


STRING_LEN = 28.5  # (inches)




class Boom:

    boom_extender_spark: rev.CANSparkMax
    boom_rotator_spark: WPI_TalonFX

    sd: NetworkTable
    
    kP = 0
    kI = 0
    kD = 0
    kF = 0

    # get sparks from main robot via variable injection
    
    def setup(self):
        """instead of __init__(), use setup() to initialize values (works with magicrobot variable injection)"""
        self.extender_speed = 0
        self.rotator_speed = 0

        # for now, there are not limits to how much you can wind the string (with extender)
        #   in the future, add safety mechanism to ensure string is not overwound
        # self.slack = STRING_LEN

        self.boom_rotator_spark.config_kF(0, self.kF, 10)
        self.boom_rotator_spark.config_kP(0, self.kP, 10)
        self.boom_rotator_spark.config_kI(0, self.kI, 10)
        self.boom_rotator_spark.config_kD(0, self.kD, 10)
        
        self.boom_rotator_spark.setInverted(False)
    

    def set_Setpoint(self, setpoint: float):
            self.setpoint = setpoint

    def set_extender(self, motor_speed: float):
        self.extender_speed = limit(motor_speed, [-1, 1])

        self.sd.putValue("Boom Extender Speed: ", self.extender_speed)

    def set_rotator(self, motor_speed: float):
        self.rotator_speed = limit(motor_speed, [-1, 1])

        self.sd.putValue("Boom Rotator Speed: ", self.rotator_speed)
    

    def execute(self):

        self.boom_extender_spark.set(self.extender_speed)
        self.boom_rotator_spark.set(self.rotator_speed)
