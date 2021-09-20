from random import random
import math
import sys
sys.path.append('')
from ships import *
from colony import *

class Player():
  def __init__(self, strategy):
    self.player_number = None
    self.home_colony = None
    self.ships = []
    self.colonies = []
    self.strategy = strategy
    self.strategy.set_player(self)

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
    return self.strategy.choose_translation(board, choices, ship)

  def choose_target(self, opponent_ships):
    return self.strategy.choose_target(opponent_ships)