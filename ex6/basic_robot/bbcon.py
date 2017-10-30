

class BBCON:
    def __init__(self):

        # List of  behaciors used by BBCON
        self.behaviors = []
        self.active_behaviors = []


        # Lists of sensor objects and motor object used by BBOCN
        self.sensobs = []
        self.motobs = []

        # Object to resolve actuator request produced by behaviors
        self.arbitrator = None

        # Information about timesteps
        self.timestep_length = 0.5
        self.current_timestep = 0


    ## METHOD BBCON SHOULD HAVE
    def add_behavior(self, behavior):
        if behavior not in self.behaviors:
            self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        if sensob not in self.sensobs:
            self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        if behavior not in self.active_behaviors:
            self.activate_behaviors.append(behavior)

    def deactivate_behavior(self, behavior):
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    ## METHOD BBCON MUST HAVE
    def run_one_timestep(self):

        # 1. update all sensobs, query for values and pre-proccessing


        # 2. update all behaviors. read relevant sensobs values and produce motor recomendation



        # 3. invoke arbitrator -> arbitrator.choose_action() that chooses and return winning behavior's
        #    motor reccomendations and helt_request flag


        # 4. update all motobs based on these reccomendations, motobs updates settings on all motors


        # 5 Wait time step to let motor perform the chosen action


        # 6 reset sensobs
        for ob in self.sensobs:



