from time import sleep
from sensob import Sensob
from arbitrator import Arbitrator
from motob import Motob
import Behavior


class BBCON():
    def __init__(self, arbitrator,  motob, sensobs=[], behaviors=[], active_behaviors=[]):
        self.sensobs = sensobs

        self.behaviors = behaviors
        self.motob = motob
        self.active_behaviors = active_behaviors

        # Object to resolve actuator request produced by behaviors
        self.arbitrator = arbitrator

        self.timestep_length = 0.5

        self.halt = False


    def addBehavior(self, behavior):
        if behavior not in self.behaviors:
            self.behaviors.append(behavior)

    def addSensob(self, sensob):
        if sensob not in self.sensobs:
            self.sensobs.append(sensob)

    def activateBehavior(self, behavior):
        if behavior not in self.active_behaviors:
            self.active_behaviors.append(behavior)

    def deactivateBehavior(self, behavior):
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)


    ## METHOD BBCON MUST HAVE
    def runOneTimestep(self):

        # 1. update all sensobs, query for values and pre-proccessing
        for sensob in self.sensobs:
            sensob.update()


        # 2. update all behaviors. read relevant sensobs values and produce motor recomendation
        for behavior in self.behaviors:
            behavior.update()


        # 3. invoke arbitrator -> arbitrator.choose_action() that chooses and return winning behavior's
        #    motor reccomendations and halt_requests
        actions_chosen = self.arbitrator.choose_action()
        if actions_chosen[1]:
            self.halt = True


        # 4. update motob based on these reccomendations, motob updates settings on motors
        self.motob.update(actions_chosen)


        # 5 Wait time step to let motor perform the chosen action
        sleep(self.timestep_length)


        # 6 reset sensobs
        for sensob in self.sensobs:
            sensob.resetSensors()



    def test_run(self, time):
        i = 0
        while(not self.halt):
            i += 1
            if (i >= time/self.timestep_length):
                self.halt = True
            self.runOneTimestep()



def test():
    motob = Motob()
    arbritator = Arbitrator()
    bbcon = BBCON(arbritator, motob)
    arbritator.receive_bbcon(bbcon)
    forwd = Behavior.Forward(bbcon)
    backwd = Behavior.Backward(bbcon)
    bbcon.addBehavior(forwd)
    bbcon.addBehavior(backwd)
    bbcon.test_run(10)

