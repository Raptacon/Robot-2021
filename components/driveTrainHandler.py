import wpilib.drive
import logging as log
from enum import Enum, auto
from networktables import NetworkTables
from components.driveTrain import DriveTrain, ControlMode

class DriveTrainHandler():

    driveTrain: DriveTrain

    def on_enable(self):
        self.controlMode = ControlMode.kDisabled
        self.input1 = 0
        self.input2 = 0

    def setDriveTrain(self, ID:str, controlMode:ControlMode, input1:float, input2:float):
        """
        Sets the drive train using controlMode and
        inputs IF the handler decides the call is worthy.
        """
        if self.checkWorthiness(ID):
            self.controlMode = controlMode
            self.input1 = input1
            self.input2 = input2
        else:
            log.info(ID + " called setDriveTrain() but was not deemed worthy.")

    def checkWorthiness(self, ID:str):
        """
        Determines if a given ID is worthy.
        This (should be) determined based off of whether
        the joysticks have input as well as if autonomous
        code is running.
        Right now everything is worthy.
        """
        return True

    def execute(self):
        self.driveTrain.__setControlMode__(self.controlMode)
        self.driveTrain.__genericSet__(self.input1, self.input2)
