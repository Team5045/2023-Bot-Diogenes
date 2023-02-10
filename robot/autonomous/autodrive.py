
# This file is used for the drivetrain for autonomous
from components.drivetrain import DriveTrain
# imported drivetrain from components folder

from magicbot import AutonomousStateMachine, tunable, state, timed_state
import wpilib.drive
import networktables


class autoDrive(AutonomousStateMachine):
    DEFAULT = True
    MODE_NAME = "autodrive"
    sd: networktables.NetworkTable
    drivetrain: DriveTrain

    @timed_state(duration=4, next_state="turnaround", first=True)
    def goFoward(self):
        self.drivetrain.set_motors(0.5, 0.0)
        self.sd.putValue("Mode:", "Moving Forward")
    # First autonomous state, makes robot drive forward to get ready to score

    @timed_state(duration=3, next_state="ChargePad")
    def Wait1(self):
        self.drivetrain.set_motors(0.0, 0.0)
        self.sd.putValue("Mode", "Waiting...")
    # Waiting while other functions exist

    @timed_state(duration=4, next_state="complete")
    def ChargePad(self):
        self.drivetrain.set_motors(0.5, 0.0)
        self.sd.putValue("Mode", "Moving Back")
    # Second autonomous state, makes robot drive backward, HOPEFULLY, to get to the charge station

    @state
    def complete(self):
        self.drivetrain.set_motors(0.0, 0.0)
        self.sd.putValue("Mode", "Autonomous Done")
    # Robot stops now that driving is finished, should then switch to teleop because magicbot
