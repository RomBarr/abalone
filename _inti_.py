from search import *
from abalone import *


if __name__ == "__main__":
    """gam"""

    abalone = abalone_game()
    utility = abalone.play_game(alpha_beta_player, query_player) # computer moves first
    if (utility < 0):
        print("min won the game")
    else:
        print("max won the game")
