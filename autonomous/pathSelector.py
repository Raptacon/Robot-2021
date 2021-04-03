import navx
from magicbot import tunable, AutonomousStateMachine, feedback


class PathSelector():
    MODE_NAME = "Path Follower"
    navx = navx._navx.AHRS.create_spi()
    path = None
    redAAngle = 0
    redBAngle = -26.6
    blueAAngle = 21.8
    blueBAngle = 11.3
    heading = 0
    difference = 0
    originalHeading = 0 #tunable(352)

    compatString = ["doof"]
    
    """
    def on_enable(self):
        pass
    """
    def setup(self):
        self.heading = self.navx.getFusedHeading
        self.originalHeading = self.navx.getFusedHeading

    def selector(self):
        self.difference = self.heading - self.originalHeading

        if self.difference > 180:
            self.difference -= 360
        if self.difference < -180:
            self.difference += 360

        if self.difference < redAAngle - 2.5 and self.difference > redAAngle + 2.5:
            self.path = "Red A"
            print("Red A")
        elif self.difference < redBAngle + 2.5 and self.difference > redBAngle - 2.5:
            self.path = "Red B"
            print("Red B")
        elif self.difference < blueAAngle - 2.5 and self.difference > blueAAngle + 2.5:
            self.path = "Blue A"
            print("Blue A")
        elif self.difference < blueBAngle - 2.5 and self.difference > blueBAnlge + 2.5:
            self.path = "Blue B"
            print("Blue B")

    @feedback
    def pathDisplay(self):
        return self.path

    def execute(self):
        self.path
        self.heading = self.navx.getFusedHeading
