import numpy as np
import reversi
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
# import seaborn as sns
import datetime

def main_sim(board_size = 8, num_simulations = 1, num_matches = 20):
    for sim_no in range(num_simulations):
        reversi_board = reversi.reversi(board_size)
        win_list = []
        for game_no in range(num_matches):
            if (game_no + 1) % 100 == 0:
                print (str(datetime.datetime.now()) + ' playing game ' + str(game_no) + ' in simulation no ' + str(sim_no))
            while (reversi_board.check_for_win() == 2):
                if (game_no + 1) % 100 == 0:
                    reversi_board.pretty_print()
                move = reversi_board.select_a_move()
                # print (move)
                row, col = reversi_board.get_row_col_from_index(move)
                reversi_board.play_a_move(row, col)
                reversi_board.toggle_current_player()
            if (game_no + 1) % 100 == 0:
                reversi_board.pretty_print()
            reversi_board.modify_score_board()
            win_list.append(reversi_board.check_for_win())
            reversi_board.reset_board()

        # print (win_list)
        # print (sim_no)
        reversi_board.pretty_print_score_board()

        # plot the cumulative no of wins/tie
        winner_list_cumul = [[sum([1 if win_list[i] == -1 else 0 for i in range(j)]) for j in range(num_matches)], 
                             [sum([1 if win_list[i] == 0  else 0 for i in range(j)]) for j in range(num_matches)], 
                             [sum([1 if win_list[i] == 1  else 0 for i in range(j)]) for j in range(num_matches)]]


        dir_name = "reversi with board size " + str(board_size) + " and " + str(num_matches) + " matches"
        try:
            os.mkdir(dir_name.replace(' ', '_'))
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
        plt.savefig(fig_name.replace(' ', '_'), dpi = 300)

def main_learned_vs_random(board_size = 8, num_matches = 10):
    reversi_board = reversi.reversi(board_size)
    win_list = {'random_player':{-1:0, 1:0},
                'comp_player':{-1:0, 1:0},
                'ties':0}
    reversi_board.initialize_custom_score_board(
                   np.array([245,-24,56,78,0,10,30,186,\
                            -76,-129,-74,28,-68,-26,-20,-28,\
                            34,60,46,-78,-112,44,-76,8,\
                            34,-56,-2,0,0,-32,28,-22,\
                            12,18,-120,0,0,46,-16,48,\
                            6,-114,72,-72,-118,-14,-118,66,\
                            48,-86,-130,176,-70,56,2,-27,\
                            228,-81,128,-32,28,-6,0,176]))

    for game_no in range(num_matches):
        if (game_no + 1)%100 == 0:
            print ('Playing game no ' + str(game_no))
        random_player = -1 if np.random.randint(0, 2) == 0 else 1
        # random_player = 1

        # if random_player == -1:
            # move = reversi_board.select_a_move_randomly()
            # row, col = reversi_board.get_row_col_from_index(move)
            # reversi_board.play_a_move(row, col)
            # reversi_board.toggle_current_player()
            
        while (reversi_board.check_for_win() == 2):
            if reversi_board.player == random_player:
                move = reversi_board.select_a_move_randomly()
            else:
                move = reversi_board.select_a_move()
            row, col = reversi_board.get_row_col_from_index(move)
            reversi_board.play_a_move(row, col)
            reversi_board.toggle_current_player()

        winner = reversi_board.check_for_win()
        if (random_player == -1 and winner == -1):
            win_list['random_player'][-1] += 1
        elif (random_player == -1 and winner == 1):
            win_list['comp_player'][1] += 1
        elif (random_player == 1 and winner == 1):
            win_list['random_player'][1] += 1
        elif (random_player == 1 and winner == -1):
            win_list['comp_player'][-1] += 1
        else:
            win_list['ties'] += 1
        
        reversi_board.reset_board()

    # fig_name = str(num_matches) + " matches between random and comp players comp always white"
    fig_name = str(num_matches) + " matches between random and comp players"
    fig, ax = plt.subplots(figsize=(15,10))

    y_labels = ['random player \nwins as black', 
                'random player \nwins as white',
                'comp player \nwins as black',
                'comp player \nwins as white',
                'tie']
    y_pos = np.arange(len(y_labels))
    win_counts = [win_list['random_player'][-1],
                  win_list['random_player'][1],
                  win_list['comp_player'][-1],
                  win_list['comp_player'][1],
                  win_list['ties']]

    rects = ax.barh(y_pos, win_counts, align = 'center', color = 'blue')

    labels = [str(round((100.0 * i)/num_matches, 2)) + "%" for i in win_counts]

    # for rect, label in zip(rects, labels):
        # width = rect.get_width()
        # if width == 0:
            # ax.text(width + 0.5, rect.get_y() + rect.get_height()/2, label, 
                    # ha='left', va='center', size = 'x-large', weight = 'bold')
        # else:
            # ax.text(width - 0.5, rect.get_y() + rect.get_height()/2, label, 
                    # ha='left', va='center', color = 'white', size = 'x-large',
                    # weight = 'bold')

    # ax.set_xticks([i for i in range(1, num_matches)])
    # ax.set_xticklabels(size = 'x-large')
    ax.set_xlabel('Counts', size = 'x-large')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels, size = 'x-large')
    ax.set_title(fig_name, size = 'xx-large')
    fig.savefig((fig_name + ".png").replace(' ', '_'), dpi = 300)
    print (y_labels)
    print (win_counts)

