
import wpilib
import rev
from ctre import WPI_TalonFX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable
from wpilib import DoubleSolenoid

from components.drivetrain import DriveTrain

from components.boom import Boom
from components.grabber import Grabber
import wpilib.drive

from robotpy_ext.autonomous import AutonomousModeSelector

from components.LimeLight import aiming
from utilities.encoder import Encoder

from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive
from networktables import NetworkTable
from ctre import WPI_TalonFX


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


class SpartaBot(MagicRobot):

    # a DriveTrain instance is automatically created by MagicRobot

    drivetrain: DriveTrain
    boom_arm: Boom

    def createObjects(self):
        '''Create motors and stuff here'''

        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')
        

        self.drive_controller = wpilib.XboxController(0)  # 0 works for sim?

        self.talon_L_1 = WPI_TalonFX(4)
        self.talon_L_2 = WPI_TalonFX(8)

        self.talon_R_1 = WPI_TalonFX(7)
        self.talon_R_2 = WPI_TalonFX(6)

        self.talon_ENC1 = WPI_TalonSRX(0)
        self.talon_ENC2 = WPI_TalonSRX(12)


        self.compressor = wpilib.Compressor(0, PNEUMATICS_MODULE_TYPE)
        self.solenoid1 = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 2, 3)
        self.solenoid2 = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 6, 7)
        self.solenoid1.set(DoubleSolenoid.Value.kForward)
        self.solenoid2.set(DoubleSolenoid.Value.kForward)

        self.boom_extender_spark = rev.CANSparkMax(4, MOTOR_BRUSHLESS)
        self.boom_rotator_spark = rev.CANSparkMax(1, MOTOR_BRUSHLESS)

    def disabledPeriodic(self):
        self.sd.putValue("Mode", "Disabled")

    def teleopInit(self):
        self.sd.putValue("Mode", "Teleop")
        # self.limelight = NetworkTables.getTable("limelight")
        # self.limelight.LEDState(3)
        # print("limelight on")
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''
        Called on each iteration of the control loop\n
        NOTE: all components' execute() methods will be called automatically
        '''

        # drive controls

        angle = self.drive_controller.getRightX()
        speed = self.drive_controller.getLeftY()
        
        self.sensor = self.talon_ENC1.getSensorCollection()
        MotorPosL = self.sensor.getQuadraturePosition()

        self.sense = self.talon_ENC2.getSensorCollection()
        MotorPosR = self.sense.getQuadraturePosition()



        if (abs(angle) > INPUT_SENSITIVITY or abs(speed) > INPUT_SENSITIVITY):
            # inverse values to get inverse controls
            self.drivetrain.set_motors(-speed, angle)
            self.sd.putValue('Drivetrain: ', 'moving')

        else:
            # reset value to make robot stop moving
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue('Drivetrain: ', 'static')\




        # boom controls
        # if left bumper button pressed, right and left triggers control boom extension
        #   else, they control angle
        speed = 0


        speed += self.drive_controller.getRightTriggerAxis()
        speed -= self.drive_controller.getLeftTriggerAxis()

        self.boom_arm.set_extender(0)
        self.boom_arm.set_rotator(0)

        if (abs(speed) > INPUT_SENSITIVITY):
            if self.drive_controller.getLeftBumper():
                # limit is 0.15 of max speed (prevent overwinding)
                self.boom_arm.set_extender(3*speed/20)
            else:
                self.boom_arm.set_rotator(3*speed/20)

        # self.drivetrain's execute() method is automatically called

        if self.drive_controller.getLeftBumperReleased():
            Grabber.turn_off_compressor(self)

        if self.drive_controller.getRightBumperReleased():
            Grabber.solenoid_toggle(self)
        
        if self.drive_controller.getYButton():
            aiming.side_to_side(self)
            
        if self.drive_controller.getXButton():
            aiming.forward_backward(self)
        


if __name__ == '__main__':
    wpilib.run(SpartaBot)
