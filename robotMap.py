from opentelemetry.trace import Tracer, propagation 
from opentelemetry.trace.span import Span
import opentelemetry.trace.span
from utils import configMapper
from wpilib import XboxController


class RobotMap():
    """
    Robot map gathers all the hard coded values needed to interface with
    hardware into a single location
    """
    def __init__(self, tracer):
        """intilize the robot map"""
        with tracer.start_as_current_span("RobotMap") as child:
            configFile, configPath = configMapper.findConfig()
            child.set_attribute("configFile", configFile)
            child.set_attribute("configPath", configPath)
            self.configMapper = configMapper.ConfigMapper(tracer, configFile, configPath)

class XboxMap():
    """
    Holds the mappings to TWO Xbox controllers, one for driving, one for mechanisms
    """
    def __init__(self, tracer, Xbox1: XboxController, Xbox2: XboxController):
        with tracer.start_as_current_span("XboxMap") as child:
            self.drive = Xbox1
            self.mech = Xbox2
            self.controllerInput()
            #Button mappings

    def controllerInput(self):
        """
        Collects all controller values and puts them in an easily readable format
        (Should only be used for axes while buttonManager has no equal for axes)
        """
        #Drive Controller inputs
        self.driveLeft = self.drive.getRawAxis(XboxController.Axis.kLeftY)
        self.driveRight = self.drive.getRawAxis(XboxController.Axis.kRightY)
        self.driveLeftHoriz = self.drive.getRawAxis(XboxController.Axis.kLeftX)
        self.driveRightHoriz = self.drive.getRawAxis(XboxController.Axis.kRightX)
        self.driveRightTrig = self.drive.getRawAxis(XboxController.Axis.kRightTrigger)
        self.driveLeftTrig = self.drive.getRawAxis(XboxController.Axis.kLeftTrigger)
        self.driveDPad = self.drive.getPOV()
        #Mechanism controller inputs
        self.mechLeft = self.mech.getRawAxis(XboxController.Axis.kLeftY)
        self.mechRight = self.mech.getRawAxis(XboxController.Axis.kRightY)
        self.mechLeftHoriz = self.mech.getRawAxis(XboxController.Axis.kLeftX)
        self.mechRightHoriz = self.mech.getRawAxis(XboxController.Axis.kRightX)
        self.mechRightTrig = self.mech.getRawAxis(XboxController.Axis.kRightTrigger)
        self.mechLeftTrig = self.mech.getRawAxis(XboxController.Axis.kLeftTrigger)
        self.mechDPad = self.mech.getPOV()

    def getDriveController(self):
        return self.drive

    def getMechController(self):
        return self.mech

    def getDriveLeft(self):
        return self.driveLeft

    def getDriveRight(self):
        return self.driveRight

    def getDriveLeftHoriz(self):
        return self.driveLeftHoriz

    def getDriveRightHoriz(self):
        return self.driveRightHoriz

    def getDriveRightTrig(self):
        return self.driveRightTrig

    def getDriveLeftTrig(self):
        return self.driveLeftTrig

    def getDriveDPad(self):
        return self.driveDPad

    def getMechLeft(self):
        return self.mechLeft

    def getMechRight(self):
        return self.mechRight

    def getMechLeftHoriz(self):
        return self.mechLeftHoriz

    def getMechRightHoriz(self):
        return self.mechRightHoriz

    def getMechRightTrig(self):
        return self.mechRightTrig

    def getMechLeftTrig(self):
        return self.mechLeftTrig

    def getMechDPad(self):
        return self.mechDPad
