import random

board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]


# prints the board
def print_board():
    print(f"\n  |{board[0]}|{board[1]}|{board[2]}|{board[3]}|{board[4]}|{board[5]}|  ")
    print(f"{board[13]} |{board[12]}|{board[11]}|{board[10]}|{board[9]}|{board[8]}|{board[7]}| {board[6]}\n")


def test_print(some_board):
    print(f"Dette er et test af board {some_board}")
    print(f"|{some_board[0]}|{some_board[1]}|{some_board[2]}|{some_board[3]}|{some_board[4]}|{some_board[5]}|  ")
    print(f"{some_board[13]} |{some_board[12]}|{some_board[11]}|{some_board[10]}|{some_board[9]}|{some_board[8]}|{some_board[7]}| {some_board[6]}\n")


# Checks if the game has ended and printes out who won
def check_win():
    if board[12] + board[11] + board[10] + board[9] + board[8] + board[7] == 0 or board[0] + board[1] + board[2] + \
            board[3] + board[4] + board[5] == 0:
        print_board()
        if board[6] > board[13]:
            print("Player 1 won")
        elif board[6] < board[13]:
            print("Player 2 won")
        else:
            print("It is a draw")
        return True
    else:
        return False


def bot_move():
    future_moves = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    enemy_future_moves = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for i in range(6):
        test_board = []
        for element in board:
            test_board.append(element)
        score, motified_board = try_move(test_board, i, test_board[i], False)
        future_moves[i] += score
        enemy_move, empty = minimax(False, motified_board)
        enemy_score, motified_board = try_move(motified_board, enemy_move, motified_board[enemy_move], True)
        enemy_future_moves[i] += enemy_score
        test_board = motified_board
        for y in range(6):
            bmove = minimax(True, test_board)
            score, motified_board = try_move(test_board, bmove, test_board[bmove], False)
            future_moves[i] += score
            enemy_move, empty = minimax(False, motified_board)
            enemy_score, motified_board = try_move(motified_board, enemy_move, motified_board[enemy_move], True)
            enemy_future_moves[i] += enemy_score
            test_board = motified_board
    mini_max_diff = {}
    for i in range(len(future_moves)):
        diff = future_moves[i] - enemy_future_moves[i]
        mini_max_diff[i] = diff

    bmove = max(mini_max_diff, key=mini_max_diff.get)
    wmove = min(future_moves, key=future_moves.get)

    dist = bmove - 6
    # location is asigned to the opposite hole
    location = 6 - dist

    if bmove == "done":
        return "Stop"
    if future_moves[bmove] == future_moves[wmove]:
        while True:
            ran_num = random.randint(0, 5)
            if board[ran_num] != 0:
                return ran_num
    elif board[bmove] == 0 and board[location] == 0:
        while True:
            ran_num = random.randint(0, 5)
            if board[ran_num] != 0:
                return ran_num
    else:
        return bmove


def minimax(max_turn, tested_board):
    enemy_best_possible_move = {}
    best_possible_move = {}
    if check_win():
        return "Done"
    if max_turn:
        start_score = tested_board[13]
        for y in range(6):
            outcome = 0
            score, motified_board = try_move(tested_board, y, tested_board[y], False)
            if score > start_score + 2:
                outcome += 3
            elif score > start_score + 1:
                outcome += 2
            elif score > start_score:
                outcome += 1
            else:
                outcome -= 3
            best_possible_move[y] = outcome
        best_move = max(best_possible_move, key=best_possible_move.get)
        return best_move
    else:
        start_score = tested_board[6]
        for y in range(6):
            outcome = 0
            score, motified_board = try_move(tested_board, y, tested_board[y], True)
            if score > start_score + 2:
                outcome += 3
            elif score > start_score + 1:
                outcome += 2
            elif score > start_score:
                outcome += 1
            else:
                outcome -= 3
            enemy_best_possible_move[y] = outcome
        enemy_best_move = max(enemy_best_possible_move, key=enemy_best_possible_move.get)
        return enemy_best_move, enemy_best_possible_move[enemy_best_move]


def try_move(old_board, location, amount, player1_turn):
    new_board = []
    for element in old_board:
        new_board.append(element)
    # If the player choices a hole that has 0 ball, it chocies the hole opposite
    if amount == 0:
        # dist is asigned the amount of hole it is from player1's goal
        dist = location - 6
        # location is asigned to the opposite hole
        location = 6 - dist
        # amount is changed to the new holes amount
        amount = new_board[location]

    start_location = location
    new_board[location] = 0
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
            new_board[location] += 1

            # Checks if the last ball went into the players goal. if it did, it gives the player another turn
            if location == 6 and i + 1 == amount:
                new_board[6] += 3

        send_board = []
        for element in new_board:
            send_board.append(element)
        return new_board[6], send_board
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
            new_board[location] += 1

            # Checks if the last ball went into the players goal. if it did, it gives the player another turn
            if (location == 13 or location == -1) and i + 1 == amount:
                new_board[13] += 1

        send_board = []
        for element in new_board:
            send_board.append(element)
        return new_board[13], send_board


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
            # Switch case that puts the correct value in the fucktion move based on the players input
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
            best_bot_move = bot_move()
            if best_bot_move == "Stop":
                finshed_game = True
                break
            best_bot_move_amount = board[best_bot_move]
            print(f"Bot: chooses pile {best_bot_move}")
            player1_turn = move(best_bot_move, best_bot_move_amount, False)
        finshed_game = check_win()


if __name__ == '__main__':
    main()
