from components.driveTrain import DriveTrain

class DriveTrainHandler():
    compatString = ["doof"]

    driveTrain: DriveTrain

    def requestDriveTrain(requestSource):
        print(type(requestSource))
        return True
