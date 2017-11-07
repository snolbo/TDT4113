from time import sleep
from sensob import *
from arbitrator import Arbitrator
from motob import Motob
from behavior import *
from camera import Camera
from zumo_button import ZumoButton



class BBCON():
    def __init__(self, arbitrator,  motob, sensobs=[], behaviors=[], active_behaviors=[]):
        self.sensobs = sensobs

        self.behaviors = behaviors
        self.motob = motob
        self.active_behaviors = active_behaviors

        # Object to resolve actuator request produced by behaviors
        self.arbitrator = arbitrator

        self.timestep_length = 0.1

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
        actions_chosen = self.arbitrator.choose_action(stochastic=True)
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
        print("BBCON timestep lengh : " + str(self.timestep_length))
        i = 0
        run = True
        while(run):
            i += 1
            if (i >= time/self.timestep_length):
                run = False
            self.runOneTimestep()
        self.motob.stop()



def test():

    motob = Motob()
    arbritator = Arbitrator()
    bbcon = BBCON(arbritator, motob)
    arbritator.receive_bbcon(bbcon)

    # cam_object = Camera()
    # imchannel_sensob = ImageChannelSensob(cam_object)
    # bbcon.addSensob(imchannel_sensob)
    # color_track_behavior = FollowColor(bbcon, imchannel_sensob)
    # bbcon.addBehavior(color_track_behavior)


    ultrasound_sensob = UltrasonicSensob()
    bbcon.addSensob(ultrasound_sensob)
    stop_behavior = UltrasoundStop(bbcon, ultrasound_sensob)
    bbcon.addBehavior(stop_behavior)

    ir_sensob = IRProx()
    bbcon.addSensob(ir_sensob)
    avoid_wall_behavior = AvoidSideWalls(bbcon, ir_sensob)
    bbcon.addBehavior(avoid_wall_behavior)

    # forwd = Forward(bbcon)
    # backwd = Backward(bbcon)
    # bbcon.addBehavior(forwd)
    # bbcon.addBehavior(backwd)


    ZumoButton().wait_for_press()
    while(True):
        bbcon.test_run(5)
        ZumoButton().wait_for_press()

