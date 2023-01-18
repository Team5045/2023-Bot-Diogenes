"""
This file runs the main loop of the robot and is responsible for connecting all other parts of the robot code together.

-----Usage-----
python py/robot/robot.py deploy --skip-tests
# Need to update this to make it automatically launch a .sh file




-----For first-time use-----


Download robotpy onto your computer:
py -3 -m pip install robotpy
    To upgrade, use:
    py -3 -m pip install --upgrade robotpy


Download and install all vendor dependencies and third-party software after re-imaging the RoboRIO:
py -3 -m robotpy_installer download-python
py -3 -m robotpy_installer install-python
py -3 -m robotpy_installer download robotpy
py -3 -m robotpy_installer install robotpy
py -3 -m robotpy_installer download robotpy[ctre]
py -3 -m robotpy_installer install robotpy[ctre]
py -3 -m robotpy_installer download robotpy[rev]
py -3 -m robotpy_installer install robotpy[rev]
"""

# MagicBot framework
