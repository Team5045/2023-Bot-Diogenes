from wpimath.controller import PIDController
from magicbot import tunable
from networktables import NetworkTables
from components.boom import Boom
from ctre import WPI_TalonFX
from robotpy import d

class Rotate_Controller:

    boom_arm: Boom
    boom_rotator_motor: WPI_TalonFX
    
    rate = 0.5
    kP = 0
    kI = 0
    kD = 0
    kF = 0

    def setup(self):
        self.angle = None
        self.angle_controller = PIDController(
            Kp = self.kP,
            Ki=self.kI,
            Kd=self.kD,
            Kf=self.kF,
            source = self.get_angle,
            output = self.pid_Write_angle
        )

        self.angle_controller.setInputRange(-180, 180)
        self.angle_controller.setContinuous(True)
        self.angle_controller.setOutputRange(-self.rate, self.rate)
        
    
    def get_angle(self):
        self.boom_rotator_motor.getSelectedSensorPosition()

    def pid_Write_angle(self, rate):
        self.rate = rate
    
    def move(self, position):
        self.setpoint = position
        self.angle_controller.enable()
    
    def execute(self):
        if self.setpoint == self.get_angle:
            self.boom_rotator_motor.set(0)
            self.stop()
        else:
            self.boom_rotator_motor.set(self.rate)
            
    def stop(self):
        self.angle_controller.disable()
    
    def on_disable(self):
        self.stop()


