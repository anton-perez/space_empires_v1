import sys
sys.path.append('')
from player import *
from game import *
sys.path.append('strategies')
from bum_rush import *
from smart_rush import *



num_wins = {1: 0, 2: 0}

for _ in range(50):
  players = [Player(SmartRush()), Player(BumRush())]
  game = Game(players)
  game.run_to_completion()
  winner = game.winner
  num_wins[winner] += 1

print('Player 1 SmartRush', num_wins)

num_wins = {1: 0, 2: 0}

for _ in range(50):
  players = [Player(BumRush()), Player(SmartRush())]
  game = Game(players)
  game.run_to_completion()
  winner = game.winner
  num_wins[winner] += 1

print('Player 2 SmartRush', num_wins)