
# Dont see why we need multiple of these, as we have 1 motor and all commands depend on each other
# -> cant go forward and backward simontaniously. hence only need 1 Motob, and the commands are exclusive
class Motob:
    def __init__(self):
        # Dictionary to hold the commands actuated by this object and most recent motor reccomendation sent
        # self.command_dict[motor] = value
        # NOTE: in the assignment it says list of motors, but we only have one motor here, and the motob's
        #       issue commands
        # structure: {"string code for command" : [function-pointer to method in motor: last sent value], ...}
        self.command_dict = {}



    def update(self, recommendation):
        # Store and send motor recommendation
        for values in self.command_dict.values():
            values[1] = recommendation
        self.operationalize(recommendation)

    # Method that create motor settings based on recommendation and send them to relevant motors
    # Needs to be overwritten by specialization of the motob class
    def operationalize(self, recommendation):
        raise NotImplementedError("Please Implement this method")



    # Adds a code representing the motor command, and initialize last sent value to None
    def add_motor(self, code, command):
        self.command_dict[code] = [command, None]




# Example of how a motob class can be implemented
class ExampleMotob(Motob):
    def __init__(self):
        super(ExampleMotob, self).__init__()

    def operationalize(self, recommendation):
        # get code for recommendation rec_code
        for code in self.command_dict:
            # if rec_code == code
                # function = command_dict[code][0]
                # input = command_dict[code][1]
                # function(input)  # -> executes the command with given input
            #...
            pass
        # All motors operationalized succsessfully
        return


