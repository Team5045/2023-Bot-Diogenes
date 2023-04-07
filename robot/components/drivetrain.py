from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive
from networktables import NetworkTable
import rev
from ctre import WPI_TalonFX

from tools.utils import Lim


SPEED_MULTIPLIER = 1
ANGLE_MULTIPLIER = 1

MOTOR_BRUSHED = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushed
MOTOR_BRUSHLESS = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless

class DriveTrain:

    # Magicrobot variable injection automatically gets these values from main robot
    # NOTE: components must go in the components folder for magicrobot to properly inject shared variables
    talon_L_1: WPI_TalonFX
    talon_L_2: WPI_TalonFX

    talon_R_1: WPI_TalonFX
    talon_R_2: WPI_TalonFX

    sd: NetworkTable

    def setup(self):
        """instead of __init__(), use setup() to initialize values (works with magicirobot variable injection"""
        self.drivetrain_encoder_motor_right: rev.CANSparkMax = rev.CANSparkMax(1, MOTOR_BRUSHLESS)
        self.drivetrain_encoder_motor_left: rev.CANSparkMax = rev.CANSparkMax(2, MOTOR_BRUSHLESS)

        self.drivetrain_encoder_right = self.drivetrain_encoder_motor_right.getEncoder()
        self.drivetrain_encoder_left = self.drivetrain_encoder_motor_left.getEncoder()

        self.speed = 0
        self.angle = 0

        self.left_motors: MotorControllerGroup = MotorControllerGroup(
            self.talon_L_1, self.talon_L_2)
        self.right_motors: MotorControllerGroup = MotorControllerGroup(
            self.talon_R_1, self.talon_R_2)

        self.drive: DifferentialDrive = DifferentialDrive(
            self.left_motors, self.right_motors)

    # control method
    def set_motors(self, speed: float, angle: float):
        """
        sets the speed and angle of the motors
        speed: percentage of full speed
        angle: percentage of full rotation, ccw is positive
        Puts values into smartdashboard to be called by arcadeDrive() later in execute()
        """
        self.speed = Lim.limit(speed, [-1, 1])
        self.angle = Lim.limit(angle, [-1, 1])

        self.sd.putValue("Speed", self.speed)
        self.sd.putValue("Angle", self.angle)

    def execute(self) -> None:
        """
        Reads the data from smartdashboard (set by control methods), and then sends data to output devices such as motors.
        Execute is called in telopPeriodic automatically; no need to manually call
        """

        self.drive.arcadeDrive(self.angle, self.speed, True)
