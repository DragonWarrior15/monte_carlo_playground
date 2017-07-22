import numpy as np
import reversi
import os
import matplotlib.pyplot as plt

def main():
    for sim_no in range(num_simulations):
        reversi_board = reversi.reversi(board_size)
        win_list = []
        for game_no in range(num_matches):
            print ('playing game ' + str(game_no) + ' in simulation no ' + str(sim_no))
            while (reversi_board.check_for_win() == 2):
                # reversi_board.pretty_print()
                move = reversi_board.select_a_move()
                # print (move)
                row, col = reversi_board.get_row_col_from_index(move)
                reversi_board.play_a_move(row, col)
                reversi_board.toggle_current_player()
            reversi_board.modify_score_board()
            win_list.append(reversi_board.check_for_win())
            reversi_board.reset_board()

        print (win_list)
        print (sim_no)
        reversi_board.pretty_print_score_board()

        # plot the cumulative no of wins/tie
        winner_list_cumul = [[sum([1 if win_list[i] == -1 else 0 for i in range(j)]) for j in range(num_matches)], 
                             [sum([1 if win_list[i] == 0  else 0 for i in range(j)]) for j in range(num_matches)], 
                             [sum([1 if win_list[i] == 1  else 0 for i in range(j)]) for j in range(num_matches)]]


        dir_name = "reversi with board size " + str(board_size) + " and " + str(num_matches) + " matches"
        try:
            os.mkdir(dir_name)
        except OSError:
            pass
        fig_name = os.path.join(dir_name, str(sim_no) + ".png")
        plt.figure()
        plt.plot([i for i in range(1, num_matches + 1)], winner_list_cumul[0], label = "Black")
        plt.plot([i for i in range(1, num_matches + 1)], winner_list_cumul[1], label = "Tie")
        plt.plot([i for i in range(1, num_matches + 1)], winner_list_cumul[2], label = "White")
        # plt.xticks([i for i in range(1, num_matches)])
        plt.xlabel('Match No')
        plt.ylabel('Total Cumulative Count')
        plt.legend(loc = 2)
        plt.title(dir_name + " sim no " + str(sim_no))
        plt.savefig(fig_name, dpi = 300)

num_simulations = 5
num_matches = 10
board_size = 8
if __name__ == "__main__":
    main()