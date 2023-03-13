from magicbot import AutonomousStateMachine, tunable, state, timed_state
import networktables
from networktables import NetworkTable

class autograb(AutonomousStateMachine):
    DEFAULT = True
    MODE_NAME = "autograb"
    
    # @timed_state()