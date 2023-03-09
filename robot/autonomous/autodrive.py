
# This file is used for the drivetrain for autonomous
from components.drivetrain import DriveTrain
# imported drivetrain from components folder

from magicbot import AutonomousStateMachine, tunable, state, timed_state
from networktables import NetworkTables, NetworkTable
import wpilib
import wpilib.drive
import networktables

class autoDrive(AutonomousStateMachine):
    DEFAULT = True
    MODE_NAME = "autodrive"
    sd: networktables.NetworkTable
    drivetrain: DriveTrain

    @timed_state(duration=3, next_state="complete", first=True)
    def goFoward(self):
        self.drivetrain.set_motors(0.5, 0.0)
        self.sd.putValue("Mode:", "Moving Forward")
    # First autonomous state, makes robot drive forward to get ready to score

    @state
    def complete(self):
        self.drivetrain.set_motors(0.0, 0.0)
        self.sd.putValue("Mode", "Autonomous Done")
    # Robot stops now that driving is finished, should then switch to teleop because magicbot









