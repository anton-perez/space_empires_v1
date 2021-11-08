import sys
sys.path.append('')
from player import *
from game import *
sys.path.append('strategies')
from test_strategy import *
from priority_attacker import *



num_wins = {1: 0, 2: 0}

for _ in range(1000):
  players = [Player(PriorityAttacker()), Player(CustomStrategy())]
  game = Game(players)
  game.run_to_completion()
  winner = game.winner
  num_wins[winner] += 1

print('Player 1 PriorityAttacker', num_wins)

num_wins = {1: 0, 2: 0}

for _ in range(1000):
  players = [Player(CustomStrategy()), Player(PriorityAttacker())]
  game = Game(players)
  game.run_to_completion()
  winner = game.winner
  num_wins[winner] += 1

print('Player 2 PriorityAttacker', num_wins)
