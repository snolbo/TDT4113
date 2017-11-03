from camera import Camera
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt


class Sensob:
    def __init__(self, sensors_dict={}):
        # Hold sensors and their last updated values. Values are stored since they are accessed by behaviors
        self.sensors_dict = sensors_dict

        # Holds the data to be returned from this object, set in preprocessData
        self.data = None


    # Load values from all connected sensors into this
    def update(self):
        for sensor in self.sensors_dict:
            self.sensors_dict[sensor] = sensor.get_value()
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


def plot(img):
    plt.figure()
    plt.imshow(img)
    plt.axis("off")
    plt.show(block=False)



class ExampleSensob(Sensob):
    def __init__(self):
        super(ExampleSensob, self).__init__()


    def preprocess_data(self):
        for value in self.sensors_dict.values():
            # Process data
            pass
        # Store result from prprocessing in self.data
        self.data = None


class ImageSensob(Sensob):
    def __init__(self, cam_object):
        sensors_dict = {cam_object: None}
        super(ImageSensob, self).__init__(sensors_dict)

    def preproccessData(self):
        image = self.sensors_dict.values()



cam_object = Camera()
image_sensob = ImageSensob(cam_object)
image_sensob.update()

im = image_sensob.data
print()
# plot(im)

