import wpilib
from wpilib import DoubleSolenoid
from magicbot import MagicRobot


class Grabber:

    compressor : wpilib.Compressor
    solenoid1 : wpilib.DoubleSolenoid
    solenoid_gear : wpilib.DoubleSolenoid


    def setup(self):
        pass

    def toggle_compressor(self):
        if (self.compressor.isEnabled()):
            self.compressor.disable()
        else:
            self.compressor.enableDigital()

    def solenoid_toggle(self):
        self.solenoid1.toggle()

    def shift_gears(self):
        self.solenoid_gear.toggle()


    def execute(self):
        pass
