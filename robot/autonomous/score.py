# This is the file used to contain grabber, boom, etc. for autonomous

from components.boom import Boom
from components.grabber import grabber
from components.drivetrain import DriveTrain
# Components imported from other directories

from magicbot import AutonomousStateMachine, tunable, timed_state
import wpilib
import rev
from ctre import WPI_TalonSRX
from magicbot import MagicRobot
from networktables import NetworkTables, NetworkTable
from wpilib import DoubleSolenoid
import wpilib.drive

# class score(AutonomousStateMachine):
    