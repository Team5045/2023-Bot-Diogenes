import wpilib
import ctre
from ctre import TalonSRX
from components.drivetrain import DriveTrain

talon_ENC1 = TalonSRX(0)
talon_ENC2 = TalonSRX(12)

class Encoder():
    def getEncoderLeft(self):
        print("Left Side Values..")
        self.sensor = talon_ENC1.getSensorCollection()
        MotorPosL = self.sensor.getQuadraturePosition()
        print(MotorPosL)
        MotorVelL = self.sensor.getQuadratureVelocity()
        print(MotorVelL)

    def getEncoderRight(self):
        print("Right Side Values..")
        self.sense = talon_ENC2.getSensorCollection()
        MotorPosR = self.sense.getQuadraturePosition()
        print(MotorPosR)
        MotorVelR = self.sense.getQuadratureVelocity
        print(MotorVelR)



