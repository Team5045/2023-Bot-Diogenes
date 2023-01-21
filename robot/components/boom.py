from wpilib import Spark


class Boom:

    boom_spark: Spark

    def setup(self):
        """instead of __init__(), use setup() to initialize values (works with magicirobot variable injection)"""
        pass

    def extend(self):
        """start extending the boom arm; keeps extending until told to do otherwise (or reaches max)"""
        pass

    def retract(self):
        """start retracting the boom arm; keeps retracting until told to do otherwise (or cannot anymore)"""
        pass

    def stop(self):
        """stop boom movement"""
        pass

    def execute(self):
        pass