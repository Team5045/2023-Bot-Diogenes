# This is the file used to contain grabber, boom, etc. for autonomous
# This is going to be commented out for now as we do not currently have all the functions ready to test. 

from components.boom import Boom
from components.grabber import grabber
from components.drivetrain import DriveTrain
# Components imported from other directories

from magicbot import AutonomousStateMachine, tunable, state, timed_state
import wpilib
import rev
from ctre import WPI_TalonSRX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable
from wpilib import DoubleSolenoid
import wpilib.drive
import networktables

class score(AutonomousStateMachine):
    MODE_NAME = "score"
    DEFAULT = True
    sd: networktables.NetworkTable
    
    