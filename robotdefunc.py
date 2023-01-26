#py -3 robot.py sim

import ctre
import magicbot
#import navx
import wpilib.drive
# from enum import IntEnum
# from wpilib import XboxController
# #from components import shooterFalcon, elevator #, shifter, intake, tower
# #from components.shooterFalcon import Shooter
# from wpilib.drive import DifferentialDrive
# from networktables import NetworkTables
# from magicbot import timed_state, state


# cond = threading.Condition()
# notified = [False]

# def connectionListener(connected, info):
#     print(info, '; Connected=%s' % connected)
#     with cond:
#         notified[0] = True
#         cond.notify()

# NetworkTables.initialize(server='10.50.45.2')
# NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)

# with cond:
#     print("Waiting")
#     if not notified[0]:
#         cond.wait()
'''
NetworkTables.initialize(server='roborio-5045-frc.local')
sd = NetworkTables.getTable('SmartDashboard')
sd.putNumber('someNumber', 1234)
otherNumber = sd.getNumber('otherNumber')py -3 robot.py sim
'''
# xbox =  wpilib.XboxController(0)

# class xboxthing:
#     def __init___(self):
#         self.CONTROLLER_LEFT = wpilib.XboxController.getLeftX()
#         self.CONTROLLER_RIGHT = wpilib.XboxController.getRightY()

# ys = self.drive.arcadeDrive(-self.drive_controller.getY()) #, self.drive_controller.getX()
# xs = self.drive.arcadeDrive(-self.driveStick.getX())

class SpartaBot(magicbot.MagicRobot):

    def createObjects(self):       
        # self.value = DoubleSolenoid.Value.kForward
        # self.outin = DoubleSolenoid.Value.kForward
        self.drive_controller = wpilib.XboxController(0)

        #drivetrain
        self.drivetrain_left_motor_slave = ctre.WPI_TalonSRX(6)
        self.drivetrain_left_motor_slave2 = ctre.WPI_TalonSRX(9)
        self.left = wpilib.MotorControllerGroup(self.drivetrain_left_motor_slave, self.drivetrain_left_motor_slave2)

        self.drivetrain_right_motor_slave = ctre.WPI_TalonSRX(1)
        self.drivetrain_right_motor_slave2 = ctre.WPI_TalonSRX(5)
        self.right = wpilib.MotorControllerGroup(self.drivetrain_right_motor_slave, self.drivetrain_right_motor_slave2)
        #self.left = wpilib.MotorcontrollerGroup(self.drivetrain_left_motor_slave, self.drivetrain_left_motor_slave2)
        #self.right = wpilib.MotorControllerGroup( self.drivetrain_right_motor_slave, self.drivetrain_right_motor_slave2)
        self.drive = wpilib.drive.DifferentialDrive(self.left, self.right)
        self.drive.setExpiration(0.1)

        # self.shifter_shiftsolenoid = wpilib.Solenoid(1)

    def teleopPeriodic(self):
    


        #ys = self.drive.arcadeDrive(-self.drive_controller.getY()) #, self.drive_controller.getX()
        #xs = self.drive.arcadeDrive(-self.driveStick.getX())
        # fuckidk = xboxthing()
        try:

            speed = self.drive_controller.getLeftX()
            angle = self.drive_controller.getRightY()
            #print(speed)
            #print(angle)
            if (abs(angle) > 0.05 or abs(speed) > 0.05):
                self.drive.arcadeDrive(-speed, -angle, True) 
            else:
                self.drive.arcadeDrive(0, 0, True)
        except:
            self.onException()

if __name__ == '__main__':
    wpilib.run(SpartaBot)

print("Connected!")

#py -3 robot.py sim

#py -3 robot.py deploy

#figure out what ssh is and how to connect it with roborio
