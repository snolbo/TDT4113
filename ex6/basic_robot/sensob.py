


class Sensob:
    def __init__(self):
        # Hold sensors and their last updated values
        self.sensors_dict = {}

        # Holds the data to be returned from this object
        self.data = None


    # Load values from all connected sensors into this
    def update(self):
        for sensor in self.sensors_dict:
            self.sensors_dict[sensor] = sensor.get_value()
        self.preproccess_data()
        return self.data

    # Method that performs preproccessing to produce result to be returned from this sensob.
    # Needs to be overwritten by specialization of the sensob class
    def preproccess_data(self):
        raise NotImplementedError("Please Implement this method")

    # Adds a sensor to the dictionary and initializes its value to None
    def add_sensor(self, sensor):
        self.sensors_dict[sensor] = None



class ExampleSensob(Sensob):
    def __init__(self):
        super(ExampleSensob, self).__init__()


    def preprocess_data(self):
        for value in self.sensors_dict.values():
            # Process data
            pass
        # Store result from prprocessing in self.data
        self.data = None

