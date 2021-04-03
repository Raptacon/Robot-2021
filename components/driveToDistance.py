from magicbot import StateMachine, state, timed_state, tunable, feedback
from components.lidar import Lidar
from components.driveTrain import DriveTrain
import logging as log


class DriveToDistance(StateMachine):
    lidar: Lidar
    driveTrain: DriveTrain

    def on_enable(self):
        """Called when bot is enabled."""
        self.speed = -.15
        self.distanceSet = 0
        self.starting = False
        self.running = False

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
        if self.starting and self.running == False and self.distanceSet != 0:
            self.next_state('setInitialPosition')
        else:
            self.next_state('idling')

    @state
    def setInitialPosition(self):
        """
        Sets the initial potion of the robot
        """
        self.starting = False
        self.running = True
        self.initialPosition = self.lidar.getDist()
        self.next_state('StartDrive')

    @state
    def StartDrive(self):
        """
        Runs check on getDist and distanceSet to make sure their values won't break robot
        calcutes the values that the lidar must read to drive a certain distance
        """
        if self.lidar.getDist() == -1:
            log.error("Lidar is at max dist")
            self.stop()
        else:
            self.driveDistance = self.initialPosition - self.distanceSet
            if self.driveDistance < 0:
                log.error("Distance setpoint is greater than current position - Don't do that")
                self.stop()
            else:
                self.next_state('drive')

    @state
    def drive(self):
        """
        Drives the robot and checks if the robot has driven to the correct postion
        """
        self.driveTrain.setArcade(self.speed, 0)
        if self.lidar.getDist() <= self.distanceSet:
            self.stop()
        else:
            self.next_state('drive')

    def stop(self):
        """
        Stops the drivetrain and sets the setpoint to 0
        """
        self.running = False
        self.distanceSet = 0
        self.driveTrain.setTank(0, 0)
        self.next_state('idling')

    def setDistance(self, distanceSet):
        """
        Sets the distance we want the robot to drive to.
        For example: If you are 40 cm away from wall and want to get to 30,
        input 30 as distanceSet. The robot should drive 10 cm.
        """
        if distanceSet <= 30:
            log.error("Invalid Distance given to robot")
            self.distanceSet = 0
            self.starting = False
        else:
            self.distanceSet = distanceSet
