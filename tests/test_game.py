import sys
sys.path.append('')
from player import *
from game import *
sys.path.append('strategies')
from test_strategy import *

players = [Player(CustomStrategy()), Player(CustomStrategy())]
game = Game(players)
game.run_to_completion()