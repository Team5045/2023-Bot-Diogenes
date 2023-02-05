import wpilib
import wpilib.drive
import robotpy
import ctre
import timer
import networktables
import components.Limelight

# Future To-Do List: Goals for Auton
# 1. Gyro? Could make good use for charge station
# 2. Limelight, integrate Allen's new limeight function within auton for a better optimization :)

class autonomous:
    def auto1TRUE(self):
        self.drivetrain.set_motors(0.5, 0)
        self.sd.putValue("Drivetrain: ", "First Auton State...")
    def auto1FALSE(self):
        self.drivetrain.set_motors(0.0, 0.0)
        self.sd.putValue("Drivetrain:", "First State Finished")

    def auto2TRUE(self):
        self.drivetrain.set_motors(-0.5, 0)
        self.sd.putValue("Drivetrain: ", "Second Auton State...")

    def auto2FALSE(self):
        self.drivetrain.set_motors(0.0, 0)
        self.sd.putValue("Drivetrain: ", "Auton Completed, Moving to teleop")

# To be continued with features like grabber, etc.