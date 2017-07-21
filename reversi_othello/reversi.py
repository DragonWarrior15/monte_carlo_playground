import numpy as np

class reversi():
    '''
    1 is white and -1 is black, standard convention from now on
    note that the pieces at the four centre squares are already occupied
    '''
    def __init__(self, board_size):
        '''
        initialization method for a reversi board of the given size
        TODO : add custom starting methods like black and white handicap
        '''
        self.board = np.zeros(board_size * board_size)
        self.board_size = board_size
        # fill the centre 4 pieces, can make this dynamic also
        self.board[self.board_size * (self.board_size//2 - 1) + self.board_size//2 - 1] = 1
        self.board[self.board_size * (self.board_size//2    ) + self.board_size//2    ] = 1
        self.board[self.board_size * (self.board_size//2 - 1) + self.board_size//2    ] = -1
        self.board[self.board_size * (self.board_size//2    ) + self.board_size//2 - 1] = -1

    def pretty_print(self):
        for i in range(self.board_size):
            print (self.board[self.board_size * i : self.board_size * (i + 1)])

    def get_board_size(self):
        return (self.board_size)


def main():
    myBoard = reversi(8)
    myBoard.pretty_print()
    print (myBoard.get_board_size())

if __name__ == "__main__":
    main()

