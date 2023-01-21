from wpilib import Spark
from networktables import NetworkTable

class Boom:

    # get sparks from main robot via variable injection
    boom_extender_spark: Spark
    boom_rotator_spark: Spark

    sd: NetworkTable

    def setup(self):
        """instead of __init__(), use setup() to initialize values (works with magicrobot variable injection)"""
        pass

    def set_extender(self):
        pass

    def set_rotator(self):
        pass

    def execute(self):
        pass