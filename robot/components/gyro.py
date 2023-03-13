import wpilib
import navx
from wpilib.interfaces import Gyro
from networktables import NetworkTable
from components.drivetrain import DriveTrain

class Gyro:

    drivetrain: DriveTrain
    sd: NetworkTable

#Gyro.calibrate() should be activated,
#but with a button or what?
    def setup(self): #hopefully this works
        self.gyro = navx._navx.AHRS.create_spi()
        self.angle = 0
        self.gain = 1
        self.pitch = self.gyro.getPitch()

        #getPitch() <-- get this, doing something with motor,
        #robot doesn't fall off platform

    def pitchmode(self):
        
        pitch = self.gyro.getPitch()
        if pitch > 10:
            self.drivetrain.set_motors(pitch * 0.05, 0.0)
            self.sd.putValue('Drivetrain: ', 'moving')

        else:
            # reset value to make robot stop moving
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue('Drivetrain: ', 'static')


        if pitch < -10: #this value is also made up
        # inverse values to get inverse controls
            self.drivetrain.set_motors(pitch * -0.05, 0.0)
            self.sd.putValue('Drivetrain: ', 'moving')

        else:
        # reset value to make robot stop moving
            self.drivetrain.set_motors(0.0, 0.0)
            self.sd.putValue('Drivetrain: ', 'static')

        
    def execute(self):

        """
        Reads the data from smartdashboard (set by control methods), and then sends data to output devices such as motors.
        Execute is called in telopPeriodic automatically; no need to manually call
        """


        