import wpilib
import navx
from wpilib.interfaces import Gyro
from networktables import NetworkTable

class Gryo:
#Gyro.calibrate() should be activated,
#but with a button or what?
    def setup(self):
        self.calibrate() #hopefully this works
        self.gyro = navx.AHRS

        #getPitch() <-- get this, doing something with motor,
        #robot doesn't fall off platform
        
