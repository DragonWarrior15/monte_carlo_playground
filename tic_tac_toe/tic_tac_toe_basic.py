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
        if (curr_score_board[position[0], position[1]] > max_score):
            max_score = curr_score_board[position[0], position[1]]

    # get a list of all the board positions which have the max score
    max_score_positions = []
    for position in empty_positions:
        if (curr_score_board[position[0], position[1]] == max_score):
            max_score_positions.append(position)

    # randomly choose a position from amongst the above
    pos_to_return = max_score_positions[random.randint(0, len(max_score_positions) - 1)]

    # return the position
    return (pos_to_return)

def update_score_board(curr_score_board, curr_board, winner = None):
    if winner == None:
        return (curr_score_board)
    else:
        n = len(curr_board)
        for i in range(n):
            for j in range(n):
                curr_score_board[i][j] += winner * curr_board[i][j]
        return (curr_score_board)

def check_game_status(curr_board):
    n = len(curr_board)
    

num_simulations = 100
num_matches = 10
board_size = 3
win_list = []
# the main simulation
for _ in range(num_simulations):
    for _ in range(num_matches):
        # initialize the board
        game_board = []
        for i in range(board_size):
            game_board.append([0] * board_size)
        # initialize the score tracker
        score_board = []
        for i in range(board_size):
            score_board.append([0] * board_size)

        # play the game, X (-1) pays first
        player_1 = random.randint(0, 1) == 1 ? 1 : -1
        player_2 = -1 * player_1

