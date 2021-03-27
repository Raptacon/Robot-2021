from components.driveTrain import DriveTrain
from magicbot import tunable, feedback
from wpilib import controller

import navx

class TurnToAngle():

    #PID
    #P = tunable(0.032)
    #I = tunable(0.0001)
    #D = 0
    #time = 0.01
    
    navx = navx._navx.AHRS.create_spi()
    driveTrain: DriveTrain
    #PIDController = None
    nextOutput = 0
    returningOutput = 0
    isRunning = False
    isReturning = False
    scanning = False
    initialHeading = 0
    nextHeading = 0
    heading = 0
    originalHeading = 0
    orignalNext = 0
    turnAngle = tunable(5)
    speed = tunable(.15)
    multiplier = tunable(.75)
    tolerance = tunable(1)

    def setup(self):
        self.heading = self.navx.getFusedHeading()
        self.originalHeading = self.navx.getFusedHeading()
        self.initialHeading = self.navx.getFusedHeading()
        #self.PIDController = controller.PIDController(Kp= self.P, Ki= self.I, Kd= self.D, period = self.time)

    def setIsRunning(self):
        self.isRunning = True
        self.nextHeading = self.initialHeading + self.turnAngle
        if self.nextHeading > 360 and self.heading < self.nextHeading - 360:
            self.nextHeading -= 360
        #self.PIDController = controller.PIDController(Kp= self.P, Ki= self.I, Kd= self.D, period = self.time)
    
    def setScan(self):
        self.scanning = True

    def setIsReturning(self):
        self.isReturning = True
    """
    def setSpeed(self):
        if self.nextHeading - self.heading >= 90:
            self.speed = .25
        elif self.nextHeading - self.heading < 90 and self.nextHeading - self.heading >= 45:
            self.speed = .2
        elif self.nextHeading - self.heading < 45:
            self.speed = .15
    """
    def output(self):
        if self.isRunning == True:
            if self.nextHeading > 360 or self.nextHeading < 0:
                self.nextHeading = self.nextHeading % 360

            if self.nextHeading - self.heading < 180:
                self.driveTrain.setTank(-1 * self.speed, self.speed)
            else:
                self.driveTrain.setTank(self.speed, -1 * self.speed)
            
            if (self.heading < self.nextHeading + self.tolerance and self.heading > self.nextHeading - self.tolerance):
                self.isRunning = False
                print("At angle")
            elif (self.heading + 360 < self.nextHeading + 2 * self.tolerance) and (self.heading + 360 > self.nextHeading - 2 * self.tolerance):
                self.isReturning = False
                print("stopping")
    @feedback
    def outputDisplay(self):
        return self.nextOutput

    @feedback
    def nextHeadingDisplay(self):
        return self.nextHeading
    
    def scan(self):
        if self.scanning == True:
            for x in range(0, 13):
                self.nextHeading = self.initialHeading + 5
                self.isRunning = True
                self.output()
                self.initialHeading = self.heading

    
    def stop(self):
        self.nextOutput = 0
        #self.PIDController.reset()
        
        if self.nextHeading > 360:
            self.nextHeading -= 360
        
        self.isRunning = False
        self.isReturning = False
        self.initialHeading = self.heading


    def execute(self):
        self.output()
        self.scan()
        self.heading = self.navx.getFusedHeading()