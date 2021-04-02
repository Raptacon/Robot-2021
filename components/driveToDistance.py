from magicbot import StateMachine, state, timed_state, tunable, feedback
from components.lidar import getDist
import logging as log


class driverToDistance(StateMachine):
    @state
    def idling(self):
        '''
        Puts driveToDistance int "idling"
        '''
        if self.start:
            self.next_state('setInitialPosition')

    @state
    def setInitialPosition(self):
        '''
        Sets the initial potion of the robot
        '''
        self.initialPosition = getDist
        self.next_state('StartDrive')

    @state
    def StartDrive(self):
        '''
        runs check on getDist and distanceSet to make sure their values won't break robot
        calcutes the values that the lidar must read to drive a surtent distance
        '''
        if getDist == -1 or self.distanceSet <= 30:
            self.next_state('idling')
        else:
            self.driveDistance = self.initialPosition - self.distanceSet
            self.next_state('drive')

    @state
    def drive(self):
        '''
        Drives the robot and checks if the robot has droven the correct postion
        '''
        self.speed = .09
        DriveTrain.setTank(self.speed)
        if self.driveDistance >= getDist:
            self.driveDistance = 0
            self.next_state('idling')

    def setDistance(self, distanceSet):
        '''
        Sets the distance we want the robot to drive
        '''
        self.distanceSet = distanceSet
        if self.distanceSet <= 30:
            log.error("Invalid Distance give to robot")
