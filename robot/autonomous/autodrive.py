
# This file is used for the drivetrain for autonomous
from components.drivetrain import DriveTrain
# imported drivetrain from components folder

from magicbot import AutonomousStateMachine, tunable, timed_state
from networktables import NetworkTables, NetworkTable
import wpilib
import wpilib.drive

class autoDrive(AutonomousStateMachine):

    # Using the built in variable injection from magicbot
    MODE_NAME = "autodrive"
    DEFAULT = True

    @timed_state(duration=2, next_state="ChargePad")
    def goFoward(self):
        self.drive.arcadeDrive(0.5, 0, True)
    # First autonomous state, makes robot drive forward to get ready to score
    
    @timed_state(duartion=3, next_state="done")
    def ChargePad(self):
        self.drive.arcadeDrive(-0.5, 0, True)
    # Second autonomous state, makes robot drive backward, HOPEFULLY, to get to the charge station
    @timed_state(duration=10)
    def done(self):
        self.drive.arcadeDrive(0, 0, True)
    # Robot stops now that driving is finished, should then switch to teleop because magicbot









