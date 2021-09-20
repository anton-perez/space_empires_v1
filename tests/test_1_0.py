import sys
sys.path.append('')
from player import *
sys.path.append('games')
from game import *
sys.path.append('strategies')
from custom_strategy import *
# sys.path.append('players')
# from random_player import *
# from custom_player import *

players = [Player(CustomStrategy()), Player(CustomStrategy())]
game = Game(players)
game.run_to_completion()