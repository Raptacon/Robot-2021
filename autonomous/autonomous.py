from magicbot import AutonomousStateMachine, tunable, timed_state, state
from networktables import NetworkTables as networktable
from wpilib import SendableChooser
from components.driveTrainGoToDist import GoToDist
from components.turnToAngle import TurnToAngle
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
    goToDist: GoToDist
    turnToAngle: TurnToAngle
    shooter: ShooterLogic
    shooterMotors: ShooterMotorCreation
    pneumatics: Pneumatics
    drive_speed = tunable(.25)

    rpm = 0 # Choose this based on path
    CenterRPM = 5000 # Placeholder

    # travelArray = [] # Build this based on path
    dumbSpeedSections = [[10, .5], [5, .3], [2, .1]] # Will probably need fixes
    travelArray = [["turnAbs", 180], ["forward", 5]]
    centerTA = []

    @state#(first=True)
    def determinePath(self):
        self.path = self.LCRDropDown.getSelected()
        if self.path == "Right":
            self.rpm = 0
            self.travelArray = self.rightTA
        elif self.path == "Center":
            self.rpm = self.CenterRPM
            self.travelArray = self.centerTA
        else:
            # On Left path, the distance should be estimated
            self.rpm = 0
        self.autoShoot.setRPM(self.rpm)

        self.next_state("turnToTargetShoot")

    @state
    def turnToTargetShoot(self):
        """Uses limelight to align to target and shoot"""

        self.autoAlign.setShootAfterComplete(True)
        self.autoAlign.engage()
        if self.autoAlign.autoAlignFinished and self.autoShoot.finished and self.shooter.finished:
            self.next_state("travel")
        else:
            self.next_state("turnToTargetShoot")
    
    @state(first=True)
    def travel(self):
        """
        Follow an array of turns and lateral motions
        in order to find balls and shoot them.
        """
        self.goToDist.setDumbSpeedSections(self.dumbSpeedSections)
        
        self.turnToAngle.setTurnAngle(180)
        self.turnToAngle.execute()
        self.next_state("travel")
        # for motion in self.travelArray:
        #     if motion[0] == "turnAbs":
        #         self.turnToAngle.setTurnAngle(motion[1])
        #     elif motion[0] == "forward":
        #         self.goToDist.setTargetDist(motion[1], True)