

board = [6, 6, 6, 6, 6, 6, 0, 6, 6, 6, 6, 6, 6, 0]


def print_board():
    print(f"\n  |{board[0]}|{board[1]}|{board[2]}|{board[3]}|{board[4]}|{board[5]}|  ")
    print(f"{board[13]} |{board[12]}|{board[11]}|{board[10]}|{board[9]}|{board[8]}|{board[7]}| {board[6]}\n")


def move(location, amount, player1_turn):
    if player1_turn:
        for i in range(amount):
            location -= 1
            if location == -1:
                location -= 1
            board[location] += 1
            if location == 6:
                pass
            elif board[location] == 1 and i + 1 == amount:
                player1_turn = False
    else:
        for i in range(amount):
            location -= 1
            if location == -8:
                location -= 1
            board[location] += 1
            if location == 13:
                pass
            elif board[location] == 1 and i + 1 == amount:
                player1_turn = True
    return player1_turn


def main():
    player1_turn = True
    finshed_game = False
    while not finshed_game:
        print_board()
        if player1_turn:
            player_1_move = input("Player 1: choose a pile to play: ")
            match int(player_1_move):
                case 1:
                    player1_turn = move(12, board[12], True)
                    board[12] = 0
                case 2:
                    player1_turn = move(11, board[11], True)
                    board[11] = 0
                case 3:
                    player1_turn = move(10, board[10], True)
                    board[10] = 0
                case 4:
                    player1_turn = move(9, board[9], True)
                    board[9] = 0
                case 5:
                    player1_turn = move(8, board[8], True)
                    board[8] = 0
                case 6:
                    player1_turn = move(7, board[7], True)
                    board[7] = 0
        else:
            player_2_move = input("Player 2: choose a pile to play: ")
            match int(player_2_move):
                case 1:
                    player1_turn = move(0, board[0], False)
                    board[0] = 0
                case 2:
                    player1_turn = move(1, board[1], False)
                    board[1] = 0
                case 3:
                    player1_turn = move(2, board[2], False)
                    board[2] = 0
                case 4:
                    player1_turn = move(3, board[3], False)
                    board[3] = 0
                case 5:
                    player1_turn = move(4, board[4], False)
                    board[4] = 0
                case 6:
                    player1_turn = move(5, board[5], False)
                    board[5] = 0


if __name__ == '__main__':
    main()
