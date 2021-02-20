import wpilib
import navx

class Navx:
    
    def setup(self):
        
        self.navx = navx._navx.AHRS.create_spi()

    def displayValues(self):
        
        """Prints the navx functions that we want to implement. This can be changed based off of how we want these values to be displayed. This can also be implemented after 
        certain time periods."""

        print("X Displacement: ", str(self.navx.getDisplacementX()))
        print("Y Displacement: ", str(self.navx.getDisplacementY()))
        print("Z Displacement: ", str(self.navx.getDisplacementZ()))
        print("Roll: ", str(self.navx.getRoll()))
        print("Pitch: ", str(self.navx.getPitch()))
        print("Yaw: ", str(self.navx.getYaw()))
        
    def reset(self):
        """Resets values to 0 from the current position"""

        self.navx.reset()
        self.navx.resetDisplacement()

    def turnToAngle(self):
        """Turn a certain amount of degrees. Could be moved to autonomous."""
        pass

    def execute(self):
        pass
