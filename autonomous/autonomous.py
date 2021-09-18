from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.driveTrain import DriveTrain
from components.shooterLogic import ShooterLogic
from components.shooterMotors import ShooterMotorCreation
from components.pneumatics import Pneumatics
from components.driveTrainGoToDist import GoToDist

class Autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    time = 1.4
    MODE_NAME = "Basic Autonomous"
    DEFAULT = True
    driveTrain: DriveTrain
    shooter: ShooterLogic
    shooterMotors: ShooterMotorCreation
    pneumatics: Pneumatics
    goToDist: GoToDist
    drive_speed = tunable(.25)

    @state(first = True)
    def engage_shooter(self):
        """Starts shooter and fires"""
        self.driveTrain.execute()
        self.goToDist.engage()
        self.goToDist.setTargetDist(60)
        self.goToDist.start()
