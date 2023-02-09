
# This file is used for the drivetrain for autonomous
from components.drivetrain import DriveTrain
# imported drivetrain from components folder

from magicbot import AutonomousStateMachine, tunable, state, timed_state
from networktables import NetworkTables, NetworkTable
import wpilib
import wpilib.drive
import networktables

MODE_NAME = "autodrive"
DEFAULT = True
sd: networktables.NetworkTable
drive: DriveTrain
# Using the built in variable injection from magicbot

class autoDrive(AutonomousStateMachine):
    @timed_state(duration=2, next_state="Wait1")
    def goFoward(self):
        self.drive.arcadeDrive(0.5, 0, True)
        self.sd.putValue("Mode:", "Moving Forward")
    # First autonomous state, makes robot drive forward to get ready to score
    
    @timed_state(duration=3, next_state="ChargePad")
    def Wait1(self):
        self.drive.arcadeDrive(0.0, 0.0, True)
        self.sd.putValue("Mode", "Waiting...")
    #Waiting while other functions exist
    
    @timed_state(duartion=3, next_state="done")
    def ChargePad(self):
        self.drive.arcadeDrive(-0.5, 0, True)
        self.sd.putValue("Mode", "Moving Back")
    # Second autonomous state, makes robot drive backward, HOPEFULLY, to get to the charge station
    @state
    def done(self):
        self.drive.arcadeDrive(0, 0, True)
        self.sd.putValue("Mode", "Autonomous Done")
    # Robot stops now that driving is finished, should then switch to teleop because magicbot









