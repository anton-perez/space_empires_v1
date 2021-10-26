from random import random
import math
import sys
sys.path.append('')
from ships import *
from colony import *

class RandomPlayer():
  def __init__(self):
    self.player_number = None
    self.home_colony = None
    self.ships = []
    self.colonies = []

  def set_player_number(self, n):
    self.player_number = n

  def set_home_colony(self, colony):
    colony.set_player_number(self.player_number)
    self.home_colony = colony

  def add_ship(self, ship):
    ship.set_player_number(self.player_number)
    ship.set_ship_number(len(self.get_ships_by_type(ship.name))+1)
    self.ships.append(ship)

  def remove_ship(self, ship):
    self.ships.remove(ship)

  def add_colony(self, colony):
    colony.set_player_number(self.player_number)
    self.colonies.append(colony)

  def get_ships_by_type(self, type_name):
    return [ship for ship in self.ships if ship.name == type_name]

  def choose_translation(self, board, choices, ship):
    random_idx = math.floor(len(choices) * random())
    return choices[random_idx]

  def choose_target(self, opponent_ships):
    random_idx = math.floor(len(opponent_ships) * random())
    return opponent_ships[random_idx]
