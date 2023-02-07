import timer
import wpilib
import rev
from ctre import WPI_TalonSRX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable
from wpilib import DoubleSolenoid
import wpilib.drive
from robotpy_ext.autonomous import AutonomousModeSelector


from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive
from networktables import NetworkTable
from ctre import WPI_TalonSRX
# -------------------------------- Commented Out Imports, to be un-commented ---------------------
# from robot.utils import limit
# from components.drivetrain import DriveTrain
# from components.boom import Boom
# from components.grabber import grabber
# ------------------------------------------------------------------------------------------------
# Download and install stuff on the RoboRIO after imaging
'''py -3 -m robotpy_installer download-python
   py -3 -m robotpy_installer install-python
   py -3 -m robotpy_installer download robotpy
   py -3 -m robotpy_installer install robotpy
   py -3 -m robotpy_installer download robotpy[ctre]
   py -3 -m robotpy_installer install robotpy[ctre]
   py -3 -m robotpy_installer download robotpy[rev]
   py -3 -m robotpy_installer install robotpy[rev]
'''

# Push code to RoboRIO (only after imaging)
'''python robot/robot.py deploy --skip-tests'''
'''py robot/robot.py deploy --skip-tests --no-version-check'''

# if ctre not found
'''py -3 -m pip install -U robotpy[ctre]'''
'''py -3 -m pip install robotpy[ctre]'''

INPUT_SENSITIVITY = .3

MagicRobot.control_loop_wait_time = 0.05

SPEED_MULTIPLIER = 1
ANGLE_MULTIPLIER = 1

# ---------------------------------------------------------------------------------------------------------------------
# Section added from drivetrain.py for testing autonomous, will be removed after completion
def limit(number: float, limits: list) -> float:
    """
    return a number within the limits, returning the limiting number if out of bounds
    number: any number
    limits: list of limits, first element is minimum, second is max
    ex:
        >>> limit(5, [-4, 4])
        >>> 4
    """
    return min(max(number, limits[0]), limits[1])
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

        self.left_motors: MotorControllerGroup = MotorControllerGroup(self.talon_L_1, self.talon_L_2)
        self.right_motors: MotorControllerGroup = MotorControllerGroup(self.talon_R_1, self.talon_R_2)

        self.drive: DifferentialDrive = DifferentialDrive(self.left_motors, self.right_motors)

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

        self.drive.arcadeDrive(angle * ANGLE_MULTIPLIER, speed * SPEED_MULTIPLIER, True)
        # NOTE: THIS IS INVERSED?
        # self.drive.arcadeDrive(speed * SPEED_MULTIPLIER, angle * ANGLE_MULTIPLIER, squareInputs=True)

# -------------------------------------------------------------------------------------------------------------------------
class SpartaBot(MagicRobot):

    # a DriveTrain instance is automatically created by MagicRobot
    drivetrain: DriveTrain
    # boom_arm: Boom

    def createObjects(self):
        '''Create motors and stuff here'''

        PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
        MOTOR_BRUSHED = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushed

        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')

        self.timer = wpilib.Timer()
        self.autonmodes = AutonomousModeSelector("autonomous")

        self.drive_controller = wpilib.XboxController(0) #0 works for sim?

        self.talon_L_1 = WPI_TalonSRX(1)
        self.talon_L_2 = WPI_TalonSRX(5)

        self.talon_R_1 = WPI_TalonSRX(6)
        self.talon_R_2 = WPI_TalonSRX(9)

        self.compressor = wpilib.Compressor(0, PNEUMATICS_MODULE_TYPE)
        self.solenoid = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 0, 1)
        self.solenoid.set(DoubleSolenoid.Value.kForward)


        self.boom_extender_spark = rev.CANSparkMax(1, MOTOR_BRUSHED)
        self.boom_rotator_spark = rev.CANSparkMax(2, MOTOR_BRUSHED)
        #self.testmotor = rev.CANSparkMax(3, MOTOR_BRUSHED)

    def disabledPeriodic(self):
        self.sd.putValue("Mode", "Disabled")

    def autonomousInit(self):
        self.timer.start()
        self.sd.putValue("Mode", "Autonomous")
        print("Auton Beginning")
        # Begins the autonomous timer, should be limited at 15 seconds

    def autonomousPeriodic(self):

        print("Running...")

        if self.timer.get() < 2.0:
            self.drivetrain.set_motors(0.5, 0.0)
            print(self.timer.get())
            print("first auton state running")
            self.sd.putValue("Drivetrain: ", "First Auton State...")
        else:
            self.drivetrain.set_motors(0.0, 0.0)
            print("State 1 Finished")
            self.sd.putValue("Drivetrain:", "First State Finished")

        self.drivetrain.execute()


        # if self.timer.get() < 3.0:
        #     self.drivetrain.set_motors(-0.5, 0.0)
        #     self.sd.putValue("Drivetrain: ", "Second Auton State...")
        #     print("second state running")
        # else:
        #     self.drivetrain.set_motors(0.0, 0.0)
        #     self.sd.putValue("Drivetrain: ", "Second Auton State...")
        #     print("done")

    def disabledInit(self):
        self.autonmodes.disable()
        self.drivetrain.set_motors(0.0, 0.0)
        self.drivetrain.execute()
    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.sd.putValue("Mode", "Teleop")

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''

        # drive controls
        print("tele")
        angle = self.drive_controller.getRightX()
        speed = self.drive_controller.getLeftY()

        if (abs(angle) > INPUT_SENSITIVITY or abs(speed) > INPUT_SENSITIVITY):
            # inverse values to get inverse controls
            self.drivetrain.set_motors(speed, -angle)
            self.sd.putValue('Drivetrain: ', 'moving')

        else:
            # reset value to make robot stop moving
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue('Drivetrain: ', 'static')

        # boom controls
        # if left bumper button pressed, right and left triggers control boom extension
        #   else, they control angle

        # if (self.drive_controller.getLeftBumper()):
        #     #extend_speed = 0
        #
        #     # left trigger retracts, while right trigger extends
        #     self.boom_arm.extender_speed -= self.drive_controller.getLeftTriggerAxis()
        #     self.boom_arm.extender_speed += self.drive_controller.getRightTriggerAxis()
        #
        #     #self.boom_arm.set_extender(extend_speed)
        #
        # elif self.drive_controller.getRightTriggerAxis() > 0.05:
        #     #rotation_speed = 0
        #
        #
        #     self.boom_arm.rotator_speed = self.drive_controller.getRightTriggerAxis()/10
        #
        #
        #     #self.boom_arm.set_rotator(rotation_speed)
        #     #self.boom_rotator_spark.set(rotation_speed/4)
        # elif self.drive_controller.getLeftTriggerAxis() > 0.05:
        #     self.boom_arm.rotator_speed = -self.drive_controller.getLeftTriggerAxis()/10
        #
        # else:
        #     self.boom_arm.rotator_speed = 0
        #     self.boom_arm.extender_speed = 0
        #
        #
        # if self.drive_controller.getXButton():
        #     #self.testmotor.set(0.5)
        #     self.boom_arm.rotator_speed = 0.5
        #     print(self.boom_arm.rotator_speed)
        #
        # else:
        #     #self.testmotor.set(0)
        #     self.boom_rotator_spark.set(0)
        #
        #


        # self.drivetrain's execute() method is automatically called

        # if self.drive_controller.getBButtonReleased():
        #     grabber.turn_off_compressor(self)
        #
        # if self.drive_controller.getAButtonReleased():
        #     grabber.solenoid_toggle(self)

        # if self.drive_controller.getYButton():




if __name__ == '__main__':
    wpilib.run(SpartaBot)