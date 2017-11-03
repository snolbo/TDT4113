from time import sleep

class BBCON:
    def __init__(self, arbitrator,  sensobs=[], motobs=[], behaviors=[], active_behaviors=[]):
        self.sensobs = sensobs

        self.behaviors = behaviors
        self.motobs = motobs
        self.active_behaviors = active_behaviors

        # Object to resolve actuator request produced by behaviors
        self.arbitrator = arbitrator

        self.timestep_length = 0.5


    def addBehavior(self, behavior):
        if behavior not in self.behaviors:
            self.behaviors.append(behavior)

    def addSensob(self, sensob):
        if sensob not in self.sensobs:
            self.sensobs.append(sensob)

    def activateBehavior(self, behavior):
        if behavior not in self.active_behaviors:
            self.activate_behaviors.append(behavior)

    def deactivateBehavior(self, behavior):
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)


    ## METHOD BBCON MUST HAVE
    def runOneTimestep(self):

        # 1. update all sensobs, query for values and pre-proccessing
        for sensob in sensobs:
            sensob.update()


        # 2. update all behaviors. read relevant sensobs values and produce motor recomendation
        for behavior in self.behaviors:
            behavior.update()


        # 3. invoke arbitrator -> arbitrator.choose_action() that chooses and return winning behavior's
        #    motor reccomendations and halt_requests


        # 4. update all motobs based on these reccomendations, motobs updates settings on all motors


        # 5 Wait time step to let motor perform the chosen action
        time.sleep(self.timestep_length)


        # 6 reset sensobs
        for sensob in self.sensobs:
            sensob.resetSensors()






