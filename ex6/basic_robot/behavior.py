class Behavior:
    def __init__(self, bbcon, active_flag=True, priority=1):
        # Pointer to the controller that uses this behavior
        self.bbcon = bbcon

        # List of recommendations that this behavior provides to the arbitrator
        self.motor_recommendations = []

        # Indicates if the behavior is active
        self.active_flag = active_flag
        if active_flag:
            self.bbcon.activateBehavior(self)

        # Value indicating the importance of this behavior. Static
        self.PRIORITY = priority

        # Request robot to completely halt activity
        self.halt_request = False

        # Number in range [0,1], indicating degree of warrant of this behavior
        self.match_degree = 0

        # Basis for selecting winning behavior for a timestep
        self.weight = 0


    # Test whether it should deactivate
    def consider_deactivation(self):
        raise NotImplementedError("Please Implement this method")

    # Test whether it should activate
    def consider_activation(self):
        raise NotImplementedError("Please Implement this method")

    def update_activity_status(self):
        if self.consider_activation() and self.active_flag == False:
            self.active_flag = True
            self.bbcon.activateBehavior(self)
        elif self.consider_deactivation() and self.active_flag == True:
            self.active_flag = False
            self.bbcon.deactivateBehavior(self)

    def update_weight(self):
        self.weight = self.PRIORITY * self.match_degree


    # Interface between bbcon and behavior
    def update(self):
        self.update_activity_status()
        self.sense_and_act()
        self.update_weight()

    # Uses sensob readings to produce motor recommendations (and halt requests). Specialized for each behavior
    def sense_and_act(self):

        # Gather values of sensobs
        # (Checking relvevant posts on bbcon)
        # Determine motor recommendations (and halt request)
        # Set match degree
        raise NotImplementedError("Please Implement this method")


class Forward(Behavior):
    def __init__(self, bbcon):
        super(Forward, self).__init__(bbcon)

    def consider_deactivation(self):
        return False

    def consider_activation(self):
        return True

    def sense_and_act(self):
        self.motor_recommendations = [0.5, 0.5]
        self.match_degree = 1


class Backward(Behavior):
    def __init__(self, bbcon):
        super(Backward, self).__init__(bbcon)

    def consider_deactivation(self):
        return False

    def consider_activation(self):
        return True

    def sense_and_act(self):
        self.motor_recommendations = [-0.5, -0.5]
        self.match_degree = 1




class FollowColor(Behavior):
    def __init__(self, bbcon, sensob):
        super(FollowColor, self).__init__(bbcon)

        # field for sensob
        self.sensob = sensob

    def consider_deactivation(self):
        return False

    def consider_activation(self):
        return True

    def sense_and_act(self):
        im_data = self.sensob.data
        value = self.weigthedDifference(im_data)
        dir = 1
        speed = abs(value) if abs(value) > 0.1 else 0
        self.motor_recommendations = [speed, -speed]
        self.match_degree = 1

    # Takes in a np array that represent image data, single channel only, calculated the weighted difference of values
    # from the center line in the image. Use to detect which side has most high intensity values
    def weigthedDifference(self, im_data):
        rows, cols = im_data.shape
        weighted_difference = 0
        mid = int(cols / 2)
        sum = 0
        im_data = im_data / 255.0
        for i in range(0, rows):
            for j in range(0, cols):
                # Add value to weighted_difference based on value and difference from center
                value = (j - mid) * im_data[i][j]
                weighted_difference += value
                sum += abs(value)
        # Return normalized result
        return float(weighted_difference/sum)


class UltrasoundStop(Behavior):
    def __init__(self, bbcon, sensob):
        super(UltrasoundStop, self).__init__(bbcon)
        # field for sensob
        self.sensob = sensob
        self.PRIORITY = 1000

    def consider_deactivation(self):
        return False

    def consider_activation(self):
        return True

    def sense_and_act(self):
        data = self.sensob.data
        if data < 10:
            self.match_degree = 1
        else:
            self.match_degree = 0
        self.motor_recommendations = [0, 0]


class AvoidSideWalls(Behavior):
    def __init__(self, bbcon, sensob):
        super(AvoidSideWalls, self).__init__(bbcon)

        # field for sensob
        self.sensob = sensob

    def consider_deactivation(self):
        return False

    def consider_activation(self):
        return True

    def sense_and_act(self):
        data = self.sensob.data
        right, left = data[0], data[1]

        self.motor_recommendations = [0, 0]
        self.match_degree = 0
        if right and not left:
            self.motor_recommendations = [0.5, 0.2]
            self.match_degree = 1

        elif not right and left:
            self.motor_recommendations = [0.2, 0.5]
            self.match_degree = 1

