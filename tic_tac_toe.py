print("**************************")
print("  Welcome to Tic Tac Toe!  ")
print("**************************")

def print_board(board):
    print()
    print(board[0], "|", board[1], "|", board[2])
    print("--+---+--")
    print(board[3], "|", board[4], "|", board[5])
    print("--+---+--")
    print(board[6], "|", board[7], "|", board[8])
    print()


def check_winner(board, player):
    win = [
        [0,1,2], [3,4,5], [6,7,8],
        [0,3,6], [1,4,7], [2,5,8],
        [0,4,8], [2,4,6]
    ]

    for combo in win:
        if all(board[i] == player for i in combo):
            return True
    return False


def board_full(board):
    return all(cell in ["X", "O"] for cell in board)


board = ["1","2","3","4","5","6","7","8","9"]
current_player = "X"

while True:
    print_board(board)

    try:
        move = int(input(f"Player {current_player}, choose a position (1-9): ")) - 1

        if move < 0 or move > 8:
            print("Invalid position!")
            continue

        if board[move] in ["X", "O"]:
            print("That position is already taken!")
            continue

        board[move] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins!")
            break

        if board_full(board):
            print_board(board)
            print("🤝 It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

    except ValueError:
        print("Please enter a number from 1 to 9.")

print("Thanks for playing!")