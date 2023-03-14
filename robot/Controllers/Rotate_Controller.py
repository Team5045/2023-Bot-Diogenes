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

"""A backport of the upcoming (in 2020) WPILib PIDController."""

__version__ = "0.7.1"

import math

from typing import ClassVar, Optional

import wpilib

__any__ = ("PIDController",)


#class PIDController(wpilib.SendableBase):
#    """Class implements a PID Control Loop."""
#
#    instances: ClassVar[int] = 0
#
#    #: Factor for "proportional" control
#    Kp: float
#    #: Factor for "integral" control
#    Ki: float
#    #: Factor for "derivative" control
#    Kd: float
#
#    #: The period (in seconds) of the loop that calls the controller
#    period: float
#
#    _maximum_integral: float = 1
#    _minimum_integral: float = -1
#    #: Maximum input - limit setpoint to this
#    _maximum_input: float = 0
#    #: Minimum input - limit setpoint to this
#    _minimum_input: float = 0
#    #: Input range - difference between maximum and minimum
#    _input_range: float = 0
#    #: Do the endpoints wrap around? eg. Absolute encoder
#    _continuous: bool = False
#
#    #: The error at the time of the most recent call to calculate()
#    _position_error: float = 0
#    _velocity_error: float = 0
#
#    #: The error at the time of the second-most-recent call to calculate() (used to compute velocity)
#    prev_error: float = math.inf
#
#    #: The sum of the errors for use in the integral calc
#    total_error: float = 0
#
#    #: The percentage or absolute error that is considered at setpoint.
#    _position_tolerance: float = 0.05
#    _velocity_tolerance: float = math.inf
#
#    setpoint: float = 0
#
#    def __init__(self, Kp: float, Ki: float, Kd: float, *, period: float = 0.02):
#        """Allocate a PID object with the given constants for Kp, Ki, and Kd.
#
#        :param Kp: The proportional coefficient.
#        :param Ki: The integral coefficient.
#        :param Kd: The derivative coefficient.
#        :param period: The period between controller updates in seconds.
#                       The default is 20ms.
#        """
#        super().__init__(addLiveWindow=False)
#
#        self.period = period
#        self.Kp = Kp
#        self.Ki = Ki
#        self.Kd = Kd
#
#        PIDController.instances += 1
#        self.setName("PIDController", PIDController.instances)
#
#    def setPID(self, Kp: float, Ki: float, Kd: float) -> None:
#        """Set the PID Controller gain parameters."""
#        self.Kp = Kp
#        self.Ki = Ki
#        self.Kd = Kd
#
#    def setP(self, Kp: float) -> None:
#        """Set the Proportional coefficient of the PID controller gain."""
#        self.Kp = Kp
#
#    def setI(self, Ki: float) -> None:
#        """Set the Integral coefficient of the PID controller gain."""
#        self.Ki = Ki
#
#    def setD(self, Kd: float) -> None:
#        """Set the Differential coefficient of the PID controller gain."""
#        self.Kd = Kd
#
#    def setSetpoint(self, setpoint: float) -> None:
#        """Set the setpoint for the PIDController."""
#        if self._maximum_input > self._minimum_input:
#            self.setpoint = self._clamp(
#                setpoint, self._minimum_input, self._maximum_input
#            )
#        else:
#            self.setpoint = setpoint
#
#    def atSetpoint(self) -> bool:
#        """
#        Return true if the error is within the percentage of the specified tolerances.
#
#        This will return false until at least one input value has been computed.
#        """
#        return (
#            abs(self._position_error) < self._position_tolerance
#            and abs(self._velocity_error) < self._velocity_tolerance
#        )
#
#    def _setInputRange(self, minimum_input: float, maximum_input: float) -> None:
#        """Sets the maximum and minimum values expected from the input.
#
#        :param minimum_input: The minimum value expected from the input.
#        :param maximum_input: The maximum value expected from the input.
#        """
#        self._minimum_input = minimum_input
#        self._maximum_input = maximum_input
#        self._input_range = maximum_input - minimum_input
#
#        # Clamp setpoint to new input
#        if maximum_input > minimum_input:
#            self.setpoint = self._clamp(self.setpoint, minimum_input, maximum_input)
#
#    def enableContinuousInput(self, minimum_input: float, maximum_input: float) -> None:
#        """Enable continuous input.
#
#        Rather than using the max and min input range as constraints, it
#        considers them to be the same point and automatically calculates
#        the shortest route to the setpoint.
#
#        :param minimum_input: The minimum value expected from the input.
#        :param maximum_input: The maximum value expected from the input.
#        """
#        self._continuous = True
#        self._setInputRange(minimum_input, maximum_input)
#
#    def disableContinuousInput(self) -> None:
#        """Disables continuous input."""
#        self._continuous = False
#
#    def setIntegratorRange(
#        self, minimum_integral: float, maximum_integral: float
#    ) -> None:
#        """Sets the minimum and maximum values for the integrator.
#
#        When the cap is reached, the integrator value is added to the controller
#        output rather than the integrator value times the integral gain.
#
#        :param minimum_integral: The minimum value of the integrator.
#        :param maximum_integral: The maximum value of the integrator.
#        """
#        self._minimum_integral = minimum_integral
#        self._maximum_integral = maximum_integral
#
#    def setTolerance(
#        self, position_tolerance: float, velocity_tolerance: float = math.inf
#    ) -> None:
#        """
#        Sets the error which is considered tolerable for use with atSetpoint().
#
#        :param position_tolerance: Position error which is tolerable.
#        :param velocity_tolerance: Velocity error which is tolerable.
#        """
#        self._position_tolerance = position_tolerance
#        self._velocity_tolerance = velocity_tolerance
#
#    def getPositionError(self) -> float:
#        """Returns the difference between the setpoint and the measurement."""
#        return self.getContinuousError(self._position_error)
#
#    def getVelocityError(self) -> float:
#        """Returns the velocity error."""
#        return self._velocity_error
#
#    def calculate(self, measurement: float, setpoint: Optional[float] = None) -> float:
#        """
#        Returns the next output of the PID controller.
#
#        :param measurement: The current measurement of the process variable.
#        :param setpoint: The new setpoint of the controller if specified.
#        """
#        if setpoint is not None:
#            self.setSetpoint(setpoint)
#
#        Ki = self.Ki
#
#        prev_error = self.prev_error = self._position_error
#        error = self._position_error = self.getContinuousError(
#            self.setpoint - measurement
#        )
#        period = self.period
#        vel_error = self._velocity_error = (error - prev_error) / period
#        total_error = self.total_error
#
#        if Ki:
#            total_error = self.total_error = self._clamp(
#                total_error + error * period,
#                self._minimum_integral / Ki,
#                self._maximum_integral / Ki,
#            )
#
#        return self.Kp * error + Ki * total_error + self.Kd * vel_error
#
#    def reset(self) -> None:
#        """Reset the previous error, the integral term, and disable the controller."""
#        self.prev_error = 0
#        self.total_error = 0
#
#    def initSendable(self, builder) -> None:
#        builder.setSmartDashboardType("PIDController")
#        builder.setSafeState(self.reset)
#        builder.addDoubleProperty("p", lambda: self.Kp, self.setP)
#        builder.addDoubleProperty("i", lambda: self.Ki, self.setI)
#        builder.addDoubleProperty("d", lambda: self.Kd, self.setD)
#        builder.addDoubleProperty("setpoint", lambda: self.setpoint, self.setSetpoint)
#
#    def getContinuousError(self, error: float) -> float:
#        """Wraps error around for continuous inputs.
#
#        The original error is returned if continuous mode is disabled.
#
#        :param error: The current error of the PID controller.
#        :return: Error for continuous inputs.
#        """
#        input_range = self._input_range
#        if self._continuous and input_range > 0:
#            error %= input_range
#            if error > input_range / 2:
#                return error - input_range
#
#        return error
#
#    @staticmethod
#    def _clamp(value: float, low: float, high: float) -> float:
#        return max(low, min(value, high))

