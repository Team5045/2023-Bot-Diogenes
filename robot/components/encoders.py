import wpilib
from ctre import TalonFX
from magicbot import MagicRobot

class Encoder():
    
    def setup(self):
        Talon_RE = TalonFX(2)
        Talon_LE = TalonFX(1)
        self.encoderR = Talon_RE
        self.encoderL = Talon_LE
    
    def getValues(self):
        # Getting information from the right gearbox TalonFX
        PositionRight = self.encoderR.getSelectedSensorPosition()
        VelocityRight = self.encoderR.getSelectedSensorVelocity()
        print(f'POSITION(right): {PositionRight}')
        print(f'VELOCITY(right): {VelocityRight}')

        # Getting information from the left gearbox TalonFX
        PositionLeft = self.encoderL.getSelectedSensorPosition() 
        VelocityLeft = self.encoderL.getSelectedSensorVelocity()
        print(f'POSITION(left): {PositionLeft}')
        print(f'VELOCITY(left): {VelocityLeft}')
        
    def execute(self):
        pass

        
