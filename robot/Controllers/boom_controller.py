import math
from wpimath.controller import PIDController
from components.boom import Boom



PICKUP_LOCATION  = None
DROPOFF_LOCATION = None


def sigmoid(x):
  return 2 / (1 + math.exp(0.0005*x)) - 1


class BoomController:
    boom_arm: Boom

    kP = 0.01
    kI = 0
    kD = 0.01

    def setup(self):

        self.setpoint = self.boom_arm.get_arm_angle()

        self.angle_controller = PIDController(
            Kp=self.kP,
            Ki=self.kI,
            Kd=self.kD,
        )

    def goto_setpoint(self):
        diff = self.angle_controller.calculate(self.boom_arm.get_arm_angle(), self.setpoint)
        speed = sigmoid(diff)
        self.boom_arm.set_rotator(speed)

    def use_current_setpoint(self):
        """Use the arm's current position as the setpoint"""
        self.setpoint = self.boom_arm.get_arm_angle()

    def set_setpoint(self, point):
        self.setpoint = point

    def execute(self):
        pass

