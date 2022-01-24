from random import random
from ship_data import *
import math
import sys
sys.path.append('')
from ships import *
from colony import *

class Player():
  def __init__(self, strategy):
    self.player_num = None
    self.home_colony = None
    self.ships = []
    self.colonies = []
    self.ship_counter = {name:0 for name in ship_objects}
    self.cp = 0
    self.strategy = strategy

  def set_player_number(self, player_num):
    self.player_num = player_num

  def set_home_colony(self, colony):
    colony.set_player_number(self.player_num)
    self.home_colony = colony

  def add_ship(self, ship):
    ship.set_player_number(self.player_num)
    self.ship_counter[ship.name] += 1
    ship.set_ship_number(self.ship_counter[ship.name])
    self.ships.append(ship)

  def remove_ship(self, ship):
    self.ships.remove(ship)

  def add_colony(self, colony):
    colony.set_player_number(self.player_num)
    self.colonies.append(colony)

  def get_ships_by_type(self, type_name):
    return [ship for ship in self.ships if ship.name == type_name]

  def get_info_from_ship(self, ship):
    return ship.__dict__()

  def choose_translation(self, ship_info, choices):
    return self.strategy.choose_translation(ship_info, choices)

  def choose_target(self, ship_info, combat_order_info):
    return self.strategy.choose_target(ship_info, combat_order_info)

  def buy_ships(self, cp):
    return self.strategy.buy_ships(cp)