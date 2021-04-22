import wpilib.drive
import logging as log
from enum import Enum, auto
from networktables import NetworkTables
from components.driveTrain import DriveTrain, ControlMode

class DriveTrainHandler():

    driveTrain: DriveTrain

    def on_enable(self):
        self.controlMode = ControlMode.kDisabled
        self.currentID = "None"
        self.input1 = 0
        self.input2 = 0

    def setDriveTrain(self, ID:str, controlMode:ControlMode, input1:float, input2:float):
        """
        Sets the drive train using controlMode and
        inputs IF the handler decides the call is worthy.
        """

        self.input1 = 0
        self.input2 = 0

        if self.checkWorthiness(ID):
            self.currentID = ID
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
        Right now our policies are rudimentary.
        """

        # Always accept joystick input
        # In order to prevent joystick from overriding everything,
        # joystick input should not be called while people aren't pressing
        # the joysticks. (Don't call when the joysticks are within a deadzone)
        if ID == "Joystick":
            return True
        elif "Component" in ID and self.currentID != "Joystick":
            return True
        else:
            return False

    def execute(self):
        self.driveTrain.__setControlMode__(self.controlMode)
        self.driveTrain.__genericSet__(self.input1, self.input2)
        self.currentID = "None"
