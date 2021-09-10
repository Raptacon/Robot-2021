from magicbot import AutonomousStateMachine, tunable, timed_state, state
from components.driveTrain import DriveTrain
from components.autoAlign import AutoAlign
from components.shooterLogic import ShooterLogic
from components.shooterMotors import ShooterMotorCreation
from components.pneumatics import Pneumatics
from components.BallCounter import ballCounter

class Autonomous(AutonomousStateMachine):
    """Creates the autonomous code"""
    time = 1.4
    MODE_NAME = "Offseason Autonomous"
    DEFAULT = True
    autoAlign: AutoAlign
    driveTrain: DriveTrain
    shooter: ShooterLogic
    shooterMotors: ShooterMotorCreation
    pneumatics: Pneumatics
    drive_speed = tunable(.25)

    rpm = 0 # Choose this based on path

    @state(first=True)
    def turnToTargetShoot(self):
        """Uses limelight to align to target"""
        self.autoAlign.setShootAfterComplete(True)
        self.autoShoot.setRPM(self.rpm)
        self.autoAlign.engage()
        if self.autoAlign.autoAlignFinished and self.autoShoot.finished and self.shooterLogic.finished:
            self.next_state("travel")

    @state
    def shooter_wait(self):
        """Waits for shooter to finish, then next state"""
        if self.shooter.current_state == 'idling':
            self.next_state_now('drive_backwards')

    # @timed_state(duration = time, next_state = 'turn')
    # def drive_backwards(self):
    #     """Drives the bot backwards for a time"""
    #     self.driveTrain.setTank(self.drive_speed, self.drive_speed)

    # @timed_state(duration = time, next_state = 'stop')
    # def turn(self):
    #     """Turns for a time"""
    #     self.driveTrain.setTank(-self.drive_speed, self.drive_speed)

    # @state(must_finish = True)
    # def stop(self):
    #     """Stops driving bot"""
    #     self.driveTrain.setTank(0, 0)
    #     self.done()
