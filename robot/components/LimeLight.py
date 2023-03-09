# To-do List for Limelight--------------------------------------------------------------------
# Factor in April Tags? (Limelight 3.0 required)\
# Install the limelight on the robot for testing
# Figure out how to manage the limelight LED stat frrom controller
# --------------------------------------------------------------------------------------------

import networktables
import wpilib.drive
import wpilib
from networktables import NetworkTables
from components.drivetrain import DriveTrain

LED_ON = 1
LED_OFF = 0
LED_PartialRight = 2
LED_PartialLeft = 3
# Uh idk really how to turn on limelight in the code yet so ima just use the limelight finder tool to do that for now

class aiming:
    table = NetworkTables.getTable("Limelight")
    drivetrain: DriveTrain
    # Pulls values for limelight
    tx = table.getNumber('tx', None)
    ty = table.getNumber('ty', None)
    ta = table.getNumber('ta', None)
    ts = table.getNumber('ts', None)
    # Above values are just the value assignments that limeight reads, see limelight finder for specifics

    def side_to_side(self):
        try:
            self.turn = self.table.getNumber('tx', None) / 30.75
            print(f"turn {self.turn}")
            # self.drive.arcadeDrive(self.turn, 0)
        except Exception as e:
            print(e + "Did not work! (Type 1)")

    def forward_backward(self):
        try:
            self.move = self.table.getNumber('ta', None)
            print(f"move {self.move}")
            if self.move < 10:
                # self.drivetrain.set_motors(0.5, 0.0)
                pass
            elif self.move > 10:
                # self.drivetrain.set_motors(-0,5, 0)
                pass
        except Exception as e:
            print(e + "Did not work (Type 2)")





