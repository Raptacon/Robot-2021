import navx
from magicbot import tunable, AutonomousStateMachine, feedback, state, timed_state


class PathSelector(AutonomousStateMachine):
    MODE_NAME = "Path Follower"
    navx = navx._navx.AHRS.create_spi()
    path = None
    redAAngle = 0
    redBAngle = -26.6
    blueAAngle = 21.8
    blueBAngle = 11.3
    heading = 0
    difference = 0
    originalHeading = tunable(352)
    pathInt = 0

    
    @state(first = True)
    def variableSetup(self):
        self.heading = self.navx.getFusedHeading()
        self.next_state('selector')
    
    @state(must_finish = True)
    def selector(self):
        self.difference = self.heading - self.originalHeading

        if self.difference > 180:
            self.difference -= 360
        if self.difference < -180:
            self.difference += 360

        if self.difference < self.redAAngle - 2.5 and self.difference > self.redAAngle + 2.5:
            self.path = "Red A"
            self.pathInt = 1
            print("Red A")
        elif self.difference < self.redBAngle + 2.5 and self.difference > self.redBAngle - 2.5:
            self.path = "Red B"
            self.pathInt = 2
            print("Red B")
        elif self.difference < self.blueAAngle - 2.5 and self.difference > self.blueAAngle + 2.5:
            self.path = "Blue A"
            self.pathInt = 3
            print("Blue A")
        elif self.difference < self.blueBAngle - 2.5 and self.difference > self.blueBAgnle + 2.5:
            self.path = "Blue B"
            self.pathInt = 4
            print("Blue B")
        
        self.next_state('stop')

    @feedback
    def pathDisplay(self):
        return self.pathInt
    
    @state(must_finish = True)
    def stop(self):
        self.done()

