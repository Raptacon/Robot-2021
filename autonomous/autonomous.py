from magicbot import AutonomousStateMachine, tunable, timed_state, state
from networktables import NetworkTables as networktable
from wpilib import SendableChooser
from components.driveTrain import DriveTrain
from components.autoAlign import AutoAlign
from components.autoShoot import AutoShoot
from components.shooterLogic import ShooterLogic
from components.shooterMotors import ShooterMotorCreation
from components.pneumatics import Pneumatics
from components.ballCounter import ballCounter

class Autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    LCRDropDown: SendableChooser
    MODE_NAME = "Offseason Autonomous"
    DEFAULT = True
    autoAlign: AutoAlign
    autoShoot: AutoShoot
    driveTrain: DriveTrain
    shooter: ShooterLogic
    shooterMotors: ShooterMotorCreation
    pneumatics: Pneumatics
    drive_speed = tunable(.25)

    rpm = 0 # Choose this based on path

    @state(first=True)
    def turnToTargetShoot(self):
        """Uses limelight to align to target and shoot"""
        self.path = self.LCRDropDown.getSelected()
        self.autoAlign.setShootAfterComplete(True)
        self.autoShoot.setRPM(self.rpm)
        self.autoAlign.engage()
        if self.autoAlign.autoAlignFinished and self.autoShoot.finished and self.shooterLogic.finished:
            self.next_state("travel")
    
    @state
    def travel(self):
        """
        Follow an array of turns and lateral motion
        in order to find balls and shoot them.
        """