from random import random
import math
import sys
sys.path.append('')
from ships import *
from colony import *

class WaitStrategy():
  def __init__(self, move):
    self.player = None
    self.move = move
    self.turn = 0

  def set_player(self, player):
    self.player = player
  
  def get_ships_by_type(self, type_name):
    return [ship for ship in self.player.ships if ship.name == type_name]

  def choose_translation(self, board, choices, ship):
    board_len = len(board)
    mid_x = (board_len + 1) // 2
    if ship.coords == (mid_x-1, board_len-1):
      return self.move
    return (0,0)
    
  def choose_target(self, opponent_ships):
    random_idx = math.floor(len(opponent_ships) * random())
    return opponent_ships[random_idx]