

board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]


# prints the board
def print_board():
    print(f"\n  |{board[0]}|{board[1]}|{board[2]}|{board[3]}|{board[4]}|{board[5]}|  ")
    print(f"{board[13]} |{board[12]}|{board[11]}|{board[10]}|{board[9]}|{board[8]}|{board[7]}| {board[6]}\n")


# Checks if the game has ended and printes out who won
def check_win():
    if board[13] + board[12] + board[11] + board[10] + board[9] + board[8] + board[7] == 0 or board[0] + board[1] + board[2] + board[3] + board[4] + board[5] == 0:
        print_board()
        if board[6] > board[13]:
            print("Player 1 won")
        elif board[6] < board[13]:
            print("Player 2 won")
        else:
            print("It is a draw")
        return True


# Moves the hole according to which turn it is and what hole was choicen
def move(location, amount, player1_turn):
    # If the player choices a hole that has 0 ball, it chocies the hole opposite
    if amount == 0:
        # dist is asigned the amount of hole it is from player1's goal
        dist = location - 6
        # location is asigned to the opposite hole
        location = 6 - dist
        # amount is changed to the new holes amount
        amount = board[location]

    start_location = location
    board[location] = 0
    if player1_turn:
        # for loop that loops thougth the kalaha board based on the amount of balls in the selected hole
        # it takes the poision of the hole selected and moves though the loop backwards
        for i in range(amount):
            location -= 1
            # checks if the location has gone out of index and puts it back on track
            if location == -15:
                # find_back is asigned the location of how many time the for loop can loop before it get out of index
                find_back = 15 + start_location
                # remain findes the amount of time it needs to go back in the loop from the startpoint
                remain = find_back % 14
                # location is now asigned to the right location, the loop went out of index
                location = start_location - remain
            # checks if the location is about to put a ball into the enemies goal and move it 1 more back
            if location == -1:
                location -= 1

            # gives the reached hole 1 ball
            board[location] += 1

            # Checks if the last ball went into the players goal. if it did, it gives the player another turn
            if location == 6 and i + 1 == amount:
                player1_turn = True
            else:
                player1_turn = False
    else:
        # for loop that loops thougth the kalaha board based on the amount of balls in the selected hole
        for i in range(amount):
            location -= 1
            # checks if the location has gone out of index and puts it back on track
            if location == -15:
                # find_back is asigned the location of how many time the for loop can loop before it get out of index
                find_back = 15 + start_location
                # remain findes the amount of time it needs to go back in the loop from the startpoint
                remain = find_back % 14
                # location is now asigned to the right location, the loop went out of index
                location = start_location - remain
            # checks if the location is about to put a ball into the enemies goal and move it 1 more back
            if location == -8:
                location -= 1

            # gives the reached hole 1 ball
            board[location] += 1

            # Checks if the last ball went into the players goal. if it did, it gives the player another turn
            if (location == 13 or location == -1) and i + 1 == amount:
                player1_turn = False
            else:
                player1_turn = True
    return player1_turn


# Runs a while loop, that ends if finshed_game.
# It takes a string userinput and runs it though a switch case that run the function move with the correct parameters
def main():
    player1_turn = True
    finshed_game = False
    while not finshed_game:
        print_board()
        if player1_turn:
            # Switch case that puts the correct value in the function move based on the players input
            player_1_move = input("Player 1: choose a pile to play: ")
            match int(player_1_move):
                case 1:
                    player1_turn = move(12, board[12], True)
                case 2:
                    player1_turn = move(11, board[11], True)
                case 3:
                    player1_turn = move(10, board[10], True)
                case 4:
                    player1_turn = move(9, board[9], True)
                case 5:
                    player1_turn = move(8, board[8], True)
                case 6:
                    player1_turn = move(7, board[7], True)
        else:
            # Switch case that puts the correct value in the fucktion move based on the players input
            player_2_move = input("Player 2: choose a pile to play: ")
            match int(player_2_move):
                case 1:
                    player1_turn = move(0, board[0], False)
                case 2:
                    player1_turn = move(1, board[1], False)
                case 3:
                    player1_turn = move(2, board[2], False)
                case 4:
                    player1_turn = move(3, board[3], False)
                case 5:
                    player1_turn = move(4, board[4], False)
                case 6:
                    player1_turn = move(5, board[5], False)
        finshed_game = check_win()


if __name__ == '__main__':
    main()
