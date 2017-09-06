import PlayerTypes
import numpy as np
import matplotlib.pyplot

class SingleGame:
    dict_str2num = {"rock": 0, "paper": 1, "scissor": 2}
    winner_table = [    [0, -1, 1],
                        [1, 0, -1],
                        [-1, 1, 0]  ] # could use just one list and shift with modulo on lookup

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.str = "Game not yet played"


    def play_game(self):
        p1_choice = self.player1.choose_action()
        p2_choice = self.player2.choose_action()
        p1_num = self.dict_str2num[p1_choice]
        p2_num = self.dict_str2num[p2_choice]
        p1_result = self.winner_table[p1_num][p2_num]
        #print( p1_choice + "    " + p2_choice)
        self.player1.receive_result(p1_result, p1_choice, p2_choice)
        self.player2.receive_result(-p1_result, p2_choice, p1_choice)


        self.str = self.player1.get_name() + "(1) choose: " + p1_choice + ", " + self.player2.get_name() + "(2) choose: " + p2_choice + " | "
        if p1_result == 0:
            self.str += "Draw"
        else:
            self.str+= "Winner is " + (self.player1.get_name() + "(1)" if p1_result else self.player2.get_name() + "(2)")
        return p1_result

    def __str__(self):
        return self.str


class MultipleGame(SingleGame):
    def __init__(self, player1, player2, num_games):
        super(MultipleGame, self).__init__(player1, player2)
        self.num_games = num_games

    def play_single_game(self):
        return super(MultipleGame, self).play_game()


    def play_tournament(self):
        p1_percentage = np.array([0])
        p2_percentage = np.array([0])
        for i in range(1,self.num_games+1):
            p1_result = self.play_single_game()
            if p1_result == 1:
                p1_percentage = np.append(p1_percentage, p1_percentage[i-1] +1)
                p2_percentage = np.append(p2_percentage, p2_percentage[i-1])
            elif p1_result == -1:
                p1_percentage = np.append(p1_percentage, p1_percentage[i - 1])
                p2_percentage = np.append(p2_percentage, p2_percentage[i - 1]+1)
            else:
                p1_percentage = np.append(p1_percentage, p1_percentage[i - 1])
                p2_percentage = np.append(p2_percentage, p2_percentage[i - 1])

        I = [ i for i in range(1,self.num_games +1)]
        p1_percentage = np.divide(p1_percentage[1:], I)
        p2_percentage = np.divide(p2_percentage[1:], I)

        matplotlib.pyplot.figure(1)
        matplotlib.pyplot.plot(I, p1_percentage)
        matplotlib.pyplot.axis([1,self.num_games, 0,1])

        matplotlib.pyplot.figure(2)
        matplotlib.pyplot.plot(I, p2_percentage)
        matplotlib.pyplot.axis([1,self.num_games, 0, 1])


        matplotlib.pyplot.show()


        return














p1 = PlayerTypes.MostCommon()
p2 = PlayerTypes.MostCommon()

game = MultipleGame(p1,p2, 300)
print(game)

game.play_tournament()
