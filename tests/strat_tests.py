import sys
sys.path.append('')
from player import *
from game import *
sys.path.append('strategies')
from test_strategy import *
from cayden_strategy import *
from justin_strategy import *
from maia_strategy import *
from charlie_strategy import *
from william_strategy import *

'''
players = [Player(CustomStrategy()), Player(CustomStrategy())]
game = Game(players)
game.run_to_completion()

players = [Player(CaydenStrategy()), Player(CaydenStrategy())]
game = Game(players)
game.run_to_completion()

players = [Player(JustinStrategy()), Player(JustinStrategy())]
game = Game(players)
game.run_to_completion()

players = [Player(MaiaStrategy()), Player(MaiaStrategy())]
game = Game(players)
game.run_to_completion()

players = [Player(CharlieStrategy()), Player(CharlieStrategy())]
game = Game(players)
game.run_to_completion()

players = [Player(WilliamStrategy()), Player(WilliamStrategy())]
game = Game(players)
game.run_to_completion()
'''
players = [Player(MaiaStrategy()), Player(CustomStrategy())]
game = Game(players)
game.run_to_completion()
print(game.winner)