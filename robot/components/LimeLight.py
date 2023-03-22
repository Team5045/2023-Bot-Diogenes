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
    limelight = NetworkTables.getTable("limelight")
    sd = NetworkTables.getTable('SmartDashboard')
    drivetrain: DriveTrain
    # Pulls values for limelight
    tx = limelight.getNumber('tx', None)
    ty = limelight.getNumber('ty', None)
    ta = limelight.getNumber('ta', None)
    ts = limelight.getNumber('ts', None)
    # Above values are just the value assignments that limeight reads, see limelight finder for specifics
    sd: networktables.NetworkTable

    def side_to_side(self):
        try:
            self.turn = NetworkTables.getTable("limelight").getNumber('tx', None) / 30.75
            self.sd.putValue("Limelight LR", self.turn)
            self.drivetrain.set_motors(0, self.turn)
            print(f"Limelight LR {self.turn}")
        except Exception as e:
            print(str(e))

    def forward_backward(self):
        try:
            self.move = NetworkTables.getTable("limelight").getNumber('ta', None)
            if abs(self.move) > 0.05:
                if abs(self.move) > 1:
                    if (self.move < 0):
                        self.drivetrain.set_motors(-0.8, 0)
                    else:
                        self.drivetrain.set_motors(0.8, 0)
                self.drivetrain.set_motors(self.move * 0.8, 0)

            if self.move < 10:
                self.sd.putValue("Limelight FB", "forward")
            elif self.move > 10:
                self.sd.putValue("Limelight FB", "backward")
            else:
                self.sd.putValue("Limelight FB", "perfect!")
        except Exception as e:
            print(str(e))
