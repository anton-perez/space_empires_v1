import math
import random

class CaydenStrategy():
  def __init__(self):
    self.simple_board = None

  def best_option(self, options, coordinate):
    best_option = options[0]
    min_distance = math.dist(best_option, coordinate)

    for option in options:
      if math.dist(option, coordinate) < min_distance:
        best_option = option
        min_distance = self.distance(option, coordinate)

    return best_option

  def best_translation(self, options, coordinate, desired_location):
    best_option = options[0]
    updated_coordinate = [best_option[n] + coordinate[n] for n in range(len(best_option))]
    distance = math.dist(updated_coordinate, desired_location)

    for option in options:
      new_coordinate = [option[n] + coordinate[n] for n in range(len(option))]

      if math.dist(new_coordinate, desired_location) < distance:
        best_option = option
        updated_coordinate = new_coordinate
        distance = math.dist(new_coordinate, desired_location)

    return best_option

  def choose_translation(self, ship_info, possible_translations):
    opponent_home_colony = []

    for key in self.simple_board:
      for obj in self.simple_board[key]:
        if obj['obj_type'] == 'Colony' and obj['player_num'] != ship_info['player_num'] and obj['is_home_colony'] == True:
          opponent_home_colony.append(key)

    closest_colony = self.best_option(opponent_home_colony, ship_info['coords'])
    return self.best_translation(possible_translations, ship_info['coords'], closest_colony)

  def get_enemies(self, own_ship, combat_order):
    player_num = own_ship['player_num']
    enemies = []
    for ship_info in combat_order:
      if ship_info['player_num'] != player_num and ship_info['hp'] > 0:
        enemies.append(ship_info)
    return enemies
  
  def choose_target(self, ship_info, combat_order):
    enemies_info = self.get_enemies(ship_info, combat_order)
    target_info = enemies_info[random.randint(0, len(enemies_info)-1)]
    return target_info