import logging as log

class ballCounter:
    """Class meant to keep track of the number of balls currently in the hopper"""

    compatString = ["doof"]

    def on_enable(self):
        self.ballCount = 0

    def addBall(self):
        if self.ballCount <= 4:
            self.ballCount += 1
        else:
            log.error("Too many balls added")

    def subtractBall(self):
        if self.ballCount >= 1:
            self.ballCount -= 1
        else:
            log.error("Too many balls subtracted")

    def resetBallCount(self):
        """
        Reset the variable ballCount to 0
        """
        self.ballCount = 0

    def getBallCount(self):
        return self.ballCount

    def execute(self):
        pass
