import wpilib
import ctre
from ctre import TalonSRX
from components.drivetrain import DriveTrain
import networktables
from networktables import NetworkTable

talon_ENC1 = TalonSRX(0)
talon_ENC2 = TalonSRX(12)

class Encoder():
    sd: NetworkTable 
    def setup(self):
        self.sensor1 = talon_ENC1.getSensorCollection()
        self.sensor2 = talon_ENC2.getSensorCollection()

    def getEncoderLeft(self):
        self.sd.putValue("Event: ", "Getting LEFT Encoder Values")
        print("Left Side Values..")

        MotorPosL = self.sensor1.getQuadraturePosition()
        print(MotorPosL)

        MotorVelL = self.sensor1.getQuadratureVelocity()
        print(MotorVelL)
        return()

    def getEncoderRight(self):
        self.sd.putValue("Event: ", "Getting RIGHT Encoder Values")
        print("Right Side Values..")

        MotorPosR = self.sensor2.getQuadraturePosition()
        print(MotorPosR)

        MotorVelR = self.sensor2.getQuadratureVelocity
        print(MotorVelR)
        return()



