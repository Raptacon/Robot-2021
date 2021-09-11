from magicbot import StateMachine, state, tunable
from components.driveTrain import DriveTrain
import logging as log

class GoToDist(StateMachine):

    compatString = ["doof"]

    driveTrain: DriveTrain
    dumbTolerance = tunable(.25)
    tolerance = tunable(.25)
    starting = False
    running = False
    targetDist = 0
    dumbSpeedSections = [[36, .3],[12, .2],[8, .15],[5, .1]]

    def setTargetDist(self, distance):
        """
        Call this to set the target distance
        (In Feet)
        """
        self.targetDist = distance

    def setDumbSpeedSections(self, sections:list):
        """
        Accepts a 2D list with distances in feet
        and speeds from 0 to 1 to determine speeds
        at different distances. Speed should decrease
        with distance.
        """
        
        self.dumbSpeedSections = sorted(sections, key=lambda x: x[1], reverse = True)

    def start(self):
        """
        Call this to start the process
        """
        self.starting = True

    def stop(self):
        self.running = False
        self.driveTrain.setArcade(0, 0)
        self.next_state("idling")

    @state(first=True)
    def idling(self):
        """
        THIS IS A STATE
        DO NOT CALL IT AS A METHOD
        """
        self.initDist = 0
        if self.starting and not self.running:
            if self.targetDist != 0:
                self.next_state("recordInitDist")
            else:
                log.error("Must set target dist before calling start")
                self.next_state("idling")
        else:
            self.next_state("idling")

    @state
    def recordInitDist(self):
        """
        THIS IS A STATE
        DO NOT CALL IT AS A METHOD
        """
        self.running = True
        self.starting = False
        self.initDist = self.driveTrain.getEstTotalDistTraveled()
        self.targetDist = self.initDist + self.targetDist
        self.next_state("goToDist")

    @state
    def goToDist(self):
        """
        THIS IS A STATE
        DO NOT CALL IT AS A METHOD
        """
        self.dist = self.driveTrain.getEstTotalDistTraveled()
        self.dumbSpeed = 0

        self.nextSpeed = 0
        totalOffset = self.targetDist - self.dist
        for section in self.dumbSpeedSections:
            if abs(totalOffset) > section[0]:
                self.dumbSpeed = section[1]
                break

        if self.dumbSpeed == 0:
            self.dumbSpeed = self.dumbSpeedSections[-1][1]

        if self.dist < self.targetDist - self.dumbTolerance:
            self.nextSpeed = -1 * self.dumbSpeed
            self.next_state("goToDist")
        elif self.dist > self.targetDist + self.dumbTolerance:
            self.nextSpeed = self.dumbSpeed
            self.next_state("goToDist")
        if self.dist > self.targetDist - self.tolerance and self.dist < self.targetDist - self.tolerance:
            self.nextSpeed = 0
            self.stop()
            self.next_state("idling")

        self.driveTrain.setArcade(self.nextSpeed, 0)
