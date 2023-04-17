import navx
import rev
import wpilib
import wpilib.drive
from ctre import NeutralMode
from ctre import WPI_TalonFX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable
from wpilib import DoubleSolenoid
from wpimath.controller import PIDController

from components.boom import Boom
from components.drivetrain import DriveTrain
from components.encoders import Encoder
from components.grabber import Grabber
from components.gyro import Gyro

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

PID_TARGET_INPUT_MULTIPLIER = 1000

PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
MOTOR_BRUSHED = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushed
MOTOR_BRUSHLESS = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushless
MagicRobot.control_loop_wait_time = 0.05

SPEED_MULTIPLIER = 1
ANGLE_MULTIPLIER = 1

WINDING_SPEED = .2
BRAKE_MODE = NeutralMode(2)
COAST_MODE = NeutralMode(1)


class SpartaBot(MagicRobot):

    # a DriveTrain instance is automatically created by MagicRobot

    drivetrain: DriveTrain
    boom_arm: Boom
    grabber: Grabber
    gyro: Gyro
    encoder: Encoder

    def createObjects(self):
        '''Create motors and stuff here'''

        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')

        self.drive_controller: wpilib.XboxController = wpilib.XboxController(
            0)  # 0 works for sim?

        self.talon_L_1 = WPI_TalonFX(4)
        self.talon_L_2 = WPI_TalonFX(8)

        self.talon_R_1 = WPI_TalonFX(7)
        self.talon_R_2 = WPI_TalonFX(6)

        self.compressor: wpilib.Compressor = wpilib.Compressor(0, PNEUMATICS_MODULE_TYPE)

        self.solenoid1: wpilib.DoubleSolenoid = wpilib.DoubleSolenoid(
            PNEUMATICS_MODULE_TYPE, 2, 3)
        self.solenoid_gear: wpilib.DoubleSolenoid = wpilib.DoubleSolenoid(
            PNEUMATICS_MODULE_TYPE, 0, 1)

        self.solenoid1.set(DoubleSolenoid.Value.kForward)
        self.solenoid_gear.set(DoubleSolenoid.Value.kForward)

        self.boom_extender_motor: rev.CANSparkMax = rev.CANSparkMax(
            4, MOTOR_BRUSHLESS)
        self.boom_extender_motor_encoder: rev.SparkMaxRelativeEncoder = self.boom_extender_motor.getEncoder()
        self.boom_rotator_motor1 = WPI_TalonFX(5)
        self.boom_rotator_motor2 = WPI_TalonFX(3)

        self.talon_L_1.setNeutralMode(COAST_MODE)
        self.talon_L_2.setNeutralMode(COAST_MODE)
        self.talon_R_1.setNeutralMode(COAST_MODE)
        self.talon_R_2.setNeutralMode(COAST_MODE)

        self.prev_mode_moving = True

        self.navx = navx.AHRS.create_spi()

        self.is_braking = False

        # PID
        self.armPID = PIDController(0.00001, 0.0001, 0.0001, 0.02)
        self.armPID.setTolerance(50)
        self.arm_pid_target = -10000
        self.arm_pid_output = 0
        self.arm_pid_enabled = False

        self.drivePID = PIDController(0.0001, 0, 0, 0.02)
        self.drivePID.setTolerance(50)
        


    def disabledInit(self) -> None:
        self.navx.reset()

        self.navx = navx.AHRS.create_spi()

    def disabledInit(self) -> None:
        self.navx.reset()

    def disabledPeriodic(self):
        self.sd.putValue("Mode", "Disabled")

    def teleopInit(self):
        self.sd.putValue("Mode", "Teleop")
        self.boom_extender_motor_encoder.setPosition(0)
        self.boom_rotator_motor1.setSelectedSensorPosition(0)
        self.boom_rotator_motor2.setSelectedSensorPosition(0)
        self.armPID.reset()
        # self.compressor.disable()
        # self.limelight = NetworkTables.getTable("limelight")
        # self.limelight.LEDState(3)
        # print("limelight on")
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''
        Called on each iteration of the control loop\n
        NOTE: all components' execute() methods will be called automatically
        '''

        # if (not self.armPID.atSetpoint()):
        #     self.armPID.setSetpoint(self.arm_pid_target)
        #     # self.arm_pid_output = self.armPID.calculate(self.boom_rotator_motor.getSelectedSensorPosition(), self.arm_pid_target)
        #     self.arm_pid_output = self.armPID.calculate(self.boom_rotator_motor.getSelectedSensorPosition())
        # else:
        #     self.arm_pid_output = 0

        # drive controls
        # print("tele")
        

        # mode = self.drivetrain.is_moving()
        #
        #
        #
        # if (mode != self.prev_mode_moving):
        #     print("changed mode!")
        #     if (mode):
        #
        #         self.drivetrain.set_motors(speed, -angle)
        #         self.drivetrain.set_mode(COAST_MODE)
        #         self.sd.putValue('Drivetrain: ', 'moving')
        #
        #     else:
        #         # reset value to make robot stop moving
        #         self.drivetrain.set_mode(BRAKE_MODE)
        #         self.drivetrain.set_motors(0.0, 0.0)
        #         self.sd.putValue('Drivetrain: ', 'static')
        #
        # self.prev_mode_moving = mode

        '''BOOM AND GRABBER COMMENTED OUT'''
        # boom rotation: left/right triggers
        # rot_speed = 0
        # #
        # rot_speed += self.drive_controller.getRightTriggerAxis()
        # rot_speed -= self.drive_controller.getLeftTriggerAxis()

        # arm_pid_target += self.drive_controller.getRightTriggerAxis()
        # arm_pid_target -= self.drive_controller.getLeftTriggerAxis()

        # if (abs(rot_speed) > INPUT_SENSITIVITY):
        #     self.boom_arm.set_rotator(rot_speed / 5)
        # else:
        #     self.boom_arm.set_rotator(0)

        # Boom rotation PID

        if (abs(self.drive_controller.getRightTriggerAxis()) > INPUT_SENSITIVITY or abs(
                self.drive_controller.getLeftTriggerAxis()) > INPUT_SENSITIVITY):
            self.arm_pid_target += self.drive_controller.getRightTriggerAxis() * PID_TARGET_INPUT_MULTIPLIER
            self.arm_pid_target -= self.drive_controller.getLeftTriggerAxis() * PID_TARGET_INPUT_MULTIPLIER
            self.armPID.setSetpoint(self.arm_pid_target)
            if not self.arm_pid_enabled:
                self.arm_pid_target = (self.boom_rotator_motor1.getSelectedSensorPosition() + self.boom_rotator_motor2.getSelectedSensorPosition()) / 2
                self.armPID.setSetpoint(self.arm_pid_target)
                self.arm_pid_enabled = True
                self.armPID.reset()

        if self.drive_controller.getYButtonReleased():
            self.arm_pid_enabled = not self.arm_pid_enabled
            if self.arm_pid_enabled:
                self.armPID.setSetpoint(self.arm_pid_target)

        if self.arm_pid_enabled:
            self.arm_pid_output = self.armPID.calculate((self.boom_rotator_motor1.getSelectedSensorPosition() + self.boom_rotator_motor2.getSelectedSensorPosition()) / 2)
            self.boom_arm.set_rotator(self.arm_pid_output)
        else:
            self.boom_arm.set_rotator(0)
            self.armPID.reset()
        
        angle = self.drivePID.calculate(self.drive_controller.getRightX())
        speed = self.drivePID.calculate(self.drive_controller.getLeftY())

        if (abs(angle) > INPUT_SENSITIVITY or abs(speed) > INPUT_SENSITIVITY):
            if self.is_braking:
                # print("setting coast mode")
                self.talon_L_1.setNeutralMode(COAST_MODE)
                self.talon_L_2.setNeutralMode(COAST_MODE)
                self.talon_R_1.setNeutralMode(COAST_MODE)
                self.talon_R_2.setNeutralMode(COAST_MODE)
                self.is_braking = False

            self.drivetrain.set_motors(speed, -angle)

            self.sd.putValue('Drivetrain: ', 'moving')
            
            # self.talon_L_1.setNeutralMode(COAST_MODE)
            # self.talon_L_2.setNeutralMode(COAST_MODE)
            # self.talon_R_1.setNeutralMode(COAST_MODE)
            # self.talon_R_2.setNeutralMode(COAST_MODE)

        else:
            if not self.is_braking:
                # print("setting brake mode")
                self.talon_L_1.setNeutralMode(BRAKE_MODE)
                self.talon_L_2.setNeutralMode(BRAKE_MODE)
                self.talon_R_1.setNeutralMode(BRAKE_MODE)
                self.talon_R_2.setNeutralMode(BRAKE_MODE)
                self.is_braking = True
            # reset value to make robot stop moving
            self.drivetrain.set_motors(0.0, 0.0)
            #
            # self.talon_L_1.setNeutralMode(BRAKE_MODE)
            # self.talon_L_2.setNeutralMode(BRAKE_MODE)
            # self.talon_R_1.setNeutralMode(BRAKE_MODE)
            # self.talon_R_2.setNeutralMode(BRAKE_MODE)

            self.sd.putValue('Drivetrain: ', 'static')

        # boom extension: bumpers
        # NOTE: it is assumed that the boom arm is fully retracted
        wind_speed = 0

        if (self.drive_controller.getRightBumper()):
            wind_speed -= WINDING_SPEED

        if (self.drive_controller.getLeftBumper()):
            wind_speed += WINDING_SPEED

        self.boom_arm.set_extender(wind_speed, self.boom_extender_motor_encoder)

        # grabber: A button to open/close (switches from one state to another)
        if self.drive_controller.getAButtonReleased():
            self.grabber.solenoid_toggle()

        if self.drive_controller.getBButtonReleased():
            self.grabber.toggle_compressor()

        # if self.drive_controller.getYButton():
        #     aiming.side_to_side(self)
        #     aiming.forward_backward(self)

        if self.drive_controller.getRightStickButtonReleased():
            self.solenoid_gear.toggle()

        # if self.drive_controller.getLeftStickButtonReleased():
        #     self.talon_L_1.setNeutralMode(BRAKE_MODE)
        #     self.talon_L_2.setNeutralMode(BRAKE_MODE)
        #     self.talon_R_1.setNeutralMode(BRAKE_MODE)
        #     self.talon_R_2.setNeutralMode(BRAKE_MODE)
        # get hacked!

        if self.drive_controller.getXButton():
            self.gyro.balancing()

        if self.drive_controller.getStartButtonReleased():
            self.gyro.reset()

        if self.drive_controller.getXButton():
            self.gyro.balancing()
        if self.drive_controller.getStartButtonReleased():
            self.gyro.reset()

        if self.drive_controller.getBackButtonReleased():
            self.encoder.getValues()

        self.sd.putValue("rotator 1 encoder", self.boom_rotator_motor1.getSelectedSensorPosition())
        self.sd.putValue("rotator 2 encoder", self.boom_rotator_motor2.getSelectedSensorPosition())
        self.sd.putValue("average rotator encoder", (
                self.boom_rotator_motor1.getSelectedSensorPosition() + self.boom_rotator_motor2.getSelectedSensorPosition()) / 2)
        self.sd.putValue("rotator pid error", self.armPID.getPositionError())
        self.sd.putValue("rotator pid target", self.arm_pid_target)
        self.sd.putValue("rotator pid", self.arm_pid_output)
        self.sd.putValue("pid enabled", self.arm_pid_enabled)
            
            


if __name__ == '__main__':
    wpilib.run(SpartaBot)
