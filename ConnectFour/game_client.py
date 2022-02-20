import socket
import sys

class Client():
    def __init__(self, target_host, target_port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((target_host, target_port))
    
class Game():

    def __init__(self):
        #  initialise a 7x6 2d array filled with '-' for the board
        self.gamestate = [['-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-'], ['-', '-', '-', '-', '-', '-']]

    def print_state(self):
        print("\n")
        print([str(i) for i in range(6)])
        for row in self.gamestate:
            print(row)

    #  place a counter at the first free position in the column selected and return that position as a tuple
    def insert_counter(self, column, ourTurn):
        # starting at the bottom of the board, check for a free space
        for i in range(6, -1, -1):
            if(self.gamestate[i][column] == '-'):
                if ourTurn:
                    self.gamestate[i][column] = 'X'
                    return (i, column)
                else:
                    self.gamestate[i][column] = 'O'
                    return (i, column)

    #  given a row indice on the board, check for 4 consecutive counters
    def check_win_row(self, row):
        counters = 0
        # check the current row for a win
        for i in range(0, 6):
            if self.gamestate[row][i] == 'X':
                counters += 1
                print("Winning row counters: %d" % counters)
                if counters == 4:
                    return True
            if self.gamestate[row][i] == '-':
                counters = 0
        return False

    def check_win_column(self, column):
        counters = 0
        # check the current column for a win
        for i in range(0, 7):
            if self.gamestate[i][column] == 'X':
                counters += 1
                print("Winning column counters: %d" % counters)
                if counters == 4:
                    return True
            if self.gamestate[i][column] == '-':
                counters = 0
        return False

    #  given a boardspace (row, column) check for a win, return Boolean
    def check_win(self, boardspace):
        win = False
        row = boardspace[0]
        column = boardspace[1]

        row_win = self.check_win_row(row)
        column_win = self.check_win_column(column)
        if row_win or column_win:
            win = True
        return win


if __name__ == "__main__":
    
    target_host = "192.168.1.102"
    target_port = 4444

    client = Client(target_host, target_port)
    client_socket = client.client

    game = Game()

    ##  Server will send "start" to let us know if we're allowed to speak first
    received = client_socket.recv(1024).decode('utf-8')

    ##  We're the first to go so send our move to the server then listen for reply
    if "start" in received:

        game.print_state()
        chosenColumn = input("Choose a column: ")
        client_socket.send(chosenColumn.encode('utf-8'))
        game.insert_counter(int(chosenColumn), True)
        game.print_state()

        chosenColumn = client_socket.recv(1024).decode('utf-8')
        game.insert_counter(int(chosenColumn), False)
        game.print_state()

    ##  If we were not the first to speak then update the game board based on player 1's move
    else:

        chosenColumn = int(received)
        game.insert_counter(chosenColumn, False)
        game.print_state()

    ##  Send and receive messages now
    while True:

        game.print_state()
        chosenColumn = input("Choose a column: ")
        boardspace = game.insert_counter(int(chosenColumn), True)
        if game.check_win(boardspace):
            print("YOU WIN!!!")
        game.print_state()
        client_socket.send(chosenColumn.encode('utf-8'))



        received = client_socket.recv(1024).decode('utf-8')

        chosenColumn = int(received)
        boardspace = game.insert_counter(chosenColumn, False)
        game.print_state()
        if game.check_win(boardspace):
            print("YOU LOSE!!!")
