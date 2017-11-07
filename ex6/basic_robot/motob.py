from motors import Motors

# Just one class for the motors

class Motob():

    def __init__(self):
        self.value = None
        self.motors = Motors()

    # Method called by bbcon.
    # Takes in agreed upon syntax.
    def update(self, actions_chosen):
        halt_flag = actions_chosen[1]
        if halt_flag:
            print("stop")
            self.motors.stop()
            # Do something to tell the bbcon to stop the run???? #Evt. let the bbcon check itself, and stop after wait(). While-loop!
            return
        self.value = [actions_chosen[0]]  # If only one motob
        self.operationalize()
        self.value = None

    # Not to be called by anything but motobs own update.
    def operationalize(self):
        # Agree upon the syntax of recommendations. But if (L/R, deg, speed). (Then duration depends on deg and speed). So maybe just (L/R/F/B, speed).
        # We can just correspond dur with wait/dur of bbcon. Either let update take it in, or decide on given, static duration.
        for action in self.value:
            print(str(action))
            self.motors.set_value(action, 0)

    def stop(self):
        self.motors.stop()


# a = [1,2]
# left, right = a
# print(left)
# print(right)