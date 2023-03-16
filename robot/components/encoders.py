import wpilib
from ctre import TalonSRX
import networktables
from networktables import NetworkTable

LeftEncoder = TalonSRX(0)
RightEncoder = TalonSRX(1)

class encoders():
    # Left encoder values getting from here
    def left(self):
        self.senseleft = LeftEncoder.getSensorCollection()
        print(self.senseleft.getQuadratureVelocity())
    
    # Right encoder values getting from here
    def right(self):
        self.senseright = RightEncoder.getSensorCollection()
        print(self.senseright.getQuadratureVelocity())
