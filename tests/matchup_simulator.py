import sys
sys.path.append('')
from player import *
from game import *
sys.path.append('strategies')
from justin_comp_strat import * #CompetitionStrat
from cayden_comp_strat import * #CaydenStrat
from william_comp_strat import * #WallStrat
from maia_comp_strat import * #BattleStrat
from charlie_strategy import * #MoveToOpponent
from smart_rush import *



num_wins = {1: 0, 2: 0}

for _ in range(50):
  players = [Player(MoveToOpponent()), Player(BattleStrat())]
  game = Game(players)
  game.run_to_completion()
  winner = game.winner
  num_wins[winner] += 1

print('Player 1 SmartRush', num_wins)

num_wins = {1: 0, 2: 0}

for _ in range(50):
  players = [Player(BattleStrat()), Player(MoveToOpponent())]
  game = Game(players)
  game.run_to_completion()
  winner = game.winner
  num_wins[winner] += 1

print('Player 2 SmartRush', num_wins)