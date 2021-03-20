from components.driveTrain import DriveTrain
from magicbot import tunable
from wpilib import controller

import navx

class TurnToAngle():

    P = 0.0025
    I = 0
    D = 0
    
    navx = navx._navx.AHRS.create_spi()
    time = 0.01
    driveTrain: DriveTrain
    PIDController = controller.PIDController(Kp= P, Ki= I, Kd= D, period = time)
    nextOutput = 0
    returningOutput = 0
    isRunning = False
    initialHeading = 0
    nextHeading = 0
    heading = 0
    originalHeading = 0
    isReturning = False


    
    def setup(self):
        self.heading = self.navx.getFusedHeading()
        self.originalHeading = self.navx.getFusedHeading()

    def setIsRunning(self):
        self.isRunning = True


    def setIsReturning(self):
        self.isReturning = True
    
    def output(self):
        if self.isRunning == True:
            self.nextHeading = self.initialHeading + 90
            if self.nextHeading > 360:
                self.nextHeading -= 360
                self.nextOutput = self.PIDController.calculate(measurement = float(self.heading), setpoint = float(self.nextHeading))
                self.driveTrain.setTank(-.25 * self.nextOutput, .25 * self.nextOutput)

            elif self.nextHeading < 360:
                self.nextOutput = self.PIDController.calculate(measurement = float(self.heading), setpoint = float(self.nextHeading))
                self.driveTrain.setTank(self.nextOutput, -1 * self.nextOutput)

        if self.nextOutput == 0:
            self.PIDController.reset()
            self.driveTrain.setTank(0, 0)
    
    
    def turnToOriginal(self):
            self.returningOutput = self.PIDController.calculate(measurement = float(self.heading), setpoint = float(self.originalHeading))
            self.driveTrain.setTank(self.nextOutput, -1 * self.nextOutput)
        
            if self.returningOutput == 0:
                self.PIDController.reset()
                self.driveTrain.setTank(0, 0)
    

    def stop(self):
        self.nextOutput = 0
        self.PIDController.reset()
        #self.driveTrain.setTank(0, 0)
        self.isRunning = False
        self.isReturning = False

    def execute(self):
        self.output()
        self.turnToOriginal()
        self.heading = self.navx.getFusedHeading()
        #print(str(self.nextHeading))
        print(str(self.navx.getFusedHeading()))
        print(str(self.initialHeading))
