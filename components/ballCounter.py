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
        self.prevLoadingSensorState = State.kNotTripped
        self.prevShootngSensorState = State.kNotTripped
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
        self.currentLoadingSensorState = self.sensors.loadingSensor(State.kTripped)
        self.currentShootngSensorState = self.sensors.shootingSensor(State.kTripped)

        # If the state of a loading sensor has changed AND it is unbroken,
        # we assume a ball has entered/left and passed a break sensor
        # and so a ball is added/subtracted
        if(self.currentLoadingSensorState != self.prevLoadingSensorState
        and self.currentLoadingSensorState == False):
            self.addBall()

        if(self.currentShootngSensorState != self.prevShootngSensorState
        and self.currentShootngSensorState == False):
            self.subtractBall()

        self.prevLoadingSensorState = self.currentLoadingSensorState
        self.prevShootngSensorState = self.currentShootngSensorState
        self.SmartTable.putNumber("BallCount", self.ballCount)
        pass
