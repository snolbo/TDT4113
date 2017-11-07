
import random

# Either take inn the bbcon, or recieve it.
class Arbitrator():

    def __init__(self, bbcon=False):
        self.bbcon = bbcon # if (bbcon) else self.bbcon = None

    def receive_bbcon(self, bbcon):
        self.bbcon = bbcon

    # Method called by bbcon.
    # Returns a list with [motor_recommendation, halt_request],
    # where motor_reccomendation is a list of motor reccomendations, one for each motob, which we are going to perform,
    # and halt_request is a boolean indicating if we are going to halt the robot.
    # stochastic can be set to True if we want to make a random, biased choice.
    def choose_action(self, stochastic=False):
        if self.bbcon == id(None):
            raise ValueError('Connect a bbcon instance to the arbitrator instance.')
        active_behaviors = self.bbcon.active_behaviors
        if len(active_behaviors) == 0:
            print(active_behaviors)
            return self.random_action()
        if not stochastic:
            chosen_weight = 0
            chosen_behavior = None
            # If active_behaviors is a list
            for behavior in active_behaviors:
                weight = behavior.weight
                if (weight >= chosen_weight):
                    chosen_weight = weight
                    chosen_behavior = behavior
            return [chosen_behavior.motor_recommendations, chosen_behavior.halt_request]
        else:
            # Stupid with two for loops? Easier way to do it?
            sum = 0
            for behavior in active_behaviors:
                sum += behavior.weight
            rand = random.uniform(0,sum)
            sum = 0
            for behavior in active_behaviors:
                if rand <= sum+behavior.weight:
                    return [behavior.motor_recommendations, behavior.halt_request]
                sum += behavior.weight


    def random_action(self):
        list = [['L', 0.5],['R', 0.5],['F', 0.5],['B', 0.5]]
        action = random.choice(list)
        return [action, 0]
