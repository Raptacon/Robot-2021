from magicbot import StateMachine, state, timed_state, tunable, feedback

class ArmMotor(StateMachine):
    motors_shooter: dict

    
    def endel(self):
        self.starting = False
        self.finiangle = 0
        self.running = False
        self.intangle = 0

    def start(self):
        """
        Sets the starting variable to true,
        this should trigger the stateMachine on
        the next idling run
        """
        self.starting = True
    
    @state(first=True)
    def idling(self):
        """
        Starts the state machine if starting and not running
        """
        if self.starting and self.running == False and self.rotationset != 0:
            self.next_state('rotation')
        else:
            self.next_state('idling')

    @state
    def rotation(self):
        if(self.intangle < self.finiangle):
            
        else:
            self.next_state('stop')

    @state
    def stop(self):