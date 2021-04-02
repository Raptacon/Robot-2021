from magicbot import StateMachine, state, timed_state, tunable, feedback
from components.lidar import getDist


class driverToDistance(StateMachine):
    @state
    def idling(self):
        if self.start:
            self.next_state('setInitialPosition')

    @state
    def setInitialPosition(self):
        self.initialPosition = getDist
        self.next_state('StartDrive')

    @state
    def StartDrive(self):
        if getDist == 0:
            print("Distance is invalid")
            self.next_state('idling')
        else:
            self.driveDistance = self.initialPosition - self.distanceSet
            self.next_state('drive')

    @state
    def drive(self):
        DriveTrain.setTank
        if self.driveDistance >= getDist:
            self.driveDistance = 0
            self.next_state('idling')
            print("You have reached destnation")

    def setDistance(self, distanceSet):
        self.distanceSet = distanceSet
