'''
a simple python two machine player script where
the machines play using monte carlo simlulation and update
the scores in each cell using the end result of the game.
'''
import random

def get_empty_positions(curr_board):
    n = len(curr_board)
    return_list = []
    for i in range(n):
        for j in range(n):
            if curr_board[i][j] == 0:
                return_list.append([i, j])
    return (return_list)

def select_next_move(curr_score_board, curr_board):
    n = len(curr_board)
    empty_positions = get_empty_positions(curr_board)
    max_score = -100000000

    # get the maximum possible score in all the empty board positions
    for position in empty_positions:
        if (curr_score_board[position[0]][position[1]] > max_score):
            max_score = curr_score_board[position[0]][position[1]]

    # get a list of all the board positions which have the max score
    max_score_positions = []
    for position in empty_positions:
        if (curr_score_board[position[0]][position[1]] == max_score):
            max_score_positions.append(position)

    # randomly choose a position from amongst the above
    pos_to_return = max_score_positions[random.randint(0, len(max_score_positions) - 1)]

    # return the position
    return (pos_to_return)

def update_score_board(curr_score_board, curr_board, winner = 0):
    # there is a tie
    if winner == 0:
        return (curr_score_board)
    else:
        n = len(curr_board)
        for i in range(n):
            for j in range(n):
                curr_score_board[i][j] += winner * curr_board[i][j]
        return (curr_score_board)

def check_game_status(curr_board):
    n = len(curr_board)

def check_if_win(curr_board):
    n = len(curr_board)
    # check win in row
    for i in range(n):
        row_sum = sum([curr_board[i][j] for j in range(n)])
        if row_sum == -1 * n:
            return (-1)
        if row_sum == 1 * n:
            return (1)
    # check win in column
    for i in range(n):
        row_sum = sum([curr_board[j][i] for j in range(n)])
        if row_sum == -1 * n:
            return (-1)
        if row_sum == 1 * n:
            return (1)
    # check diagonal win
    diag_sum_1 = sum([curr_board[i][i] for i in range(n)])
    diag_sum_2 = sum([curr_board[n - 1 - i][i] for i in range(n)])
    if (diag_sum_1 == -1 * n or diag_sum_2 == -1 * n):
        return (-1)
    if (diag_sum_1 == 1 * n or diag_sum_2 == 1 * n):
        return (1)
    # check if any position is still empty
    for i in range(n):
        for j in range(n):
            if curr_board[i][j] == 0:
                return (n)
    # all positions seem to have been filled without any win
    # must be a tie then
    return (0)

def pretty_print_board(board):
    n = len(board)
    print ('########################')
    for i in range(n):
        print ([board[i][j] for j in range(n)])
    print ('########################')

num_simulations = 1
num_matches = 100
board_size = 3
win_list = []
# the main simulation
for _ in range(num_simulations):
    # initialize the score tracker
    score_board = []
    for i in range(board_size):
        score_board.append([0] * board_size)

    for _ in range(num_matches):
        # initialize the board
        game_board = []
        for i in range(board_size):
            game_board.append([0] * board_size)

        # play the game, X (-1) pays first
        player_1 = 1 if random.randint(0, 1) else -1
        player_2 = -1 * player_1

        curr_chance = -1
        while (check_if_win(game_board) == board_size):
            # pretty_print_board(game_board)
            next_move = select_next_move(score_board, game_board)
            game_board[next_move[0]][next_move[1]] = curr_chance
            curr_chance *= -1
        winner = check_if_win(game_board)
        win_list.append(winner)
        score_board = update_score_board(score_board, game_board, winner)
    # check how the score board looks
    pretty_print_board(score_board)
    # pretty_print_board(game_board)

with open('winner_list.csv', 'w') as f:
    # print (win_list)
    f.write('n'.join([str(x) for x in win_list]))
