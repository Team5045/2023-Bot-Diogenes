"""
This file runs the main loop of the robot and is responsible for connecting all other parts of the robot code together.

-----Usage-----
python robot/robot.py deploy --skip-tests
# Need to update this to make it automatically launch a .sh file




-----For first-time use-----


Download robotpy onto your computer:
py -3 -m pip install robotpy
    To upgrade, use:
    py -3 -m pip install --upgrade robotpy


Download and install all vendor dependencies and third-party software after re-imaging the RoboRIO:
py -3 -m robotpy_installer download-python
py -3 -m robotpy_installer install-python
py -3 -m robotpy_installer download robotpy
py -3 -m robotpy_installer install robotpy
py -3 -m robotpy_installer download robotpy[ctre]
py -3 -m robotpy_installer install robotpy[ctre]
py -3 -m robotpy_installer download robotpy[rev]
py -3 -m robotpy_installer install robotpy[rev]
"""

# Import all the necessary libraries
import wpilib
import wpilib.drive
import rev




class MyRobot(wpilib.TimedRobot):
    """
    Main framework object that inherits from wpilib.TimedRobot
    """

    def robotInit(self):
        """
        This function is called upon program startup and
        should be used for any initialization code.
        """

        self.controller = wpilib.XboxController(0)

        self.boom_motor = rev.CANSparkMax(0, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushed)
        self.extender_motor = rev.CANSparkMax(1, rev._rev.CANSparkMaxLowLevel.MotorType.kBrushed)


    def autonomousInit(self):
        """This function is run once each time the robot enters autonomous mode."""
        # trust auton work

    def autonomousPeriodic(self):
        """This function is called periodically during autonomous."""
        # this will def make auton actually work

    def teleopPeriodic(self):
        """This function is called periodically during operator control."""

        # Print both controller values
        self.X = self.controller.getLeftTriggerAxis()
        self.Y = self.controller.getRightTriggerAxis()

        print(f"Left Trigger: {self.X}\nRight Trigger: {self.Y}")




if __name__ == "__main__":
    wpilib.run(MyRobot)
