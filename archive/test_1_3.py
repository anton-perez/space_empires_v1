import sys
sys.path.append('')
from player import *
from game import *
sys.path.append('strategies')
from test_strategy import *
from custom_strategy import *
from wait_strategy import *


players = [Player(CustomStrategy()), Player(WaitStrategy((1,0)))]
game = Game(players)
game.run_to_completion()

print('Testing if winner is consistent...')
assert game.winner == 1
print('PASSED')
