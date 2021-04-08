import navx
from magicbot import tunable, AutonomousStateMachine, feedback, state, timed_state
from networktables import NetworkTables
from components.loaderLogic import LoaderLogic
from components.pneumatics import Pneumatics
from components.turnToAngle import TurnToAngle

class PathSelector(AutonomousStateMachine):
    MODE_NAME = "Path Follower"
    navx = navx._navx.AHRS.create_spi()
    smartDashboardNetworkTable = NetworkTables.getTable('SmartDashboard')
    pneumatics = Pneumatics
    loaderLogic = LoaderLogic
    tta = TurnToAngle
    path = "No Path"
    redAAngle = 0
    redBAngle = -26.6
    blueAAngle = 21.8
    originalHeading = tunable(0)
    blueBAngle = 11.3
    heading = 0
    """first array with displacement in inches, second is the turn angles
    Add motor parts later"""
    redA = [["Drive to ball 1", 60], ["Turn to ball 2", 60], ["Drive to ball 2", 67], ["Turn to ball 3", -98.2], 
            ["Drive to ball 3", 89], ["Turn to end", originalHeading], ["Drive to end", 192]]

    blueA = [["Drive to ball 1", 162], ["Turn to ball 2", -93.4], ["Drive to ball 2", 88], ["Turn to ball 3", 98.2], 
            ["Drive to ball 3", 67], ["Turn to end", originalHeading], ["Drive to end", 72]]

    redB = [["Drive to ball 1", 67], ["Turn to ball 2", -71.6], ["Drive to ball 2", 84], ["Turn to ball 3", 90], 
            ["Drive to ball 3", 84], ["Turn to end", originalHeading], ["Drive to end", 120]]

    blueB = [["Drive to ball 1", 152.4], ["Turn to ball 2", 56.3], ["Drive to ball 2", 84.8], ["Turn to ball 3", 90], 
            ["Drive to ball 3", 84.8], ["Turn to end", originalHeading], ["Drive to end", 42]]


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
            #self.next_state('ballOnePickup')
            self.next_state('driveForward')
        elif self.difference < self.redBAngle + 2.5 and self.difference > self.redBAngle - 2.5:
            self.path = "Red B"
            self.pathInt = 2
            print("Red B")
            #self.next_state('ballOnePickup')
            self.next_state('driveForward')
        elif self.difference > self.blueAAngle - 2.5 and self.difference < self.blueAAngle + 2.5:
            self.path = "Blue A"
            self.pathInt = 3
            print("Blue A")
            #self.next_state('ballOnePickup')
            self.next_state('driveForward')
        elif self.difference > self.blueBAngle - 2.5 and self.difference < self.blueBAngle + 2.5:
            self.path = "Blue B"
            self.pathInt = 4
            print("Blue B")
            #self.next_state('ballOnePickup')
            self.next_state('driveForward')    

    @timed_state(duration = 3)
    def driveForward(self):
        self.driveTrain.setTank(0.25, 0.25)
        print("Driving")
        self.next_state('turnBallTwo')
    """
    @state(must_finish = True)
    def ballOnePickup(self):
        self.loaderLogic.setAutoLoading()
        if self.pathInt == 1:
            #drive to distance when it is ready, redA[0][1]
            print(redA[0][0])
        elif self.pathInt == 2:
            #drive to distance when it is ready, redB[0][0]
            print(redB[0][0])
        elif self.pathInt == 3:
            #drive to distance when it is ready, blueA[0][0]
            print(blueA[0][0])
        elif self.pathInt == 4:
            #drive to distance when it is ready, blueB[0][0]
            print(blueB[0][0])
        self.next_state('turnBallTwo')
    """
    @state(must_finish = True)
    def turnBallTwo(self):
        if self.pathInt == 1:
            self.tta.turnAngle = redA[1][1]
            print(self.redA[1][0])
        elif self.pathInt == 2:
            self.tta.turnAngle = redB[1][1]
            print(self.redB[1][0])
        elif self.pathInt == 3:
            self.tta.turnAngle = blueA[1][1]
            print(self.blueA[1][0])
        elif self.tta.turnAngle == 4:
            self.tta.turnAngle = blueB[1][1]
            print(self.redB[1][0])
        self.tta.setIsRunning()
        self.next_state('stop')
    
    """
    @state(must_finish = True)
    def ballTwoPickup(self):
        self.loaderLogic.setAutoLoading()
        if self.pathInt == 1:
            #drive to distance when it is ready, redA[2][1]
            print(self.redA[2][0])
        elif self.pathInt == 2:
            #drive to distance when it is ready, redB[2][1]
            print(self.redB[2][0])
        elif self.pathInt == 3:
            #drive to distance when it is ready, blueA[2][1]
            print(self.blueA[2][0])
        elif self.pathInt == 4:
            #drive to distance when it is ready, blueB[2][1]
            print(self.blueB[2][0])
        self.next_state('turnBallThree')
        
    @state(must_finish = True)
    def turnBallThree(self):
        if self.pathInt == 1:
            self.tta.turnAngle = redA[3][1]
            print(self.redA[3][0])
        elif self.pathInt == 2:
            self.tta.turnAngle = redB[3][1]
            print(self.redB[3][0])
        elif self.pathInt == 3:
            self.tta.turnAngle = blueA[3][1]
            print(self.blueA[3][0])
        elif self.tta.turnAngle == 4:
            self.tta.turnAngle = blueB[3][1]
            print(self.blueB[3][0])
        self.tta.setIsRunning()
        self.next_state('ballThreePickup')

    @state(must_finish = True)
    def ballThreePickup(self):
        self.loaderLogic.setAutoLoading()
        if self.pathInt == 1:
            #drive to distance when it is ready, redA[4][1]
            print(self.redA[4][0])
        elif self.pathInt == 2:
            #drive to distance when it is ready, redB[4][1]
            print(self.redB[4][0])
        elif self.pathInt == 3:
            #drive to distance when it is ready, blueA[4][1]
            print(self.blueA[4][0])
        elif self.pathInt == 4:
            #drive to distance when it is ready, blueB[4][1]
            print(self.blueB[4][0])
        self.next_state('turnEnd')

    @state(must_finish = True)
    def turnEnd(self):
        self.tta.nextHeading = self.originalHeading
        self.tta.setIsRunning
        self.next_state('driveToEnd')

    @state(must_finish = True)
    def driveToEnd(self):
        if self.pathInt == 1:
            #drive to distance when it is ready, redA[6][1]
            print(self.redA[6][0])
        elif self.pathInt == 2:
            #drive to distance when it is ready, redB[6][1]
            print(self.redB[6][0])
        elif self.pathInt == 3:
            #drive to distance when it is ready, blueA[6][1]
            print(self.blueA[6][0])
        elif self.pathInt == 4:
            #drive to distance when it is ready, blueB[6][1]
            print(self.blueB[6][0])
        self.next_state('stop')
    """

    @state(must_finish = True)
    def stop(self):
        self.done()
