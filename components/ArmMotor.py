from magicbot import StateMachine, state, timed_state, tunable, feedback
class ArmMotor(StateMachine):
    motors_shooter: dict
    
    
    def enable(self):
        self.finiangle = 0
        self.Zeroangle = self.armMotor.getAngle()
        self.armMotor = self.motors_shooter["armMotor"]

    def start(self,angle):
        """
        Sets the starting variable to true,
        this should trigger the stateMachine on
        the next idling run
        """
        self.finiangle = angle
        self.next_state('rotation')

    @state
    def rotation(self):
        if self.armMotor:
            self.armMotor.set(self.shooterSpeed)
        elif self.armMotor == False:
            self.armMotor.set(0)

    @state
    def stop(self):