def main_tree_vs_learned(board_size = 8, num_matches = 10):
    reversi_board = reversi.reversi(board_size)
    win_list = {'tree_player':{-1:0, 1:0},
                'monte_carlo_player':{-1:0, 1:0},
                'ties':0}
    reversi_board.initialize_custom_score_board(
                   np.array([245,-24,56,78,0,10,30,186,\
                            -76,-129,-74,28,-68,-26,-20,-28,\
                            34,60,46,-78,-112,44,-76,8,\
                            34,-56,-2,0,0,-32,28,-22,\
                            12,18,-120,0,0,46,-16,48,\
                            6,-114,72,-72,-118,-14,-118,66,\
                            48,-86,-130,176,-70,56,2,-27,\
                            228,-81,128,-32,28,-6,0,176]))

    for game_no in range(num_matches):
        # if (game_no + 1)%5 == 0:
        print (str(datetime.datetime.now()) + ' Playing game no ' + str(game_no))
        tree_player = -1 if np.random.randint(0, 2) == 0 else 1
        # tree_player = 1

        # if tree_player == -1:
            # move = reversi_board.select_a_move_randomly()
            # row, col = reversi_board.get_row_col_from_index(move)
            # reversi_board.play_a_move(row, col)
            # reversi_board.toggle_current_player()
            
        while (reversi_board.check_for_win() == 2):
            # reversi_board.pretty_print()
            if reversi_board.player == tree_player:
                move = reversi_board.select_a_move_randomly()
            else:
                # move = reversi_board.select_a_move()
                move = reversi_board.select_a_move_from_tree(player = reversi_board.player, 
                                                             current_player = reversi_board.player)
            row, col = reversi_board.get_row_col_from_index(move)
            reversi_board.play_a_move(row, col)
            reversi_board.toggle_current_player()
        # reversi_board.pretty_print()

        winner = reversi_board.check_for_win()
        if (tree_player == -1 and winner == -1):
            win_list['tree_player'][-1] += 1
        elif (tree_player == -1 and winner == 1):
            win_list['monte_carlo_player'][1] += 1
        elif (tree_player == 1 and winner == 1):
            win_list['tree_player'][1] += 1
        elif (tree_player == 1 and winner == -1):
            win_list['monte_carlo_player'][-1] += 1
        else:
            win_list['ties'] += 1
        
        reversi_board.reset_board()

    # fig_name = str(num_matches) + " matches between random and comp players comp always white"
    fig_name = str(num_matches) + " matches between depth 3 tree and monte carlo players"
    fig, ax = plt.subplots(figsize=(15,10))

    y_labels = ['tree player \nwins as black', 
                'tree player \nwins as white',
                'monte carlo \nplayer wins\n as black',
                'monte carlo \nplayer wins\n as white',
                'tie']
    y_pos = np.arange(len(y_labels))
    win_counts = [win_list['tree_player'][-1],
                  win_list['tree_player'][1],
                  win_list['monte_carlo_player'][-1],
                  win_list['monte_carlo_player'][1],
                  win_list['ties']]

    rects = ax.barh(y_pos, win_counts, align = 'center', color = 'blue')

    labels = [str(round((100.0 * i)/num_matches, 2)) + "%" for i in win_counts]

    # for rect, label in zip(rects, labels):
        # width = rect.get_width()
        # if width == 0:
            # ax.text(width + 0.5, rect.get_y() + rect.get_height()/2, label, 
                    # ha='left', va='center', size = 'x-large', weight = 'bold')
        # else:
            # ax.text(width - 0.5, rect.get_y() + rect.get_height()/2, label, 
                    # ha='left', va='center', color = 'white', size = 'x-large',
                    # weight = 'bold')

    # ax.set_xticks([i for i in range(1, num_matches)])
    # ax.set_xticklabels(size = 'x-large')
    ax.set_xlabel('Counts', size = 'x-large')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(y_labels, size = 'x-large')
    ax.set_title(fig_name, size = 'xx-large')
    fig.savefig((fig_name + ".png").replace(' ', '_'), dpi = 300)
    print (y_labels)
    print (win_counts)

def main():
    print ('Inside main()')
    num_simulations = 10
    num_matches = 2000
    board_size = 8

    # main_sim(board_size, num_simulations, num_matches)
    # main_learned_vs_random(board_size, 500)
    main_tree_vs_learned(board_size, 20)

if __name__ == "__main__":
    main()