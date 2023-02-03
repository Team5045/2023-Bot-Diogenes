import wpilib
from wpilib import DoubleSolenoid
from magicbot import MagicRobot


class grabber:

    def setup(self):

        PNEUMATICS_MODULE_TYPE = wpilib.PneumaticsModuleType.CTREPCM
        self.compressor = wpilib.Compressor(0, PNEUMATICS_MODULE_TYPE)
        self.solenoid = wpilib.DoubleSolenoid(PNEUMATICS_MODULE_TYPE, 0, 1)
        self.solenoid.set(DoubleSolenoid.Value.kForward)


    
    def turn_off_compressor(MagicRobot):
        if (MagicRobot.compressor.isEnabled()):
            MagicRobot.compressor.disable()
        else:
            MagicRobot.compressor.enableDigital()

    def solenoid_toggle(MagicRobot):
        MagicRobot.solenoid.toggle()







   
