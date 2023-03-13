import wpilib
from wpilib import DoubleSolenoid
from magicbot import MagicRobot


class Grabber:

    def setup(self):

        PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
        self.compressor = wpilib.Compressor(0, PNEUMATICS_MODULE_TYPE)
        self.solenoid1 = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 2, 3)
        self.solenoid2 = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 6, 7)
        self.solenoid1.set(DoubleSolenoid.Value.kForward)
        self.solenoid2.set(DoubleSolenoid.Value.kForward)

    def turn_off_compressor(MagicRobot):
        if (MagicRobot.compressor.isEnabled()):
            MagicRobot.compressor.disable()
        else:
            MagicRobot.compressor.enableDigital()

    def solenoid_toggle(MagicRobot):
        MagicRobot.solenoid1.toggle()
        MagicRobot.solenoid2.toggle()
