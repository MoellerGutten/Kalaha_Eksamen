import random
import time


class kalaha:
    def __init__(self, board):
        self.board = board

    def check_win(self):
        if self.board[12] + self.board[11] + self.board[10] + self.board[9] + self.board[8] + self.board[7] == 0 or self.board[0] + self.board[1] + self.board[2] + \
                self.board[3] + self.board[4] + self.board[5] == 0:
            if self.board[6] > self.board[13]:
                return True, "Player 1 won"
            elif self.board[6] < self.board[13]:
                return True, "Player 2 won"
            else:
                return True, "It is a draw"
        else:
            return False, ""

    def console_board_print(self):
        print(f"\n  |{self.board[0]}|{self.board[1]}|{self.board[2]}|{self.board[3]}|{self.board[4]}|{self.board[5]}|  ")
        print(f"{self.board[13]} |{self.board[12]}|{self.board[11]}|{self.board[10]}|{self.board[9]}|{self.board[8]}|{self.board[7]}| {self.board[6]}\n")

    def move(self, location, player1_turn):
        saveMove = location
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
                if location == -1 or location == 13:
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
                if location == -8 or location == 6:
                    location -= 1

                # gives the reached hole 1 ball
                self.board[location] += 1

                # Checks if the last ball went into the players goal. if it did, it gives the player another turn
                if (location == 13 or location == -1) and i + 1 == amount:
                    player1_turn = False
                else:
                    player1_turn = True
        return saveMove, player1_turn

    def bot_move(self):
        future_moves = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        enemy_future_moves = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for i in range(6):
            test_board = []
            for element in self.board:
                test_board.append(element)
            score, motified_board = self.try_move(test_board, i, test_board[i], False)
            future_moves[i] += score
            enemy_move = self.minimax(False, motified_board)
            enemy_score, motified_board = self.try_move(motified_board, enemy_move, motified_board[enemy_move], True)
            enemy_future_moves[i] += enemy_score
            test_board = motified_board
            for __ in range(6):
                bmove = self.minimax(True, test_board)
                score, motified_board = self.try_move(test_board, bmove, test_board[bmove], False)
                future_moves[i] += score
                enemy_move = self.minimax(False, motified_board)
                enemy_score, motified_board = self.try_move(motified_board, enemy_move, motified_board[enemy_move], True)
                enemy_future_moves[i] += enemy_score
                test_board = motified_board
        mini_max_diff = {}
        for i in range(len(future_moves)):
            diff =  future_moves[i] - enemy_future_moves[i]
            mini_max_diff[i] = diff
        print("\n")
        print(mini_max_diff)
        print(future_moves)
        print(enemy_future_moves)

        bmove = max(mini_max_diff, key=mini_max_diff.get)
        print(bmove)
        wmove = min(future_moves, key=future_moves.get)

        dist = bmove - 6
        # location is asigned to the opposite hole
        location = 6 - dist

        if future_moves[bmove] == future_moves[wmove]:
            while True:
                ran_num = random.randint(0, 5)
                if self.board[ran_num] != 0:
                    return self.move(ran_num, False)
        elif self.board[bmove] == 0 and self.board[location] == 0:
            while True:
                ran_num = random.randint(0, 5)
                if self.board[ran_num] != 0:
                    return self.move(ran_num, False)
        else:
            return self.move(bmove, False)

    def minimax(self, max_turn, tested_board):
        enemy_best_possible_move = {}
        best_possible_move = {}
        if max_turn:
            start_score = tested_board[13]
            for y in range(6):
                outcome = 0
                score, motified_board = self.try_move(tested_board, y, tested_board[y], False)
                if score > start_score + 4:
                    outcome += 5
                elif score > start_score + 3:
                    outcome += 4
                elif score > start_score + 2:
                    outcome += 3
                elif score > start_score + 1:
                    outcome += 2
                elif score > start_score:
                    outcome += 1
                else:
                    outcome -= 1
                outcome -= self.check_enemyscore(motified_board, False)
                best_possible_move[y] = outcome
            best_move = max(best_possible_move, key=best_possible_move.get)
            return best_move
        else:
            start_score = tested_board[6]
            for y in range(6):
                outcome = 0
                score, motified_board = self.try_move(tested_board, y, tested_board[y], True)
                if score > start_score + 4:
                    outcome += 5
                elif score > start_score + 3:
                    outcome += 4
                elif score > start_score + 2:
                    outcome += 3
                elif score > start_score + 1:
                    outcome += 2
                elif score > start_score:
                    outcome += 1
                else:
                    outcome -= 1
                outcome -= self.check_enemyscore(motified_board, True)
                enemy_best_possible_move[y] = outcome
            enemy_best_move = max(enemy_best_possible_move, key=enemy_best_possible_move.get)
            return enemy_best_move

    def try_move(self, old_board, location, amount, player1_turn):
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
                if location == -1 or location == 13:
                    location -= 1

                # gives the reached hole 1 ball
                new_board[location] += 1

                # Checks if the last ball went into the players goal. if it did, it gives the player another turn
                if location == 6 and i + 1 == amount:
                    new_board[6] += 1

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
                if location == -8 or location == 6:
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

    def check_enemyscore(self, board, turn):
        enemy_outcome = 0
        outcome = None
        if turn:
            start_score = board[13]
        else:
            start_score = board[6]
        for y in range(6):
            outcome = 0
            score, __ = self.try_move(board, y, board[y], turn)
            if score > start_score + 4:
                outcome += 5
            elif score > start_score + 3:
                outcome += 4
            elif score > start_score + 2:
                outcome += 3
            elif score > start_score + 1:
                outcome += 2
            elif score > start_score:
                outcome += 1
            else:
                outcome -= 1
        if outcome == 5:
            enemy_outcome -= 4
        elif outcome == 4:
            enemy_outcome -= 3
        elif outcome == 3:
            enemy_outcome -= 2
        elif outcome == 2:
            enemy_outcome -= 1
        return enemy_outcome
