from random import random
import math
import sys
sys.path.append('')
from ships import *
from colony import *

class CustomPlayer():
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

  def calc_distance(self, point_1, point_2):
    return (abs(point_2[0]-point_1[0])**2 + abs(point_2[1]-point_1[1])**2)**0.5

  def find_home_colonies(self, board):
    board_x, board_y = (len(board[0]), len(board))
    coords = []
    for y in range(board_y):
      for x in range(board_x):
        for obj in board[y][x]:
          is_opponent_home_colony = isinstance(obj, Colony) and obj.is_home_colony and obj.player_number != self.player_number
          if is_opponent_home_colony:
            coords.append((x,y))
    return coords

  def find_min_choice(self, choices, coord):
    min_choice = choices[0]
    min_distance = self.calc_distance(min_choice, coord)

    for choice in choices:
      if self.calc_distance(choice, coord) < min_distance:
        min_choice = choice
        min_distance = self.calc_distance(choice,coord)
    return min_choice

  def min_distance_translation(self, choices, ship, target_coords):
    if choices != []:
      min_choice = choices[0]
      min_distance = self.calc_distance((ship.coords[0] + min_choice[0], ship.coords[1] + min_choice[1]), target_coords)
      for choice in choices:
        current_coords = (ship.coords[0] + choice[0], ship.coords[1] + choice[1])
        current_distance = self.calc_distance(current_coords, target_coords)

        if current_distance < min_distance:
          min_distance = current_distance
          min_choice = choice

      return min_choice

  def choose_translation(self, board, choices, ship):
    target_coords = self.find_min_choice(self.find_home_colonies(board), ship.coords)
    return self.min_distance_translation(choices, ship, target_coords)
    
  def choose_target(self, opponent_ships):
    random_idx = math.floor(len(opponent_ships) * random())
    return opponent_ships[random_idx]