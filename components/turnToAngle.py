from components.driveTrain import DriveTrain
from magicbot import tunable
from wpilib import controller
from components.navx import Navx

class TurnToAngle():

    P = 0.1
    I = 0
    D = 0
    
    navx: Navx
    yaw = None
    driveSpeed = tunable(0.25)
    driveTrain: DriveTrain
    time = 0.01
    PIDController = controller.PIDController(Kp= P, Ki= I, Kd= D, period = time)
    nextOutput = None

    def setup(self):
        reset = self.navx.reset()
        self.yaw = self.navx.getYaw()

    def output(self):
        self.nextOutput = controller.PIDController.calculate(measurement = self.navx.getYaw(), setpoint = 90)

        if self.nextOutput == 0:
            controller.PIDController.reset()

    def execute(self):
        self.yaw = self.navx.getYaw()
        self.driveTrain.setTank(self.nextOutput, -1 * self.nextOutput)
        print(self.nextOutput)
    