import numpy as np

class reversi():
    '''
    1 is white and -1 is black, standard convention from now on
    note that the pieces at the four centre squares are already occupied
    as per standard reversi rules
    '''
    def __init__(self, board_size):
        '''
        initialization method for a reversi board of the given size
        TODO : add custom starting methods like black and white handicap
        '''
        self.board = np.zeros(board_size * board_size)
        self.board_size = board_size
        # fill the centre 4 pieces, can make this dynamic also
        self.board[self.get_index_from_row_col(self.board_size//2 - 1, self.board_size//2 - 1)] = 1
        self.board[self.get_index_from_row_col(self.board_size//2    , self.board_size//2    )] = 1
        self.board[self.get_index_from_row_col(self.board_size//2    , self.board_size//2 - 1)] = -1
        self.board[self.get_index_from_row_col(self.board_size//2 - 1, self.board_size//2    )] = -1

        # set the current player to black or -1
        self.player = -1
        self.possible_moves_dict = {-1 : [], 1 : []}

        self.modify_possible_moves_dict()

        # a dictionary to store the moves played by both the players
        self.played_moves_dict = {-1 : [], 1 : []}

        # initialize the array keeping track of the weights
        self.score_board = np.zeros(board_size * board_size)

    def reset_board(self):
        self.board = np.zeros(self.board_size * self.board_size)
        # fill the centre four pieces
        self.board[self.get_index_from_row_col(self.board_size//2 - 1, self.board_size//2 - 1)] = -1
        self.board[self.get_index_from_row_col(self.board_size//2    , self.board_size//2    )] = -1
        self.board[self.get_index_from_row_col(self.board_size//2    , self.board_size//2 - 1)] = 1
        self.board[self.get_index_from_row_col(self.board_size//2 - 1, self.board_size//2    )] = 1

        # set the current player to black or -1
        self.player = -1
        self.possible_moves_dict = {-1 : [], 1 : []}

        self.modify_possible_moves_dict()

        # a dictionary to store the moves played by both the players
        self.played_moves_dict = {-1 : [], 1 : []}

    def modify_score_board(self):
        winner = self.check_for_win()
        if winner == -1 or winner == 1:
            for i in self.played_moves_dict[winner]:
                self.score_board[i] += 1
            for i in self.played_moves_dict[-1 * winner]:
                self.score_board[i] -= 1

    def initialize_custom_score_board(self, custom_score_board):
        '''
        pass a 1d numpy array here which has a custome set of weights
        '''
        # self.score_board = np.array([556,-107,79,37,103,43,59,323,\
                                    # -111,-227,155,77,-29,29,-201,-31,\
                                    # 125,-73,13,-42,-223,17,-215,33,\
                                    # 27,-129,-33,0,0,-199,13,121,\
                                    # 49,23,3,0,0,101,-85,-191,\
                                    # 99,-99,-9,-44,-95,19,-67,69,\
                                    # -26,-214,1,-43,51,-13,33,-139,\
                                    # 506,33,25,67,-121,49,-74,225])
        self.score_board = np.array(custom_score_board)

    def select_a_move(self):
        max_score = np.max([self.score_board[i] for i in self.possible_moves_dict[self.player]])
        possible_moves_list = [i for i in self.possible_moves_dict[self.player] if self.score_board[i] == max_score]
        return (possible_moves_list[np.random.randint(0, len(possible_moves_list))])

    def select_a_move_randomly(self):
        return (self.possible_moves_dict[self.player][np.random.randint(0, len(self.possible_moves_dict[self.player]))])

    def select_a_move_from_tree(self):
        '''
        This function builds a few trees by playing all the positions
        and checks which one has the maximum no of coins after playing
        that move
        '''
        board_copy = np.array(self.board)
        num_coins = []
        current_possible_moves = list(self.possible_moves_dict[self.player])
        for pos in current_possible_moves:
            row, col = self.get_row_col_from_index(pos)
            self.play_a_move(row, col)
            num_coins.append(len(np.where(self.board == self.player)[0]))
            self.board = np.array(board_copy)
        self.board = np.array(board_copy)
        self.modify_possible_moves_dict()
        max_num_coins = max(num_coins)
        max_coins_moves = [current_possible_moves[i] for i in range(len(current_possible_moves)) if num_coins[i] == max_num_coins]
        return (max_coins_moves[np.random.randint(0, len(max_coins_moves))])

    def modify_possible_moves_dict(self):
        self.possible_moves_dict[self.player] = self.calculate_possible_moves()
        self.toggle_current_player()
        self.possible_moves_dict[self.player] = self.calculate_possible_moves()
        self.toggle_current_player()

    def modify_played_moves_dict(self, move_index):
        self.played_moves_dict[self.player].append(move_index)

    def get_row_col_from_index(self, index):
        return([index//self.board_size, index - self.board_size * (index//self.board_size)])

    def get_index_from_row_col(self, row, col):
        return (row * self.board_size + col)

    def pretty_print_score_board(self):
        print ()
        # for i in range(self.board_size):
            # print (self.board[self.board_size * i : self.board_size * (i + 1)])
        newBoard = []
        for i in range(self.board_size):
            newBoard.append([0] * self.board_size)

        for i in range(self.board_size):
            for j in range(self.board_size):
                newBoard[i][j] = int(self.score_board[self.get_index_from_row_col(i, j)])

        print('\n'.join([''.join(['{:6}'.format(item) for item in row]) for row in newBoard]))
        print ()

    def pretty_print(self):
        print ()
        # for i in range(self.board_size):
            # print (self.board[self.board_size * i : self.board_size * (i + 1)])
        newBoard = []
        for i in range(self.board_size):
            newBoard.append([0] * self.board_size)

        for i in range(self.board_size):
            for j in range(self.board_size):
                newBoard[i][j] = int(self.board[self.get_index_from_row_col(i, j)])

        print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in newBoard]))
        print ()

    def pretty_print_highliting_possible_moves(self, possible_moves_list):
        newBoard = []
        for i in range(self.board_size):
            newBoard.append([0] * self.board_size)

        for i in range(self.board_size):
            for j in range(self.board_size):
                newBoard[i][j] = 2 if self.get_index_from_row_col(i, j) in possible_moves_list else int(self.board[self.get_index_from_row_col(i, j)])

        print('\n'.join([''.join(['{:3}'.format(item) for item in row]) for row in newBoard]))

    def get_board_size(self):
        return (self.board_size)

    def get_current_player(self):
        return (self.player)

    def toggle_current_player(self):
        self.player *= -1

    def check_row_col_valid(self, row, col):
        '''
        check of the index calculated based on row and col
        falls in the range [0, self.board_size ^ 2), and also, the row and col
        must be in range [0, self.board_sixe)
        '''
        index = self.get_index_from_row_col(row, col)
        if 0 <= index and index < self.board_size * self.board_size and \
           0 <= row and row < self.board_size and 0 <= col and col < self.board_size:
           return (True)
        return (False)

    def modify_board_index(self, index):
        self.board[index] = self.player

    def get_empty_neighbors_indices(row, col):
        # only the index is passed if col is None
        indices_list = []
        for horizontal_movement in [-1, 0, 1]:
            for vertical_movement in [-1, 0, 1]:
                if vertical_movement == 0 and horizontal_movement == 0:
                    continue
                index = self.get_index_from_row_col(row + horizontal_movement, col + vertical_movement)
                if self.check_row_col_valid(row + horizontal_movement, col + vertical_movement):
                    if self.board[index] == 0:
                        indices_list.append(index)

        return (indices_list)

    def play_a_move(self, row, col):
        # function to play a move
        # check if the current move is legitimate
        # then modify this cell and all possible cells which can be modified
        if self.get_index_from_row_col(row, col) in self.possible_moves_dict[self.player]:
            self.modify_board_index(self.get_index_from_row_col(row, col))
            for horizontal_movement in [-1, 0, 1]:
                for vertical_movement in [-1, 0, 1]:
                    if vertical_movement == 0 and horizontal_movement == 0:
                        continue
                    if self.check_row_col_valid(row + horizontal_movement, col + vertical_movement):
                        if (self.board[self.get_index_from_row_col(row + horizontal_movement, col + vertical_movement)] == -1 * self.player):
                            self.traverse_a_line(row + horizontal_movement, col + vertical_movement, horizontal_movement, vertical_movement, True)
                    else:
                        pass

        self.modify_played_moves_dict(self.get_index_from_row_col(row, col))
        self.modify_possible_moves_dict()

    def traverse_lines_all_directions(self, row, col):
        # this function allows to traverse in all the 8 directions and find out if it's
        # possible to move in any direction from the current row, col
        moves_list = []
        possible_moves_list = []
        for horizontal_movement in [-1, 0, 1]:
            for vertical_movement in [-1, 0, 1]:
                if vertical_movement == 0 and horizontal_movement == 0:
                    continue
                index = self.get_index_from_row_col(row + horizontal_movement, col + vertical_movement)
                if self.check_row_col_valid(row + horizontal_movement, col + vertical_movement):
                    if (self.board[index] == 0):
                        # keep moving in the opposite direction to check if all the coins
                        # are of the same opposite color until the last coin in that direction
                        # which should be of the same colour

                        # the same function can be used to play a legitimate move using the modify_board argument
                        if(self.traverse_a_line(row + horizontal_movement, col + vertical_movement, -horizontal_movement, -vertical_movement)):
                            moves_list.append(index)

        return (moves_list)

    def traverse_a_line(self, row, col, horizontal_movement, vertical_movement, modify_board = False):
        num_pos_covered = 1
        move_possible = False
        positions_to_modify = []
        positions_to_modify.append(self.get_index_from_row_col(row, col))
        # if modify_board:
            # self.board[self.get_index_from_row_col(row, col)] = self.player
        while 1:
            # print (num_pos_covered, horizontal_movement, vertical_movement, pos, row, col)
            # print (self.board[self.get_index_from_row_col(row - num_pos_covered * horizontal_movement, col - num_pos_covered * vertical_movement)])
            index = self.get_index_from_row_col(row + num_pos_covered * horizontal_movement, col + num_pos_covered * vertical_movement)
            if self.check_row_col_valid(row + num_pos_covered * horizontal_movement, col + num_pos_covered * vertical_movement):
                if (self.board[index] == -1 * self.player):
                    positions_to_modify.append(index)
                    num_pos_covered += 1

                if (self.board[index] == self.player):
                    move_possible = True
                    if modify_board:
                        # print (positions_to_modify, self.get_row_col_from_index(positions_to_modify[0]))
                        for pos in positions_to_modify:
                            self.modify_board_index(pos)
                    break
                if (self.board[index] == 0):
                    break
            else:
                break
        return (move_possible)

    def calculate_possible_moves(self):
        # player must be 1 or -1
        # get the current indices where the opposite colour is present
        opposite_color_indices = np.where(self.board == -1 * self.player)[0]
        possible_moves_list = []
        for pos in opposite_color_indices:
            row, col = self.get_row_col_from_index(pos)
            # print (pos, self.traverse_lines_all_directions(row, col))
            moves_list = self.traverse_lines_all_directions(row, col)
            if (len(moves_list)):
                for move in moves_list:
                    if move not in possible_moves_list:
                        possible_moves_list.append(move)
        return (possible_moves_list)

    def check_for_win(self):
        '''
        for a win or tie to happen, both the parties should have no possible moves left
        check this using the dictionary of possible moves, bothe lengths must be zero
        also, winner is decided based on which player has more no of coins
        return 0 for tie, 2 if the game can be played
        '''
        # print ('######')
        # print (self.possible_moves_dict[-1], self.possible_moves_dict[1])
        # print ('######')
        
        if (len(self.possible_moves_dict[-1]) == 0 and len(self.possible_moves_dict[1]) == 0):
            # the match has ended
            black_coins_on_board = len(np.where(self.board == -1)[0])
            white_coins_on_board = len(np.where(self.board == 1)[0])
            if (black_coins_on_board > white_coins_on_board):
                return (-1)
            elif (white_coins_on_board > black_coins_on_board):
                return (1)
            else:
                # tie
                return (0)
        elif (len(self.possible_moves_dict[self.player]) == 0):
            self.toggle_current_player()
            # game can be played
            return (2)
        else:
            return (2)

    def basic_game_simulator(self):
        while (self.check_for_win() == 2):
            self.pretty_print()
            self.pretty_print_highliting_possible_moves(self.possible_moves_dict[self.player])
            row, col = self.get_row_col_from_index(self.possible_moves_dict[self.player][np.random.randint(0, len(self.possible_moves_dict[self.player]))])
            # print (self.possible_moves_dict[self.player])
            # print (row, col)
            self.play_a_move(row, col)
            self.toggle_current_player()
        self.pretty_print()
        print (self.played_moves_dict[-1])
        print (self.played_moves_dict[1])
        print ('\nThe Winner is ' + str(self.check_for_win()))


def main_check():
    myBoard = reversi(8)
    myBoard.pretty_print()
    print (myBoard.get_board_size())
    print (myBoard.get_current_player())
    print (myBoard.possible_moves_dict[myBoard.player])
    for i in myBoard.possible_moves_dict[myBoard.player]:
        print (myBoard.get_row_col_from_index(i))
    print (myBoard.get_current_player())
    myBoard.pretty_print_highliting_possible_moves(myBoard.possible_moves_dict[myBoard.player])
    # myBoard.play_a_move(1, 3)
    myBoard.play_a_move(2, 4)
    myBoard.pretty_print()
    print (myBoard.get_current_player())
    myBoard.pretty_print_highliting_possible_moves(myBoard.possible_moves_dict[myBoard.player])

def main():
    myBoard = reversi(8)
    myBoard.basic_game_simulator()

if __name__ == "__main__":
    main()

