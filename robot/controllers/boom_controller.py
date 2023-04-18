'''PID controller for arm rotations'''
# package imports
import rev
from wpimath.controller import PIDController

# component imports
from components.boom import Boom

PID_TARGET_INPUT_MULTIPLIER = 1000
PID_FRONT_TARGET_LIMIT = -90000

class BoomController():

    # magicbot is cool like that
    boom_arm: Boom
    boom_extender_motor_encoder: rev.SparkMaxRelativeEncoder

    def setup(self):
        self.armPID = PIDController(0.00002, 0.00004, 0.000001, 0.02)
        self.armPID.setTolerance(50)
        self.pidOutput = 0
        self.pidEnabled = False
        self.boom_extender_motor_encoder.setPosition(0)
        self.boom_arm.boom_rotator_motor1.setSelectedSensorPosition(0)
        self.boom_arm.boom_rotator_motor2.setSelectedSensorPosition(0)
        self.armPID.reset()
        self.pidTarget = -3000

    def toggle_pid(self) -> None:

        # Toggles the PID state(on/off)
        self.pidEnabled = not self.pidEnabled
        if self.pidEnabled:
            self.pidTarget = (
                 self.boom_arm.boom_rotator_motor1.getSelectedSensorPosition() +
                   self.boom_arm.boom_rotator_motor2.getSelectedSensorPosition()) / 2
            self.armPID.setSetpoint(self.pidTarget)
            self.pidEnabled = True
            self.armPID.reset()

    def set_target(self, pidTarget) -> None:
        
        # Sets the PID Value, see robot.py
        if (self.pidTarget < PID_FRONT_TARGET_LIMIT):
            self.pidTarget = PID_FRONT_TARGET_LIMIT
        if (self.pidTarget > -1100):
            self.pidTarget = -1100
        self.armPID.setSetpoint(pidTarget)
        if not self.pidEnabled:
            pidTarget = (
                self.boom_arm.boom_rotator_motor1.getSelectedSensorPosition() +
                  self.boom_arm.boom_rotator_motor2.getSelectedSensorPosition()) / 2
            self.armPID.setSetpoint(pidTarget)
            self.pidEnabled = True
            self.armPID.reset()

    def execute(self):
        pass

