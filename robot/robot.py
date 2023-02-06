import wpilib
import rev
from ctre import WPI_TalonSRX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable
from wpilib import DoubleSolenoid
from components.drivetrain import DriveTrain

import time
from components.boom import Boom
from components.grabber import grabber

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

PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
MOTOR_BRUSHED = rev._rev.CANSparkMaxLowLevel.MotorType.kBrushed

MagicRobot.control_loop_wait_time = 0.05
class SpartaBot(MagicRobot):

    # a DriveTrain instance is automatically created by MagicRobot
    drivetrain: DriveTrain
    boom_arm: Boom

    def createObjects(self):
        '''Create motors and stuff here'''

        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')

        self.drive_controller = wpilib.XboxController(0) #0 works for sim?

        self.talon_L_1 = WPI_TalonSRX(1)
        self.talon_L_2 = WPI_TalonSRX(5)

        self.talon_R_1 = WPI_TalonSRX(6)
        self.talon_R_2 = WPI_TalonSRX(9)

        self.compressor = wpilib.Compressor(0, PNEUMATICS_MODULE_TYPE)
        self.solenoid = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 0, 1)
        self.solenoid.set(DoubleSolenoid.Value.kForward)

        self.boom_extender_spark: rev.CANSparkMax = rev.CANSparkMax(1, MOTOR_BRUSHED)
        self.boom_rotator_spark: rev.CANSparkMax = rev.CANSparkMax(2, MOTOR_BRUSHED)

    def disabledPeriodic(self):
        self.sd.putValue("Mode", "Disabled")

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.sd.putValue("Mode", "Teleop")

    def teleopPeriodic(self):
        '''
        Called on each iteration of the control loop\n
        NOTE: all components' execute() methods will be called automatically
        '''

        # drive controls

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

        if (self.drive_controller.getLeftBumper()):
            #extend_speed = 0

            # left trigger retracts, while right trigger extends
            self.boom_arm.extender_speed -= self.drive_controller.getLeftTriggerAxis()
            self.boom_arm.extender_speed += self.drive_controller.getRightTriggerAxis()

            #self.boom_arm.set_extender(extend_speed)
            
        elif self.drive_controller.getRightTriggerAxis() > 0.05:
            self.boom_arm.rotator_speed = self.drive_controller.getRightTriggerAxis()/10

        elif self.drive_controller.getLeftTriggerAxis() > 0.05:
            self.boom_arm.rotator_speed = -self.drive_controller.getLeftTriggerAxis()/10

        else:
            self.boom_arm.rotator_speed = 0
            self.boom_arm.extender_speed = 0
            
        
        if self.drive_controller.getBButtonReleased():
            grabber.turn_off_compressor(self)
        
        if self.drive_controller.getAButtonReleased():
            grabber.solenoid_toggle(self)


if __name__ == '__main__':
    wpilib.run(SpartaBot)