import wpilib
from ctre import WPI_TalonSRX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable
from wpilib import Solenoid, DoubleSolenoid
from components.drivetrain import DriveTrain
<<<<<<< HEAD
from components.pneumatics import Pneumatics

=======
from components.Grabber import Grabber
>>>>>>> main
import time

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
class SpartaBot(MagicRobot):

    # a DriveTrain instance is automatically created by MagicRobot
    drivetrain: DriveTrain
    pneumatics: Pneumatics

    def createObjects(self):
        '''Create motors and stuff here'''
        #drivetrain stuff
        NetworkTables.initialize(server='roborio-5045-frc.local')
        self.sd: NetworkTable = NetworkTables.getTable('SmartDashboard')

        self.drive_controller = wpilib.XboxController(0) #0 works for sim?

        self.talon_L_1 = WPI_TalonSRX(6)
        self.talon_L_2 = WPI_TalonSRX(9)

        self.talon_R_1 = WPI_TalonSRX(1)
        self.talon_R_2 = WPI_TalonSRX(5)

        #Pneumatics
        #In pneumatics.py


    def disabledPeriodic(self):
        self.sd.putValue("Mode", "Disabled")

    def teleopInit(self):
        '''Called when teleop starts; optional'''
        self.sd.putValue("Mode", "Teleop")

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        angle = self.drive_controller.getRightX()
        #print(self.drive_controller.getRawAxis(0))
        speed = self.drive_controller.getLeftY()
        try:
            if (abs(angle) > INPUT_SENSITIVITY or abs(speed) > INPUT_SENSITIVITY):
                # inverse values to get inverse controls
                self.drivetrain.set_motors(-speed, -angle)
                self.sd.putValue('Drivetrain: ', 'moving')

<<<<<<< HEAD
            else:
                # reset value to make robot stop moving
                self.drivetrain.set_motors(0.0, 0.0)
                self.sd.putValue('Drivetrain: ', 'static')
        except:
            self.onExcetption() #error swallower
        
        try:
            if self.drive_controller.getBButtonReleased():
                if (self.compressor.isEnabled()):
                    self.compressor.disable()
                else:
                    self.compressor.enableDigital()

            if self.drive_controller.getAButtonReleased():
                self.solenoid.toggle()
                print(self.solenoid.get())
        except:
            self.onException()


        
=======
        if (abs(angle) > INPUT_SENSITIVITY or abs(speed) > INPUT_SENSITIVITY):
            # inverse values to get inverse controls
            self.drivetrain.set_motors(-speed, -angle)
            self.sd.putValue('Drivetrain: ', 'moving')

        else:
            # reset value to make robot stop moving
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue('Drivetrain: ', 'static')

>>>>>>> main
        # self.drivetrain's execute() method is automatically called

        if self.drive_controller.getBButtonReleased():
            Grabber.turn_off_compressor(self)
        
        if self.drive_controller.getAButtonReleased():
            Grabber.solenoid_toggle(self)


if __name__ == '__main__':
    wpilib.run(SpartaBot)

#commands to remember
#py -3 robot.py sim