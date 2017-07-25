import numpy as np
import reversi
import multi_layer_perceptron as mlp
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
# import seaborn as sns
import datetime
import random
import pickle

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
        plt.savefig(os.path.join('monte_carlo_simulation_graphs', fig_name.replace(' ', '_')), dpi = 300)

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
    fig.savefig(os.path.join('match_stats_between_different_players', fig_name + ".png").replace(' ', '_'), dpi = 300)
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
    fig.savefig(os.path.join('match_stats_between_different_players', fig_name + ".png").replace(' ', '_'), dpi = 300)
    print (y_labels)
    print (win_counts)

def get_nn_evolved_from_ga(board_size, num_matches = 4, num_nn = 40, num_generations = 100):
    input_layer_size = board_size * board_size
    output_layer_size = board_size * board_size
    hidden_layers = [board_size * board_size, board_size * board_size]
    # reversi_board = reversi.reversi(board_size)
    if num_nn%2 != 0:
        num_nn += 1
    nn_list = [mlp.multi_layer_perceptron(input_layer_size, output_layer_size, hidden_layers) for _ in range(num_nn)]
    # print (nn_list)
    for gen_no in range(num_generations):
        nn_score_track = [0] * num_nn
        if gen_no%50 == 0:
            print (str(datetime.datetime.now()) + ' Generation no ' + str(gen_no))
        random.shuffle(nn_list)
        for i in range(0, num_nn, 2):
            # play i and i + 1 against each other, total of 4 matches
            # player 1 is i and player 2 is i + 1
            for _ in range(2):
                for player_1 in [-1, 1]:
                    player_2 = -1 * player_1
                    
                    reversi_board = reversi.reversi(board_size)

                    while (reversi_board.check_for_win() == 2):
                        # reversi_board.pretty_print()
                        if reversi_board.player == player_1:
                            nn_pred = nn_list[i].predict(reversi_board.board)
                        else:
                            nn_pred = nn_list[i + 1].predict(reversi_board.board)
                        # print (nn_pred)
                        nn_pred = nn_pred.reshape(input_layer_size, -1)
                        move = [[j, nn_pred[j]] for j in reversi_board.possible_moves_dict[reversi_board.player]]
                        move = sorted(move, key = lambda x:x[1], reverse = True)[0][0]
                        row, col = reversi_board.get_row_col_from_index(move)
                        reversi_board.play_a_move(row, col)
                        reversi_board.toggle_current_player()

                    # assign the points to winners and losers
                    winner = reversi_board.check_for_win()
                    if winner == 0:
                        pass
                    elif (player_1 == winner):
                        nn_score_track[i] += 1
                    elif (player_2 == winner):
                        nn_score_track[i + 1] += 1
                    # print (player_1, player_2, winner, nn_list[i], nn_list[i + 1])
                    # print (nn_score_track)

        # select the top half, make the duplicates and make the mutations
        # print (nn_score_track)
        nn_sort_list = [[i, nn_score_track[i]] for i in range(num_nn)]
        nn_sort_list = sorted(nn_sort_list, key = lambda x: x[1], reverse = True)
        nn_list = [nn_list[x[0]] for x in nn_sort_list]
        # keep only half of the top performers
        nn_list = nn_list[: num_nn//2 + 1]
        for i in range(num_nn // 2):
            nn_list.append(mlp.multi_layer_perceptron(input_layer_size, output_layer_size, hidden_layers))
            nn_list[-1].set_weights(nn_list[i].get_weights())
            nn_list[-1].tweak_weights()
            nn_list[-1].set_bias(nn_list[i].get_bias())
            nn_list[-1].tweak_bias()

    with open(os.path.join('nn_pickles', 'nn_list_' + str(num_nn) + 'nn_' + str(num_generations) + 'gen'), 'wb') as f:
        pickle.dump(nn_list, f)

def select_best_nn_league_matches(board_size, num_nn = 40, num_generations = 1000):
    input_layer_size = board_size * board_size
    output_layer_size = board_size * board_size
    hidden_layers = [board_size * board_size, board_size * board_size]

    with open(os.path.join('nn_pickles', 'nn_list_' + str(num_nn) + 'nn_' + str(num_generations) + 'gen'), 'rb') as f:
        nn_list = pickle.load(f)
    
    print ('Total number of neural nets is ' + str(len(nn_list)))
    # print (len(nn_list))

    nn_score_track = [0] * len(nn_list)

    for i in range(len(nn_list) - 1):
        for j in range(i + 1, len(nn_list)):
            print ('Playing match between ' + str(i) + ' and ' + str(j))
            for player_1 in [-1, 1]:
                player_2 = -1 * player_1
                reversi_board = reversi.reversi(board_size)

                while (reversi_board.check_for_win() == 2):
                    # reversi_board.pretty_print()
                    if reversi_board.player == player_1:
                        nn_pred = nn_list[i].predict(reversi_board.board)
                    else:
                        nn_pred = nn_list[i + 1].predict(reversi_board.board)
                    # print (nn_pred)
                    nn_pred = nn_pred.reshape(input_layer_size, -1)
                    move = [[j, nn_pred[j]] for j in reversi_board.possible_moves_dict[reversi_board.player]]
                    move = sorted(move, key = lambda x:x[1], reverse = True)[0][0]
                    row, col = reversi_board.get_row_col_from_index(move)
                    reversi_board.play_a_move(row, col)
                    reversi_board.toggle_current_player()

                # assign the points to winners and losers
                winner = reversi_board.check_for_win()
                if winner == 0:
                    pass
                elif (player_1 == winner):
                    nn_score_track[i] += 1
                elif (player_2 == winner):
                    nn_score_track[i + 1] += 1
                # print (player_1, player_2, winner, nn_list[i], nn_list[i + 1])
                # print (nn_score_track)

    # select the top half, make the duplicates and make the mutations
    # print (nn_score_track)
    nn_sort_list = [[i, nn_score_track[i]] for i in range(len(nn_list))]
    nn_sort_list = sorted(nn_sort_list, key = lambda x: x[1], reverse = True)
    nn_list = [nn_list[x[0]] for x in nn_sort_list]

    print (nn_sort_list)
    with open(os.path.join('nn_pickles', 'nn_list_' + str(num_nn) + 'nn_' + str(num_generations) + 'gen_best'), 'wb') as f:
        pickle.dump(nn_list, f)
        
def main_nn_vs_learned(board_size = 8, num_matches = 500):
    input_layer_size = board_size * board_size
    output_layer_size = board_size * board_size
    hidden_layers = [board_size * board_size, board_size * board_size]

    reversi_board = reversi.reversi(board_size)
    win_list = {'nn_player':{-1:0, 1:0},
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

    with open(os.path.join('nn_pickles', 'nn_list_40nn_1000gen_best'), 'rb') as f:
        nn_list = pickle.load(f)

    for game_no in range(num_matches):
        if (game_no + 1)%10 == 0:
            print (str(datetime.datetime.now()) + ' Playing game no ' + str(game_no))
        nn_player = -1 if np.random.randint(0, 2) == 0 else 1
        # nn_player = 1
            
        while (reversi_board.check_for_win() == 2):
            # reversi_board.pretty_print()
            if reversi_board.player == nn_player:
                nn_pred = nn_list[0].predict(reversi_board.board)
                nn_pred = nn_pred.reshape(input_layer_size, -1)
                move = [[j, nn_pred[j]] for j in reversi_board.possible_moves_dict[reversi_board.player]]
                move = sorted(move, key = lambda x:x[1], reverse = True)[0][0]
            else:
                # move = reversi_board.select_a_move()
                move = reversi_board.select_a_move()
            row, col = reversi_board.get_row_col_from_index(move)
            reversi_board.play_a_move(row, col)
            reversi_board.toggle_current_player()
        # reversi_board.pretty_print()

        winner = reversi_board.check_for_win()
        if (nn_player == -1 and winner == -1):
            win_list['nn_player'][-1] += 1
        elif (nn_player == -1 and winner == 1):
            win_list['monte_carlo_player'][1] += 1
        elif (nn_player == 1 and winner == 1):
            win_list['nn_player'][1] += 1
        elif (nn_player == 1 and winner == -1):
            win_list['monte_carlo_player'][-1] += 1
        else:
            win_list['ties'] += 1
        
        reversi_board.reset_board()

    # fig_name = str(num_matches) + " matches between random and comp players comp always white"
    fig_name = str(num_matches) + " matches between neural net 1000 generations and monte carlo players"
    fig, ax = plt.subplots(figsize=(15,10))

    y_labels = ['nn player \nwins as black', 
                'nn player \nwins as white',
                'monte carlo \nplayer wins\n as black',
                'monte carlo \nplayer wins\n as white',
                'tie']
    y_pos = np.arange(len(y_labels))
    win_counts = [win_list['nn_player'][-1],
                  win_list['nn_player'][1],
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
    fig.savefig(os.path.join('match_stats_between_different_players', fig_name + ".png").replace(' ', '_'), dpi = 300)
    print (y_labels)
    print (win_counts)

def main():
    print ('Inside main()')
    num_simulations = 10
    num_matches = 2000
    board_size = 8

    # main_sim(board_size, num_simulations, num_matches)
    # main_learned_vs_random(board_size, 500)
    # main_tree_vs_learned(board_size, 20)
    # get_nn_evolved_from_ga(board_size, num_generations = 200)
    # select_best_nn_league_matches(board_size)
    main_nn_vs_learned(board_size)

if __name__ == "__main__":
    main()