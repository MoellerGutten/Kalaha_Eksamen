import random
import time


class kalaha:
    def __init__(self, board):
        self.board = board

    # Checks if one of the sides has no balls, if this is the case returns true and who run
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

    # Moves the hole according to which turn it is and what hole was choicen
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

    # Finds out what the best move for the bot is and runs the move() funtion with that move
    def bot_move(self):
        future_moves = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        enemy_future_moves = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        # Checks how many points the enemy and the bot gets six turn forward for each of the possible moves the bot can make
        for i in range(6):
            # creates the variable test_board that is a replica of the real board
            test_board = []
            for element in self.board:
                test_board.append(element)
            # Simulates one of the six possible moves
            score, motified_board = self.try_move(test_board, i, test_board[i], False)
            # adds the score to the bot moveset dict
            future_moves[i] += score
            # Runs minimax() funktion to get the best enemy move with the manipulated board from try_move() funktion
            enemy_move = self.minimax(False, motified_board)
            # Simulates the best enemy move from minimax() funktion
            enemy_score, motified_board = self.try_move(motified_board, enemy_move, motified_board[enemy_move], True)
            # adds the score to the enemy moveset dict
            enemy_future_moves[i] += enemy_score
            # give the test_board variable the value of the manipulated board from trymove() motified_board
            test_board = motified_board
            # runs a for loop six times that finds the best move from minimax() and simulates it with try_move() and adds the scores from try_move() to the scoreset dicts
            for __ in range(3):
                bmove = self.minimax(True, test_board)
                score, motified_board = self.try_move(test_board, bmove, test_board[bmove], False)
                future_moves[i] += score
                enemy_move = self.minimax(False, motified_board)
                enemy_score, motified_board = self.try_move(motified_board, enemy_move, motified_board[enemy_move], True)
                enemy_future_moves[i] += enemy_score
                test_board = motified_board

        # creates a empty dict called mini__max_diff
        mini_max_diff = {}
        # fills the mini_max_diff variable with the differance between the bots scores and the enemies scores
        for i in range(len(future_moves)):
            diff =  future_moves[i] - enemy_future_moves[i]
            mini_max_diff[i] = diff

        # gives the bmove variable the key with the max value in mini_max_diff
        bmove = max(mini_max_diff, key=mini_max_diff.get)
        # gives the wmove variable the key with the min value in future_moves
        wmove = min(future_moves, key=future_moves.get)

        # the variable location is asigned to the opposite hole
        dist = bmove - 6
        location = 6 - dist

        # checks if the best move is also the worst move, which means it will always pick move 0 which we don't want
        if future_moves[bmove] == future_moves[wmove]:
            # Picks a random number between 0-5, if the random hol contains something other the 0, uses that move else it keeps seaching
            while True:
                ran_num = random.randint(0, 5)
                if self.board[ran_num] != 0:
                    return self.move(ran_num, False)
        # Checks if the best move hol is empty and if the oppsoite hol is empty too
        elif self.board[bmove] == 0 and self.board[location] == 0:
            # Picks a random number between 0-5, if the random hol contains something other the 0, uses that move else it keeps seaching
            while True:
                ran_num = random.randint(0, 5)
                if self.board[ran_num] != 0:
                    return self.move(ran_num, False)
        else:
            # runs the move() funktion with the best move calculated
            return self.move(bmove, False)

    # calculates the best move the bot or the enemy can make based on the number of points there goal has risen
    def minimax(self, max_turn, tested_board):
        enemy_best_possible_move = {}
        best_possible_move = {}
        combo_moves = []
        if max_turn:
            combo_moves = [0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 0]
            # give the variable start_score the value of the bots (player 2) goals value
            start_score = tested_board[13]
            # calculates the points on every possible move and adds it to a dict
            for y in range(6):
                outcome = 0
                # simulates y move with the given board tested_board
                score, motified_board = self.try_move(tested_board, y, tested_board[y], False)
                # Calculates the number of similarities of the changed board with the combo_moves list
                combo_count = sum(x == y for x, y in zip(motified_board[7:13], combo_moves[7:13]))
                # Switch case that adds the right number to the outcome variable depender on how many similartities the to board have
                match int(combo_count):
                    case 1:
                        outcome += 1
                    case 2:
                        outcome += 2
                    case 3:
                        outcome += 3
                    case 4:
                        outcome += 4
                    case 5:
                        outcome += 5
                    case 6:
                        outcome += 6

                # if else statements that adds the right number to the outcome varaible depender on how high the simulated y move had
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
                # minius the outcome variable with how good the enemyscore did using the funktion check_enemyscore()
                outcome -= self.check_enemyscore(motified_board, False)
                best_possible_move[y] = outcome
            print(best_possible_move)
            best_move = max(best_possible_move, key=best_possible_move.get)
            return best_move
        else:
            combo_moves = [1, 2, 3, 4, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0]
            start_score = tested_board[6]
            for y in range(6):
                outcome = 0
                score, motified_board = self.try_move(tested_board, y, tested_board[y], True)
                combo_count = sum(x == y for x, y in zip(motified_board[7:13], combo_moves[7:13]))
                print(combo_count)
                match int(combo_count):
                    case 1:
                        outcome += 1
                    case 2:
                        outcome += 2
                    case 3:
                        outcome += 3
                    case 4:
                        outcome += 4
                    case 5:
                        outcome += 5
                    case 6:
                        outcome += 6

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

            # creates a new board send_board, because otherwise the board will be manipulated
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

            # creates a new board send_board, because otherwise the board will be manipulated
            send_board = []
            for element in new_board:
                send_board.append(element)
            return new_board[13], send_board

    # Calculates the enemyscore just like the minimax() funktion. this funktion is created the eleminate the recursion depth limit
    def check_enemyscore(self, board, turn):
        outcome = None
        if turn:
            combo_moves = [0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 0]
            start_score = board[13]
        else:
            combo_moves = [1, 2, 3, 4, 5, 6, 0, 0, 0, 0, 0, 0, 0, 0]
            start_score = board[6]
        for y in range(6):
            outcome = 0
            score, motified_board = self.try_move(board, y, board[y], turn)
            combo_count = sum(x == y for x, y in zip(motified_board[7:13], combo_moves[7:13]))
            match int(combo_count):
                case 1:
                    outcome += 1
                case 2:
                    outcome += 2
                case 3:
                    outcome += 3
                case 4:
                    outcome += 4
                case 5:
                    outcome += 5
                case 6:
                    outcome += 6

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

        return outcome
