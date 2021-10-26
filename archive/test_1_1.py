import sys
sys.path.append('')
from player import *
from game import *
sys.path.append('strategies')
from test_strategy import *
from custom_strategy import *


players = [Player(TestStrategy()), Player(TestStrategy())]
game = Game(players)
game.run_until(3)
init_coords = players[0].ships[0].coords
game.run_until(4)
post_coords = players[0].ships[0].coords

print('Testing out of bounds protocol...')
assert init_coords == post_coords
print('PASSED')
