from camera import Camera
from PIL import Image
import imager2 as IMR
import numpy as np
from ultrasonic import *
from irproximity_sensor import *



class Sensob:
    def __init__(self, sensors_dict={}):
        # Hold sensors and their last updated values. Values are stored since they are accessed by behaviors
        self.sensors_dict = sensors_dict

        # Holds the data to be returned from this object, set in preprocessData
        self.data = None

    # Load values from all connected sensors into this
    def update(self):
        for sensor in self.sensors_dict:
            sensor.update()
            self.sensors_dict[sensor] = sensor.get_value()
            # print(self.sensors_dict[sensor])
        self.preproccessData()
        return self.data

    # Method that performs preproccessing to produce result to be returned from this sensob.
    # Needs to be overwritten by specialization of the sensob class
    def preproccessData(self):
        raise NotImplementedError("Please Implement this method")

    # Adds a sensor to the dictionary and initializes its value to None
    def addSensor(self, sensor):
        self.sensors_dict[sensor] = None

    def resetSensors(self):
        for sensor in self.sensors_dict:
            sensor.reset()



# Channel is channel index, by default use channel 0 = red
class ImageChannelSensob(Sensob):
    def __init__(self, cam_object, channel=0):
        sensors_dict = {cam_object: None}
        super(ImageChannelSensob, self).__init__(sensors_dict)
        self.channel = channel

    def preproccessData(self):
        for image in self.sensors_dict.values():
            im_data = np.array(image)
            channel_data = im_data[:, :, self.channel]
            channel_data[channel_data < 100] =  0
            self.data = channel_data
            break

class UltrasonicSensob(Sensob):
    def __init__(self, ultrasonic_obj=Ultrasonic()):
        sensors_dict = {ultrasonic_obj: None}
        super(UltrasonicSensob, self).__init__(sensors_dict)

    def update(self):
        for sensor in self.sensors_dict:
            sensor.update()
            self.sensors_dict[sensor] = sensor.get_value()
        self.preproccessData()
        return self.data

    def preproccessData(self):
        for value in self.sensors_dict.values():
            self.data = value


class IRProx(Sensob):
    def __init__(self, prox_sensor=IRProximitySensor()):
        sensors_dict = {prox_sensor: None}
        super(IRProx, self).__init__(sensors_dict)

    def preproccessData(self):
        for sensor in self.sensors_dict:
            self.data = sensor.get_value()