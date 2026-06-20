import random

def race_game():
    players = {"Player1": 0, "Player2": 0}
    while players["Player1"] < 20 and players["Player2"] < 20:
        for player in players:
            roll = random.randint(1, 6)
            players[player] += roll
            print(f"{player} rolled {roll} and now has {players[player]} points.")
    for player, score in players.items():
        if score >= 20:
            print(f"{player} wins!")