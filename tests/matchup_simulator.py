import sys
sys.path.append('')
from player import *
from game import *
sys.path.append('strategies')
from justin_comp_strat import * #CompetitionStrat
from cayden_comp_strat import * #CaydenStrat
from william_comp_strat import * #Custom
from maia_comp_strat import * #StraightToEnemyColony
from charlie_strategy import * #CharlieStrategy
from priority_attacker import *



num_wins = {1: 0, 2: 0}

for _ in range(50):
  players = [Player(Custom()), Player(CharlieStrategy())]
  game = Game(players)
  game.run_to_completion()
  winner = game.winner
  num_wins[winner] += 1

print('Player 1 PriorityAttacker', num_wins)

num_wins = {1: 0, 2: 0}

for _ in range(50):
  players = [Player(CharlieStrategy()), Player(Custom())]
  game = Game(players)
  game.run_to_completion()
  winner = game.winner
  num_wins[winner] += 1

print('Player 2 PriorityAttacker', num_wins)