import wpilib
from wpilib import Solenoid, DoubleSolenoid
from components.drivetrain import DriveTrain
from networktables import NetworkTable

class Pneumatics:
    def setup(self):
        PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
        self.compressor = wpilib.Compressor(0, PNEUMATICS_MODULE_TYPE)
        self.solenoid = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 0, 1)
        self.solenoid.set(DoubleSolenoid.Value.kForward)