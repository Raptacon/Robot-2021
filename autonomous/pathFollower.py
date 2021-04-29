import navx
from magicbot import tunable, AutonomousStateMachine, feedback, state, timed_state
from networktables import NetworkTables
import logging as log
from enum import Enum
from components.loaderLogic import LoaderLogic
from components.pneumatics import Pneumatics
from components.turnToAngle import TurnToAngle
from components.driveTrainGoToDist import GoToDist

class PathEnum(Enum):
    path1 = 1
    path2 = 2

class Vector():
    def init(self, angle, dist):
        self.angle = angle
        self.dist = dist

    def getAngle(self):
        return self.angle

    def getDist(self):
        return self.dist

class PathFollower(AutonomousStateMachine):
    MODE_NAME = "Path Follower"
    navx = navx._navx.AHRS.create_spi()
    smartDashboardNetworkTable = NetworkTables.getTable('SmartDashboard')
    pneumatics: Pneumatics
    loader: LoaderLogic
    turnToAngle: TurnToAngle
    goToDist: GoToDist
