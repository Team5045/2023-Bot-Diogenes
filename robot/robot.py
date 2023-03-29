import wpilib
import rev
from ctre import WPI_TalonFX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable
from wpilib import DoubleSolenoid

from components.drivetrain import DriveTrain
from components.boom import Boom
from components.grabber import Grabber
from components.encoders import encoders
import wpilib.drive
from robotpy_ext.autonomous import AutonomousModeSelector
from wpimath.controller import PIDController

from components.LimeLight import aiming
from ctre import NeutralMode

# Download and install stuff on the RoboRIO after imaging
'''
py -3 -m robotpy_installer download-python
py -3 -m robotpy_installer install-python
py -3 -m robotpy_installer download robotpy
py -3 -m robotpy_installer install robotpy
py -3 -m robotpy_installer download robotpy[ctre]
py -3 -m robotpy_installer install robotpy[ctre]
py -3 -m robotpy_installer download robotpy[rev]
py -3 -m robotpy_installer install robotpy[rev]
py -3 -m robotpy_installer download pynetworktables
py -3 -m robotpy_installer install pynetworktables
py -3 -m pip install -U robotpy[ctre]
py -3 -m pip install robotpy[ctre]
'''

# Push code to RoboRIO (only after imaging)
'''
python robot/robot.py deploy --skip-tests
py robot/robot.py deploy --skip-tests --no-version-check
'''


INPUT_SENSITIVITY = 0.05

PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
MOTOR_BRUSHED = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushed
MOTOR_BRUSHLESS = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless
MagicRobot.control_loop_wait_time = 0.05

SPEED_MULTIPLIER = 1
ANGLE_MULTIPLIER = 1

WINDING_SPEED = .5
NEUTRAL_MODE = NeutralMode(2)

class SpartaBot(MagicRobot):

    # a DriveTrain instance is automatically created by MagicRobot

    drivetrain: DriveTrain
    boom_arm: Boom
    grabber : Grabber

    def createObjects(self):
        """
        IDs
        0: Xbox Controller
        0: Compressor
        4: Talon Left 1
        6: Talon Right 2
        7: Talon Right 1
        8: Talon Left 2



        """

        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')

        self.drive_controller: wpilib.XboxController = wpilib.XboxController(0)  # 0 works for sim?

        self.talon_L_1 = WPI_TalonFX(4)
        self.talon_L_2 = WPI_TalonFX(8)

        self.talon_R_1 = WPI_TalonFX(7)
        self.talon_R_2 = WPI_TalonFX(6)

        # Drivetrain encoders
        self.drivetrain_encoder_motor_right: rev.CANSparkMax = rev.CANSparkMax(1, MOTOR_BRUSHLESS)
        self.drivetrain_encoder_motor_left: rev.CANSparkMax = rev.CANSparkMax(2, MOTOR_BRUSHLESS)

        self.drivetrain_encoder_right = self.drivetrain_encoder_motor_right.getEncoder()
        self.drivetrain_encoder_left = self.drivetrain_encoder_motor_left.getEncoder()

        self.compressor: wpilib.Compressor = wpilib.Compressor(0, PNEUMATICS_MODULE_TYPE)

        self.solenoid1: wpilib.DoubleSolenoid = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 2, 3)
        self.solenoid_gear: wpilib.DoubleSolenoid = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 0, 1)

        self.solenoid1.set(DoubleSolenoid.Value.kForward)
        self.solenoid_gear.set(DoubleSolenoid.Value.kForward)

        self.boom_extender_motor: rev.CANSparkMax = rev.CANSparkMax(4, MOTOR_BRUSHLESS)
        self.boom_rotator_motor = WPI_TalonFX(3)

        self.talon_L_1.setNeutralMode(NEUTRAL_MODE)
        self.talon_L_2.setNeutralMode(NEUTRAL_MODE)
        self.talon_R_1.setNeutralMode(NEUTRAL_MODE)
        self.talon_R_2.setNeutralMode(NEUTRAL_MODE)

        # PID
        self.drivePID = PIDController(0.0006, 0.0012, 0, 0.02)
        self.pidSpeed = 0


    def disabledPeriodic(self):
        self.sd.putValue("Mode", "Disabled")

    def teleopInit(self):
        self.sd.putValue("Mode", "Teleop")
        self.drivetrain_encoder_left.setPosition(0)
        self.drivetrain_encoder_right.setPosition(0)
        self.drivePID.reset()

        # self.limelight = NetworkTables.getTable("limelight")
        # self.limelight.LEDState(3)
        # print("limelight on")
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''
        Called on each iteration of the control loop\n
        NOTE: all components' execute() methods will be called automatically
        '''

        self.pidSpeed = -self.drivePID.calculate(self.drivetrain_encoder_right.getPosition(), 0)

        # drive controls
        angle = self.drive_controller.getRightX()
        speed = self.drive_controller.getLeftY()

        if self.drive_controller.getYButton():
            # pass
            self.drivetrain.set_motors(self.pidSpeed, 0)

        elif (abs(angle) > INPUT_SENSITIVITY or abs(speed) > INPUT_SENSITIVITY):

            self.drivetrain.set_motors(speed, -angle)

            self.sd.putValue('Drivetrain: ', 'moving')
            # Put encoder values in smartdashboard
            self.sd.putValue('Drivetrain Encoder Right: ', self.drivetrain_encoder_right.getPosition())
            self.sd.putValue('Drivetrain Encoder Left: ', self.drivetrain_encoder_left.getPosition())

        else:
            # reset value to make robot stop moving
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue('Drivetrain: ', 'static')

        # print(self.drivetrain.speed)

        # boom rotation: left/right triggers
        rot_speed = 0

        rot_speed += self.drive_controller.getRightTriggerAxis()
        rot_speed -= self.drive_controller.getLeftTriggerAxis()

        self.boom_arm.set_rotator(0)

        if (abs(rot_speed) > INPUT_SENSITIVITY):
            self.boom_arm.set_rotator(rot_speed/5)
            print(rot_speed)

        # boom extension: bumpers
        # NOTE: it is assumed that the boom arm is fully retracted
        wind_speed = 0

        if (self.drive_controller.getRightBumper()):
            wind_speed -= WINDING_SPEED

        if (self.drive_controller.getLeftBumper()):
            wind_speed += WINDING_SPEED

        self.boom_arm.set_extender(wind_speed)

        # grabber: A button to open/close (switches from one state to another)
        if self.drive_controller.getAButtonReleased():
            self.grabber.solenoid_toggle()

        if self.drive_controller.getBButtonReleased():
            self.grabber.toggle_compressor()

        if self.drive_controller.getYButton():
            print(f"drivetrain speed: {self.drivetrain.speed}")
            # print(-self.drivePID.calculate(self.drivetrain_encoder_right.getPosition(), 0))

        # if self.drive_controller.getYButton():
        #     aiming.side_to_side(self)
        #
        # if self.drive_controller.getXButton():
        #     aiming.forward_backward(self)




        self.sd.putValue('PID: ', self.pidSpeed)


        if self.drive_controller.getRightStickButtonReleased():
            self.solenoid_gear.toggle()


if __name__ == '__main__':
    wpilib.run(SpartaBot)
