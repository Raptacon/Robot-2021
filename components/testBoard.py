
class TestBoard:
    compatString = ["testBoard"]
    upSpeed = .1
    downSpeed = .1
    digitalInput_breakSensors: dict

    def on_enable(self):
        print("here")
        self.sensor = self.digitalInput_breakSensors["sensor1"]
    
    def execute(self):
        return self.sensor.get()
