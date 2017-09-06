import random
import numpy as np

class Player:
    dict_str2num = {"rock": 0, "paper": 1, "scissor": 2}
    dict_num2str = {0:"rock",1:"paper",2:"scissor"}

    def __init__(self):
        self.chosen_action = None

    def choose_action(self):
        self.chosen_action = "rock"
        choice = input("Rock, Paper or Scissor?: ")
        choice = choice.lower()
        if choice in self.dict_str2num:
            return choice
        else:
            print("Illegal choice, choose again...:  ")
            return self.choose_action()
    def evaluate_choosing_random(self, score_array):
        return 0 # NOT FINISHED

    def receive_result(self, result, my_choice, opponent_choice):
        #print("You choose: " + my_choice + ", Opponent choose: " + opponent_choice)
        #print( "You won!" if result == 1 else "Opponent won")
        return

    def get_name(self):
        return "Player"


class Random(Player):
    def choose_action(self):
        return self.dict_num2str[random.randint(0,2)]

    def get_name(self):
        return "Random"


class Sequential(Player):
    def __init__(self):
        super(Sequential, self).__init__()
        self.chosen_action = -1

    def choose_action(self):
        self.chosen_action +=1
        return self.dict_num2str[self.chosen_action % 3]

    def get_name(self):
        return "Sequential"

class MostCommon(Player):
    def __init__(self):
        self.opponent_statistics = [0, 0, 0]

    def choose_action(self):
        possible_choices = []
        max_index = np.argmax(self.opponent_statistics)
        for x in range(0,2):
            if self.opponent_statistics[x] == self.opponent_statistics[max_index]:
                possible_choices.append(x)
        choice = 0
        if len(possible_choices) == 1:
            choice = possible_choices[0]
        else:
            choice = possible_choices[random.randint(0,len(possible_choices))]
        return choice


    def receive_result(self, result, my_choice, opponent_choice):
        super(MostCommon, self).receive_result(result, my_choice, opponent_choice)
        choice_index = self.dict_str2num[opponent_choice]
        self.opponent_statistics[self.dict_str2num[opponent_choice]] +=1

    def get_name(self):
        return "MostCommon"

class Historian(Player):
    def __init__(self):
        super(Historian, self).__init__()
        self.action_sequence = []
        self.memory = 1

    def choose_action(self):
        subsequence = self.action_sequence[len(self.action_sequence)-2:]
        #logic for finding most common subsequnce. When memory count is known, could have created table with all
        # combinations of subsequences to faster find and store subsequence occurences, but brute force ftw!
        choice = 0
        if len(self.action_sequence)-1 - self.memory < 0:
           # print("Historian choose random because action sequnce not long enough")
            choice =  self.dict_num2str[random.randint(0,2)]
        else:
            subsequence = self.action_sequence[len(self.action_sequence) - self.memory:]
            most_common_choice = [0,0,0]
            for i in range(0,len(self.action_sequence) - len(subsequence) ):
                if self.action_sequence[i:i+len(subsequence)] == subsequence:
                    most_common_choice[self.action_sequence[i+len(subsequence)]] +=1 # increment likelyhood of next element since subseq match
            if max(most_common_choice) != 0:
                opponent_choice =  np.argmax(most_common_choice)


                return self.dict_num2str[(opponent_choice + 1) % 3] # rock paper scissor, beats left, looses right
            #print("Historian choose random because no max in subsequence")
            return self.dict_num2str[random.randint(0,2)]


    def receive_result(self, result, my_choice, opponent_choice):
        super(Historian, self).receive_result(result, my_choice, opponent_choice)
        self.action_sequence.append(self.dict_str2num[opponent_choice])

    def get_name(self):
        return "Historian"





#p0 = Player()
#p1 = Random()
#p2 = Sequential()
#p3 = MostCommon()
#p4 = Historian()


#dict = {0:"rock",1:"paper",2:"scissor"}

#for i in range(0, 20  ):
    #print("Round " +  str(i))
    #act = p4.choose_action()
    #print("Historian choose " + str(act) )
    #p4.receive_result(1, act, p2.choose_action() )

