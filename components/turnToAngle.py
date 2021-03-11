from components.driveTrain import DriveTrain
from magicbot import StateMachine, state, tunable, timed_state
from wpilib import controller
from components.navx import Navx

class TurnToAngle(StateMachine):

    P = 0.1
    I = 0
    D = 0
    
    navx: Navx
    driveSpeed = tunable(0.25)
    driveTrain: DriveTrain
    time = 0.01
    PIDController = controller.PIDController(Kp= P, Ki= I, Kd= D, period = time)
    ninetyBool = False
    negativeNinetyBool = False
    oneEightyBool = False

    def setup(self):
        reset = self.navx.reset()
        Yaw = self.navx.getYaw()

    def setNinetyBool(self):
        ninetyBool = True
        self.next_state('next')
        print("It works")
    
    def setNegativeNinetyBool(self):
        negativeNinetyBool = True
        self.next_state('next')

    def setOneEightyBool(self):
        oneEightyBool = True
        self.next_state('next')
    
    @state(first = True)
    def next(self):
        self.reset()
        print("values are reset")
        if ninetyBool == True:
            self.next_state('calcNinetyError')
        elif negativeNinetyBool == True:
            self.next_state('calcNegativeNinetyError')
        elif oneEightyBool == True:
            self.next_state('calcOneEightyError')
    
    @state
    def calcNinetyError(self):
        ninetyError = controller.PIDController.calculate(measurement = self.Yaw, setpoint = 90)
        self.next_state('turnNinety')
        
    @timed_state(duration = time)
    def turnNinety(self):
        if ninetyError > 0:
            self.driveTrain.setTank(self.driveSpeed, -1 * self.driveSpeed)
            self.next_state('calcNinetyError')
        elif ninetyError < 0:
            self.driveTrain.setTank(-1 * self.driveSpeed, self.driveSpeed)
            self.next_state('calcNinetyError')
        else:
            self.next_state('finish')

    @state
    def calcNegativeNinetyError(self):
        negativeNinetyError = conroller.PIDController.calculate(measurement = self.Yaw, setpoint = -90)
        self.next_state('turnNegativeNinety')

    @timed_state(duration = time)
    def turnNegativeNinety(self):
        if -1 * negativeNinetyError > 0:
            self.driveTrain.setTank(self.driveSpeed, -1 * self.driveSpeed)
            self.next_state('calcNegativeNinetyError')
        elif -1 * negativeNinetyError < 0:
            self.driveTrain.setTank(-1 * self.driveSpeed, self.driveSpeed)
            self.next_state('calcNegativeNinetyError')
        else:
            self.next_state('finish')

    @state
    def calcOneEightyError(self):
        oneEightyError = controller.PIDController.calculate(measurement = self.Yaw, setpoint = 180)
        self.next_state('turnOneEighty')

    @timed_state(duration = time)
    def turnOneEighty(self):
        if oneEightyError > 0:
            self.driveTrain.setTank(self.driveSpeed, -1 * self.driveSpeed)
            self.next_state('calcOneEightyError')
        elif oneEightyError < 0:
            self.driveTrain.setTank(-1 * self.driveSpeed, self.driveSpeed)
            self.next_state('calcOneEightyError')
        else:
            self.next_state('finish')

    @state
    def finish(self):
        self.ninetyBool = False
        self.negativeNinetyBool = False
        self.oneEightyBool = False

    def execute(self):
        pass