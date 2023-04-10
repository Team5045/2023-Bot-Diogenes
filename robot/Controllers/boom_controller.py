import math
from wpimath.controller import PIDController
from magicbot import tunable
from networktables import NetworkTable
from ctre import WPI_TalonFX

from components.boom import Boom



def sigmoid(x):
  return 1 / (1 + math.exp(4*x)) - 0.5


class BoomController:
    boom_arm: Boom

    kP = 0.01
    kI = 0
    kD = 0.01

    def setup(self):

        self.setpoint = self.boom_arm.get_arm_angle()

        self.angle_controller = PIDController(
            Kp = self.kP,
            Ki=self.kI,
            Kd=self.kD,
        )

    def goto_setpoint(self):
        diff = self.angle_controller.calculate()
        speed = sigmoid(diff)
        self.boom_arm.set_rotator(speed)

