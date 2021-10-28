from components.driveTrain import DriveTrain
class DriveTrainHandler():
    compatString = ["doof"]

    driveTrain: DriveTrain
    currentControl = None

    def set(self, requestOrigin, drive1, drive2):
        """
        This is the way to get control of the driveTrain

        @param: requestOrigin the source of the call.
        Must be "component" or "robot"
        """
        if requestOrigin == 'robot':
            self.currentControl = requestOrigin
            return True

    def execute(self):
        if currentControl
