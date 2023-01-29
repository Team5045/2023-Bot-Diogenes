import wpilib
from wpilib import Solenoid, DoubleSolenoid
from components.drivetrain import DriveTrain
from networktables import NetworkTable

class Pneumatics:
    def setup(self):
        PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
        self.compressor = wpilib.Compressor(0, PNEUMATICS_MODULE_TYPE)
        self.solenoid = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 0, 1)
<<<<<<< HEAD
        self.solenoid.set(DoubleSolenoid.Value.kForward)
=======
        self.solenoid.set(DoubleSolenoid.Value.kForward)
>>>>>>> f608085f7a7aa60fb7860bb53b193be5b2031b8c
