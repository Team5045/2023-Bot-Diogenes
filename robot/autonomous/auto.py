# Non-Magnolia Autonomous
import networktables
import rev
from components.boom import Boom
from components.drivetrain import DriveTrain
from components.encoders import Encoder
from components.grabber import Grabber
from components.gyro import Gyro
from controllers.boom_controller import BoomController
from ctre import NeutralMode
from magicbot import AutonomousStateMachine, state, timed_state
import navx

BRAKE_MODE = NeutralMode(2)
COAST_MODE = NeutralMode(1)
# ARM_ENCODER = 

class Autonomous(AutonomousStateMachine):
    DEFAULT = True
    MODE_NAME = "auton"
    sd: networktables.NetworkTable
    drivetrain: DriveTrain
    boom_arm: Boom
    grabber: Grabber
    gyro: Gyro
    encoder: Encoder
    boom_extender_motor_encoder: rev.SparkMaxRelativeEncoder
    boom_controller: BoomController
    

    @state(first = True)
    def initial(self):
            # Gyro is initialized/calibrated
        self.navx = navx.AHRS.create_spi()
        self.gyro.reset()

        '''NOTE: ENCODER POSITIONS NEED TO BE INITIALIZED'''
        self.boom_extender_motor_encoder.setPosition(0)
            # For the Drivetrain
        self.drivetrain.drivetrain_encoder_right.setPosition(0)
        self.drivetrain.drivetrain_encoder_left.setPosition(0)
            # For the Rotator
        self.boom_arm.boom_rotator_motor1.setSelectedSensorPosition(0) # Memphis Pyramid no lai
        self.boom_arm.boom_rotator_motor2.setSelectedSensorPosition(0)
        self.sd.putValue("Auton_Status: ", "Starting")
        self.next_state("Raise1")

    ''' NOTE: TO SELF: ROT_AVG and settarget are USING PLACEHOLDERS, MAKE SURE TO TEST FOR VALUES LATER!!!! '''

    @state
    def Raise1(self):
        ROT_AVG = (self.boom_arm.boom_rotator_motor1.getSelectedSensorPosition() + 
                   self.boom_arm.boom_rotator_motor2.getSelectedSensorPosition()) / 2
        if ROT_AVG != 0:
            self.boom_controller.set_target(1000)
            self.sd.putValue("Auton_Status: ", "Initial Rotate")
        else:
            self.boom_controller.set_target(0)
            self.sd.putValue("Auton_Status: ", "SUCCESS!")
            self.next_state("grab1")

    @state
    def grab1(self):
        self.grabber.solenoid_toggle()
        self.sd.putValue("Auton_Status: ", "Grabbing")
        self.next_state("Raise2")

    @state
    def Raise2(self):
        ROT_AVG2 = (self.boom_arm.boom_rotator_motor1.getSelectedSensorPosition() + 
                   self.boom_arm.boom_rotator_motor2.getSelectedSensorPosition()) / 2
        if ROT_AVG2 != 0:
            self.boom_controller.set_target(0)
            self.sd.putValue("Auton_Status: ", "Raising Arm")
        else:
            self.boom_controller.set_target(0)
            self.sd.putValue("Auton_Status: ", "Success!")
            self.next_state("drop1")
            # NOTE: These statements are a bit janky, but its a redundancy
    
    @state
    def drop1(self):
        self.grabber.solenoid_toggle()
        self.sd.putValue("Auton_Status: ", "Dropping.")
        self.next_state("retract")
    
    @state 
    def retract(self):
        self.boom_controller.set_target(2000) # Again, placeholder
        self.grabber.solenoid_toggle() # This prevents grabber damage 
        self.sd.putValue("Auton_Status: ", "Retracting")
        self.next_state("driveback_1")

    @timed_state(duration = 2, next_state = "done")
    def driveback_1(self):
        self.drivetrain.set_motors(-0.6, 0.0)
        self.sd.putValue("Auton_Status: ", "Driving Back")

    @state
    def done(self):
        self.drivetrain.set_motors(0.0, 0.0)
        self.sd.putValue("Auton_Status: ", "Auton Done")
        
    