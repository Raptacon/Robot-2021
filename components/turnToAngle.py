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
    turnAngle = tunable(5)
    speed = tunable(.15)
    tolerance = tunable(1)

    def setup(self):
        self.heading = self.navx.getFusedHeading()
        self.originalHeading = self.navx.getFusedHeading()
        self.initialHeading = self.navx.getFusedHeading()
        #self.PIDController = controller.PIDController(Kp= self.P, Ki= self.I, Kd= self.D, period = self.time)

    def setIsRunning(self):
        self.isRunning = True
        print(str(self.initialHeading))
        self.nextHeading = self.initialHeading + self.turnAngle
        #self.PIDController = controller.PIDController(Kp= self.P, Ki= self.I, Kd= self.D, period = self.time)
    
    def setScan(self):
        self.scanning = True

    def setIsReturning(self):
        self.isReturning = True
    
    def output(self):
        if self.isRunning == True:
            if self.nextHeading > 360 and self.heading < (self.nextHeading - 360):
                #self.nextOutput = self.PIDController.calculate(measurement = float(self.heading + 360), setpoint = float(self.nextHeading))
                if self.heading + 360 > self.nextHeading:
                    self.nextOutput = self.speed
                else:
                    self.nextOutput = -1 * self.speed
                self.driveTrain.setTank(self.nextOutput, -1 * self.nextOutput)
            
            elif self.nextHeading > 360:
                #self.nextOutput = self.PIDController.calculate(measurement = float(self.heading), setpoint = float(self.nextHeading))
                if self.heading > self.nextHeading:
                    self.nextOutput = self.speed
                else:
                    self.nextOutput = -1 * self.speed
                self.driveTrain.setTank(self.nextOutput, -1 * self.nextOutput)
            
            else:
                #self.nextOutput = self.PIDController.calculate(measurement = float(self.heading), setpoint = float(self.nextHeading))
                if self.heading > self.nextHeading:
                    self.nextOutput = self.speed
                else:
                    self.nextOutput = -1 * self.speed
                self.driveTrain.setTank(self.nextOutput, -1 * self.nextOutput)

            if self.heading < self.nextHeading + self.tolerance and self.heading > self.nextHeading - self.tolerance:
                self.driveTrain.setTank(0, 0)


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
        print(str(self.nextOutput))