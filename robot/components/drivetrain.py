from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive
from networktables import NetworkTable
from ctre import WPI_TalonSRX

from utils import limit


SPEED_MULTIPLIER = 1
ANGLE_MULTIPLIER = 1


class DriveTrain:

    # Magicrobot variable injection automatically gets these values from main robot
    # NOTE: components must go in the components folder for magicrobot to properly inject shared variables
    talon_L_1: WPI_TalonSRX
    talon_L_2: WPI_TalonSRX

    talon_R_1: WPI_TalonSRX
    talon_R_2: WPI_TalonSRX

    sd: NetworkTable

    def setup(self):
        """instead of __init__(), use setup() to initialize values (works with magicirobot variable injection"""

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

        self.sd.putValue("Speed", limit(speed, [-1, 1]))
        self.sd.putValue("Angle", limit(angle, [-1, 1]))

    def execute(self) -> None:
        """
        Reads the data from smartdashboard (set by control methods), and then sends data to output devices such as motors.
        Execute is called in telopPeriodic automatically; no need to manually call
        """

        speed = self.sd.getValue("Speed", defaultValue=0.0)
        angle = self.sd.getValue("Angle", defaultValue=0.0)

        # print(speed, angle)

        self.drive.arcadeDrive(angle * ANGLE_MULTIPLIER,
                               speed * SPEED_MULTIPLIER, True)
        # NOTE: THIS IS INVERSED?
        # self.drive.arcadeDrive(speed * SPEED_MULTIPLIER, angle * ANGLE_MULTIPLIER, squareInputs=True)
