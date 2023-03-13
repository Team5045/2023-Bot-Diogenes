import wpilib
import navx
from wpilib.interfaces import Gyro
from networktables import NetworkTable

class Gryo:
#Gyro.calibrate() should be activated,
#but with a button or what?
    def setup(self): #hopefully this works
        self.gyro = navx.AHRS
        self.angle = 0
        self.gain = 1

        #getPitch() <-- get this, doing something with motor,
        #robot doesn't fall off platform
        
    def execute(self):
        pass
        """
        Reads the data from smartdashboard (set by control methods), and then sends data to output devices such as motors.
        Execute is called in telopPeriodic automatically; no need to manually call
        """


        