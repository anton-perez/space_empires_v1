import sys
sys.path.append('')
from player import *
from game import *
sys.path.append('strategies')
from test_strategy import *
from custom_strategy import *
from wait_strategy import *


players = [Player(CustomStrategy()), Player(WaitStrategy((0,-1)))]
game = Game(players)
game.run_until(4)
game.complete_movement_phase()

print('Testing if defender is first in combat order...')
assert game.get_all_ships_on_space(game.combat_coords[0])[0].player_number == 2
print('PASSED')