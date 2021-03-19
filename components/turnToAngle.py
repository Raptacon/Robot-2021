from components.driveTrain import DriveTrain
from magicbot import tunable
from wpilib import controller
from components.navx import Navx

class TurnToAngle():

    P = 0.0025
    I = 0
    D = 0
    
    navx: Navx
    yaw = None
    driveTrain: DriveTrain
    time = 0.01
    PIDController = controller.PIDController(Kp= P, Ki= I, Kd= D, period = time)
    nextOutput = 0
    returningOutput = 0
    isRunning = False
    initialHeading = None
    isReturning = False

    def setup(self):
        reset = self.navx.reset()
        self.yaw = self.navx.getYaw()
        self.initialHeading = self.navx.getFusedHeading()

    def setIsRunning(self):
        self.isRunning = True

    def setIsReturning(self):
        self.isReturning = True
    
    def output(self):
        if self.isRunning == True:
            self.nextOutput = self.PIDController.calculate(measurement = float(self.yaw), setpoint = float(5))
            self.driveTrain.setTank(self.nextOutput, -1 * self.nextOutput)

        else:
            self.nextOutput = 0
            self.PIDController.reset()
            self.driveTrain.setTank(0, 0)

        if self.nextOutput == 0:
            self.PIDController.reset()
            self.driveTrain.setTank(0, 0)

    """
    def turnToOriginal(self):
        if self.isReturning == True:
            self.returningOutput = self.PIDController.calculate(measurement = float(self.yaw), setpoint = float(self.initialHeading))
            self.driveTrain.setTank(self.nextOutput, -1 * self.nextOutput)
        
        if self.nextOutput == 0:
            self.PIDController.reset()
            self.driveTrain.setTank(0, 0)
    """

    def stop(self):

        self.navx.reset()
        self.isRunning = False
        self.isReturning = False

    def execute(self):
        self.output()
        #self.turnToOriginal()
        self.yaw = self.navx.getYaw()
        print(self.nextOutput)
        print(str(self.yaw))
        