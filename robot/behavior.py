

class Behavior:
    def __init__(self, bbcon, motor_recommendations, active_flag=True, priority=1):
        # pointer to bbcon that we send recommendations and weights to
        self.bbcon = bbcon

        # Sensobs this bahavior gets data from
        self.sensobs = []

        # list of recommendations, one per motob this behavior passes to arbitrator, all motors used by all behaviors
        self.motor_recommendatoins = motor_recommendations

        # Flag indicating whether this behavior should consider sensob data
        self.active_flag = active_flag

        # Field indicating whether this behavior wants the robot to halt
        self.halt_request = False # What to put here? cant I just send a very high weight for the motor recommendation?

        # static predefined value for this behavior
        self.PRIORITY = priority

        # Number in range[0,1] indicating degree which current conditions warrant performance of this behavior
        # meaning all reccommendations issued by this behavior
        self.match_degree = 0

        # Weight arbitrator uses to value the winning behavior of recommendations
        self.weight = self.PRIORITY * self.match_degree

        # Remainding Field for memory etween timesteps are created by specializing classes


    # Functions to consider activation of Behavior
    def consider_deactivation(self):
        raise NotImplementedError("Please Implement this method")

    # Function to consider deactivation of Behavior
    def consider_activaton(self):
        raise NotImplementedError("Please Implement this method")

    # Read sensob data and suggest motor recommendations (and weights?)
    def sense_and_act(self):
        raise NotImplementedError("Please Implement this method")


    def update(self):
        # 1. Update activity status by considering need for activation. Get info from arbitrator?
        if self.consider_activaton():
            self.active_flag = True
        elif self.consider_deactivation():
            self.active_flag = False

        # Only perform calculations and recommendations if this behavior is active
        if self.active_flag:
            # 2. call sense_and_act
            self.sense_and_act()

            # Update behavior's weight. Need to consider the input from sensor, Place inside sense_and_act()??


        pass


