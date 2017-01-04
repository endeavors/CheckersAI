from checkers import Checkers

def getPlayerNames():
    player_a = input("Enter Player A's name: ").strip()
    if not player_a:
        player_a = "Player A"

    player_b = input("Enter Player B's name: ").strip()
    if not player_b:
        player_b = "Player B"
    return (player_a,player_b)

#NOTE: MUST BE RUN WITH PYTHON 3
if __name__ == '__main__':
    player_names = getPlayerNames()
    checkers = Checkers()
    checkers.playGame(player_names)
