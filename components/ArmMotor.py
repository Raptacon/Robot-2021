from magicbot import StateMachine, state, timed_state, tunable, feedback

class ArmMotor(StateMachine):
    motors_shooter: dict

    
    def enable(self):
        self.starting = False
        self.finangle= 0
        self.Zeroangle =self.armMotor.getAngle()
        self.armMotor = self.motors_shooter["ArmMotor"]

    def start(self, angle):
        """
        Sets the starting variable to true,
        this should trigger the stateMachine on
        the next idling run
        """
        self.finangle = angle
        self.next_state('rotation')
        
        
    
    @state(first=True)
    def idling(self):
        """
        Starts the state machine if starting and not running
        """
        self.next_state('idling')

    @state
    def rotation(self):
        
        if self.armMotor:
            self.armMotor.set(self.finangle)
        elif self.armMotor == False:
            self.armMotor.set(0)
    @state
    def stop(self):
