import logging as log
from components.breakSensors import Sensors, State
from networktables import NetworkTables

class ballCounter:
    """Class meant to keep track of the number of balls currently in the hopper"""

    SmartTable = NetworkTables.getTable("SmartDashboard")
    compatString = ["doof"]
    sensors: Sensors
    maxBalls = 4

    def on_enable(self):
        self.prevLoadingSensorTripped = State.kNotTripped
        self.prevShootngSensorTripped = State.kNotTripped
        self.ballCount = None

    def addBall(self):
        if self.ballCount <= self.maxBalls:
            self.ballCount += 1
        else:
            log.error("Too many balls added")

    def subtractBall(self):
        if self.ballCount == 0:
            log.error("Too many balls subtracted")
        else:
            self.ballCount -= 1

    def resetBallCount(self):
        """
        Reset the variable ballCount to 0
        """
        self.ballCount = 0

    def getBallCount(self):
        return self.ballCount

    def setBallCount(self, balls):
        self.ballCount = balls

    def execute(self):
        self.currentLoadingSensorTripped = self.sensors.loadingSensor(State.kTripped)
        self.currentShootngSensorTripped = self.sensors.shootingSensor(State.kTripped)

        # If the state of a loading sensor has changed AND it is unbroken,
        # we assume a ball has entered/left and passed a break sensor
        # and so a ball is added/subtracted
        if(self.currentLoadingSensorTripped != self.prevLoadingSensorTripped
        and self.currentLoadingSensorTripped == False):
            self.addBall()

        if(self.currentShootngSensorTripped != self.prevShootngSensorTripped
        and self.currentShootngSensorTripped == False):
            self.subtractBall()

        self.prevLoadingSensorTripped = self.currentLoadingSensorTripped
        self.prevShootngSensorTripped = self.currentShootngSensorTripped
        self.SmartTable.putNumber("BallCount", self.ballCount)
        pass
