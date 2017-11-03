

class Behavior:

    def __init__(self, bbcon, active_flag = True, priority = 1):
        # Pointer to the controller that uses this behavior
        self.bbcon = bbcon

        # List of recommendations that this behavior provides to the arbitrator
        self.motor_recommendations = []

        # Indicates if the behavior is active
        self.active_flag = active_flag

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
        if self.consider_activation():
            self.active_flag = True
        elif self.consider_deactivation():
            self.active_flag = False
            
    def update_weight(self):
        self.weight = self.PRIORITY * self.match_degree
        
        
    # Interface between bbcon and behavior
    def update(self):
        # Update activity status
        # Sensobs should be informed if activity status changes
        # Update weigh
       

    # Uses sensob readings to produce motor recommendations (and halt requests). Specialized for each behavior
    def sense_and_act(self):

        # Gather values of sensobs
        # (Checking relvevant posts on bbcon)
        # Determine motor recommendations (and halt request)
        # Set match degree
        
class Forward(Behavior):

    def __init__(self, bbcon):
        super(Forward, self).__init__(bbcon)

    def consider_deactivation(self):
        return False

    def consider_activation(self):
        return False
    
    def update(self):
        self.update_activity_status()
        if self.active_flag:
            self.sense_and_act()
            self.update_weight()

    def sense_and_act(self):
        self.motor_recommendations.append("F")
        self.match_degree = 1
        
      
     
           
        



  
    


