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
        self.board[self.get_index_from_row_col(self.board_size//2 - 1, self.board_size//2 - 1)] = -1
        self.board[self.get_index_from_row_col(self.board_size//2    , self.board_size//2    )] = -1
        self.board[self.get_index_from_row_col(self.board_size//2    , self.board_size//2 - 1)] = 1
        self.board[self.get_index_from_row_col(self.board_size//2 - 1, self.board_size//2    )] = 1

    def get_row_col_from_index(self, index):
        return([index//self.board_size, index - self.board_size * (index//self.board_size)])

    def get_index_from_row_col(self, row, col):
        return (row * self.board_size + col)

    def pretty_print(self):
        for i in range(self.board_size):
            print (self.board[self.board_size * i : self.board_size * (i + 1)])

    def get_board_size(self):
        return (self.board_size)

    def get_possible_moves(self, player):
        # player must be 1 or -1
        # get the current indices where the opposite colour is present
        opposite_color_indices = np.where(self.board == -1 * player)[0]
        possible_moves_list = []
        for pos in opposite_color_indices:
            row, col = self.get_row_col_from_index(pos)
            # check if one of the nearby cells is empty
            for horizontal_movement in [-1, 0, 1]:
                for vertical_movement in [-1, 0, 1]:
                    if vertical_movement == 0 and horizontal_movement == 0:
                        continue
                    end_of_line = 0
                    try:
                        if (self.board[self.get_index_from_row_col(row + horizontal_movement, col + vertical_movement)] == 0):
                            # keep moving in the opposite direction to check if all the coins
                            # are of the same opposite color until the last coin in that direction
                            # which should be of the same colour
                            num_pos_covered = 1
                            while 1:
                                # print (num_pos_covered, horizontal_movement, vertical_movement, pos, row, col)
                                # print (self.board[self.get_index_from_row_col(row - num_pos_covered * horizontal_movement, col - num_pos_covered * vertical_movement)])
                                try:
                                    if (self.board[self.get_index_from_row_col(row - num_pos_covered * horizontal_movement,
                                                                          col - num_pos_covered * vertical_movement)] == -1 * player):
                                        num_pos_covered += 1
                                    if (self.board[self.get_index_from_row_col(row - num_pos_covered * horizontal_movement,
                                                                          col - num_pos_covered * vertical_movement)] == player):
                                        end_of_line = 1
                                        break
                                    if (self.board[self.get_index_from_row_col(row - num_pos_covered * horizontal_movement,
                                                                          col - num_pos_covered * vertical_movement)] == 0):
                                        break
                                except IndexError:
                                    break
                    except IndexError:
                        pass
                    if end_of_line == 1:
                        # add to the list of possible moves
                        possible_moves_list.append(self.get_index_from_row_col(row + horizontal_movement, col + vertical_movement))
        return (possible_moves_list)


def main():
    myBoard = reversi(8)
    myBoard.pretty_print()
    print (myBoard.get_board_size())
    print (myBoard.get_possible_moves(-1))
    for i in myBoard.get_possible_moves(-1):
        print (myBoard.get_row_col_from_index(i))

if __name__ == "__main__":
    main()

