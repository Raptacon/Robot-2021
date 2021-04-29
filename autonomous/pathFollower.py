import navx
from magicbot import tunable, AutonomousStateMachine, feedback, state, timed_state
from networktables import NetworkTables
import logging as log
from components.loaderLogic import LoaderLogic
from components.pneumatics import Pneumatics
from components.turnToAngle import TurnToAngle
from components.driveTrainGoToDist import GoToDist

class PathSelector(AutonomousStateMachine):
    MODE_NAME = "Path Follower"
    navx = navx._navx.AHRS.create_spi()
    smartDashboardNetworkTable = NetworkTables.getTable('SmartDashboard')
    pneumatics: Pneumatics
    loader: LoaderLogic
    turnToAngle: TurnToAngle
    goToDist: GoToDist
    path = "No Path"
    redAAngle = 0
    redBAngle = -26.6
    blueAAngle = 21.8
    originalHeading = tunable(0)
    blueBAngle = 11.3
    heading = 0

    redADrive = [["Drive to ball 1", 60],  ["Drive to ball 2", 67], ["Drive to ball 3", 89], ["Drive to end", 192]]
    redATurn = [["Turn to ball 2", 60], ["Turn to ball 3", -98.2], ["Turn to end", originalHeading]]

    blueADrive = [["Drive to ball 1", 162],  ["Drive to ball 2", 88], ["Drive to ball 3", 67], ["Drive to end", 72]]
    blueATurn = [["Turn to ball 2", -93.4],["Turn to ball 3", 98.2],["Turn to end", originalHeading]]

    redBDrive = [["Drive to ball 1", 67],  ["Drive to ball 2", 84], ["Drive to ball 3", 84], ["Drive to end", 120]]
    redBTurn = [["Turn to ball 2", -71.6], ["Turn to ball 3", 90],["Turn to end", originalHeading]] 

    blueBDrive = [["Drive to ball 1", 152.4],  ["Drive to ball 2", 84.8], ["Drive to ball 3", 84.8], ["Drive to end", 42]]
    blueBTurn = [["Turn to ball 2", 56.3], ["Turn to ball 3", 90], ["Turn to end", originalHeading]]

    difference = 0
    originalHeading = tunable(0)
    pathInt = 0
    
    @state(first = True, must_finish = True)
    def variableSetup(self):
        self.heading = self.navx.getFusedHeading()
        print("Variables set up")
        self.next_state('loaderDeploy')

    @state(must_finish = True)
    def loaderDeploy(self):
        self.pneumatics.deployLoader()
        self.next_state('selector')
    
    @state(must_finish = True)
    def selector(self):
        self.difference = self.heading - self.originalHeading
        print(str(self.difference))
        print(str(self.heading))
        print(str(self.originalHeading))

        if self.difference > 180:
            self.difference -= 360
        if self.difference < -180:
            self.difference += 360

        if self.difference > self.redAAngle - 2.5 and self.difference < self.redAAngle + 2.5:
            self.path = "Red A"
            self.pathInt = 1
            print("Red A")
            self.next_state('ballOnePickup')
        elif self.difference < self.redBAngle + 2.5 and self.difference > self.redBAngle - 2.5:
            self.path = "Red B"
            self.pathInt = 2
            print("Red B")
            self.next_state('ballOnePickup')
        elif self.difference > self.blueAAngle - 2.5 and self.difference < self.blueAAngle + 2.5:
            self.path = "Blue A"
            self.pathInt = 3
            print("Blue A")
            self.next_state('ballOnePickup')
        elif self.difference > self.blueBAngle - 2.5 and self.difference < self.blueBAngle + 2.5:
            self.path = "Blue B"
            self.pathInt = 4
            print("Blue B")
            self.next_state('ballOnePickup')   

    @state(must_finish = True)
    def ballOnePickup(self):
        self.loader.setAutoLoading()
        if self.pathInt == 1:
            self.goToDist.setTargetDist(self.redADrive[0][1])
            print(self.redADrive[0][0])
        elif self.pathInt == 2:
            self.goToDist.setTargetDist(self.redBDrive[0][1])
            print(self.redBDrive[0][0])
        elif self.pathInt == 3:
            self.goToDist.setTargetDists(self.blueDriveA[0][1])
            print(self.blueADrive[0][0])
        elif self.pathInt == 4:
            self.goToDist.setTargetDist(self.blueBDrive[0][1])
            print(self.blueBDrive[0][0])
        else:
            log.error("No Path Found")
        self.goToDist.start()
        self.next_state('turnBallTwo')
    
    

    @state(must_finish = True)
    def turnBallTwo(self):
        if self.pathInt == 1:
            self.turnToAngle.turnAngle = redATurn[0][1]
            print(self.redATurn[0][0])
        elif self.pathInt == 2:
            self.turnToAngle.turnAngle = redBTurn[0][1]
            print(self.redBTurn[0][0])
        elif self.pathInt == 3:
            self.turnToAngle.turnAngle = blueATurn[0][1]
            print(self.blueATurn[0][0])
        elif self.turnToAngle.turnAngle == 4:
            self.turnToAngle.turnAngle = blueBTurn[0][1]
            print(self.blueBTurn[0][0])
        self.turnToAngle.setIsRunning()
        self.next_state('ballTwoPickup')
    
    
    @state(must_finish = True)
    def ballTwoPickup(self):
        self.loader.setAutoLoading()
        if self.pathInt == 1:
            self.goToDist.setTargetDist(self.redADrive[1][1])
            print(self.redADrive[1][0])
        elif self.pathInt == 2:
            self.goToDist.setTargetDist(self.redBDrive[1][1])
            print(self.redBDrive[1][0])
        elif self.pathInt == 3:
            self.goToDist.setTargetDist(self.blueADrive[1][1])
            print(self.blueADrive[1][0])
        elif self.pathInt == 4:
            self.goToDist.setTargetDist(self.blueBDrive[1][1])
            print(self.blueBDrive[1][0])
        self.goToDist.start()
        self.next_state('stop')
    """
    @state(must_finish = True)
    def turnBallThree(self):
        if self.pathInt == 1:
            self.turnToAngle.turnAngle = redATurn[0][1]
            print(self.redATurn[0][0])
        elif self.pathInt == 2:
            self.turnToAngle.turnAngle = redBTurn[0][1]
            print(self.redBTurn[0][0])
        elif self.pathInt == 3:
            self.turnToAngle.turnAngle = blueATurn[0][1]
            print(self.blueATurn[0][0])
        elif self.turnToAngle.turnAngle == 4:
            self.turnToAngle.turnAngle = blueBTurn[0][1]
            print(self.blueBTurn[0][0])
        self.turnToAngle.setIsRunning()
        self.next_state('ballThreePickup')

    @state(must_finish = True)
    def ballThreePickup(self):
        self.loader.setAutoLoading()
        if self.pathInt == 1:
            self.goToDist.setTargetDist = redADrive[2][1]
            print(self.redADrive[2][0])
        elif self.pathInt == 2:
            self.goToDist.setTargetDist = redBDrive[2][1]
            print(self.redBDrive[2][0])
        elif self.pathInt == 3:
            self.goToDist.setTargetDist = blueADrive[2][1]
            print(self.blueADrive[2][0])
        elif self.pathInt == 4:
            self.goToDist.setTargetDist = blueBDrive[2][1]
            print(self.blueBDrive[2][0])
        self.goToDist.start()
        self.next_state('turnEnd')

    @state(must_finish = True)
    def turnEnd(self):
        self.turnToAngle.nextHeading = self.originalHeading
        self.turnToAngle.setIsRunning
        self.next_state('driveToEnd')

    @state(must_finish = True)
    def driveToEnd(self):
        if self.pathInt == 1:
            self.goToDist.setTargetDist = self.redADrive[3][1]
            print(self.redADrive[3][0])
        elif self.pathInt == 2:
            self.goToDist.setTargetDist = self.redBDrive[3][1]
            print(self.redBDrive[3][0])
        elif self.pathInt == 3:
            self.goToDist.setTargetDist = self.blueADrive[3][1]
            print(self.blueADrive[3][0])
        elif self.pathInt == 4:
            self.goToDist.setTargetDist = self.blueBDrive[3][1]
            print(self.blueBDrive[3][0])
        self.goToDist.start()
        self.next_state('stop')

"""
    @state(must_finish = True)
    def stop(self):
        self.done()
