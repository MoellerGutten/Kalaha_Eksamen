import random


class kalaha:
    def __init__(self, board):
        self.board = board

    def check_win(self):
        if self.board[12] + self.board[11] + self.board[10] + self.board[9] + self.board[8] + self.board[7] == 0 or self.board[0] + self.board[1] + self.board[2] + \
                self.board[3] + self.board[4] + self.board[5] == 0:
            if self.board[6] > self.board[13]:
                print("Player 1 won")
            elif self.board[6] < self.board[13]:
                print("Player 2 won")
            else:
                print("It is a draw")
            return True
        else:
            return False

    def console_board_print(self):
        print(f"\n  |{self.board[0]}|{self.board[1]}|{self.board[2]}|{self.board[3]}|{self.board[4]}|{self.board[5]}|  ")
        print(f"{self.board[13]} |{self.board[12]}|{self.board[11]}|{self.board[10]}|{self.board[9]}|{self.board[8]}|{self.board[7]}| {self.board[6]}\n")

    def move(self, location, player1_turn):
        # If the player choices a hole that has 0 ball, it chocies the hole opposite
        amount = self.board[location]
        if amount == 0:
            # dist is asigned the amount of hole it is from player1's goal
            dist = location - 6
            # location is asigned to the opposite hole
            location = 6 - dist
            # amount is changed to the new holes amount
            amount = self.board[location]

        start_location = location
        self.board[location] = 0
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
                self.board[location] += 1

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
                self.board[location] += 1

                # Checks if the last ball went into the players goal. if it did, it gives the player another turn
                if (location == 13 or location == -1) and i + 1 == amount:
                    player1_turn = False
                else:
                    player1_turn = True
        return self.board, player1_turn

    def bot_move(self):
        moves = {}
        test_board = []
        for i in range(6):
            if i == 0:
                moves, empty = self.minimax(True)
            else:
                new_moves, new_board = self.minimax(True, test_board, moves)
                moves = new_moves
                test_board = new_board
        if moves == "done":
            return "Stop"
        if max(moves.values()) == -1 or max(moves.values()) == 0:
            while True:
                ran_num = random.randint(0, 5)
                if self.board[ran_num] != 0:
                    return ran_num
        else:
            self.move(max(moves, key=moves.get), False)

    def minimax(self, max_turn, tested_board=None, best_possible_move=None):
        enemy_best_possible_move = {}
        motified_board = []
        if best_possible_move is None:
            best_possible_move = {}
            has_seleted_values = False
        else:
            has_seleted_values = True
        if self.check_win():
            return "Done"
        if max_turn:
            if best_possible_move is not None:
                i = 0
                tested_board = []
                for element in self.board:
                    tested_board.append(element)
                    i += 1
                start_score = tested_board[13]
            else:
                start_score = tested_board[13]
            for y in range(6):
                outcome = 0
                score, motified_board = self.try_move(tested_board, y, tested_board[y], False)
                if score > start_score:
                    outcome += 1
                if score > start_score + 1:
                    outcome += 2
                else:
                    outcome -= 1
                min_list = self.minimax(False, motified_board)
                if score > max(min_list.values()) + 2:
                    outcome += 1
                if has_seleted_values:
                    best_possible_move[y] = outcome + best_possible_move[y]
                else:
                    best_possible_move[y] = outcome
            return best_possible_move, motified_board
        else:
            for y in range(6):
                outcome = 0
                start_score = tested_board[6]
                score, motified_board = self.try_move(tested_board, y, tested_board[y], False)
                if score > start_score:
                    outcome += 1
                if score > start_score + 1:
                    outcome += 2
                else:
                    outcome -= 1
                enemy_best_possible_move[y] = outcome
            return enemy_best_possible_move

    def try_move(self, new_board, location, amount, player1_turn):
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
                    new_board[6] += 2

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
                    new_board[13] += 2
            send_board = []
            for element in new_board:
                send_board.append(element)
            return new_board[13], send_board


start_board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]
game_engine = kalaha(start_board)
print(game_engine.move(12, True))
game_engine.console_board_print()
print(game_engine.bot_move())
game_engine.console_board_print()
