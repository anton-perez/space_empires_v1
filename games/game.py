import random
import sys
sys.path.append('')
from ships import *
from colony import *
sys.path.append('logs')
from logger import *

class Game:
  def __init__(self, players, board_size=[7,7]):
    self.logs = Logger('/home/runner/tempspaceempires/logs/game-logs.txt')
    self.players = players
    self.board_size = board_size
    
    global board_x, board_y 
    board_x, board_y = board_size
    self.board = [[[] for _ in range(board_x)] for _ in range(board_y)]
    self.turn = 1
    self.winner = None
    self.combat_coords = []

    self.initialize_game()

  def set_player_numbers(self):
    for i, player in enumerate(self.players):
      player.set_player_number(i+1)

  def initialize_players(self):
    self.set_player_numbers()

    mid_x = board_x // 2
    for player in self.players:
      init_coords = (mid_x, (player.player_number-1)*(board_y-1))
      
      home_colony = Colony(init_coords) # add home colony
      home_colony.is_home_colony = True
      player.set_home_colony(home_colony)

      for _ in range(3):# add scouts
        player.add_ship(Scout(init_coords))
      for _ in range(3):# add battlecruisers
        player.add_ship(Battlecruiser(init_coords))

  def initialize_board(self):
    for player in self.players:
      x, y = player.home_colony.coords
      self.board[y][x].append(player.home_colony)
      for colony in player.colonies:
        x, y = colony.coords
        self.board[y][x].append(colony)
      for ship in player.ships:
        x, y = ship.coords
        self.board[y][x].append(ship)

  def initialize_game(self):
    self.logs.clear_log()
    self.initialize_players()
    self.initialize_board()

  def check_if_coords_are_in_bounds(self, coords):
    if coords == None:
      return False
    x, y = coords
    if 0 <= x and x < board_x:
      if 0 <= y and y < board_y:
        return True
    return False
  
  def check_if_translation_is_in_bounds(self, coords, translation):
    if coords == None:
      return False
    x, y = coords
    dx, dy = translation
    new_coords = (x+dx,y+dy)
    return self.check_if_coords_are_in_bounds(new_coords)

  def get_in_bounds_translations(self, coords):
    translations = [(0,0), (0,1), (0,-1), (1,0), (-1,0)]
    in_bounds_translations = []
    for translation in translations:
      if self.check_if_translation_is_in_bounds(coords, translation):
        in_bounds_translations.append(translation)
    return in_bounds_translations

  def add_to_board(self, obj):
    x, y = obj.coords
    self.board[y][x].append(obj)

  def remove_from_board(self, obj):
    x, y = obj.coords
    self.board[y][x].remove(obj)

  def get_all_objects_on_space(self, coords):
    x, y = coords
    return self.board[y][x]
    
  def get_all_ships_on_space(self, coords):
    return [obj for obj in self.get_all_objects_on_space(coords) if isinstance(obj, Ship)]

  def get_player_ships_on_space(coords, player_number):
    x, y = coords
    return [ship for ship in self.get_all_ships_on_space(coords) if ship.player_number == player_number]

  def check_for_opponent_ships(self, input_ship):
    for ship in self.get_all_ships_on_space(input_ship.coords):
      if input_ship.player_number != ship.player_number:
        return False
    return True
  
  def get_opponent_ships(self, ship, combat_order):
    return [obj for obj in combat_order if obj.player_number != ship.player_number and obj.hp > 0]

  def all_same_team(self, ship_list):
    return len(set([ship.player_number for ship in ship_list])) == 1

  def move_ship(self, ship, translation):
    x,y = ship.coords
    new_coords = (x+translation[0], y+translation[1])
    self.remove_from_board(ship)
    ship.update_coords(new_coords)
    self.add_to_board(ship)

  def roll(self):
    return random.randint(1,10)
    
  def hit(self, attacker, defender):
    roll = self.roll()
    threshold = attacker.atk - defender.df
    if roll <= threshold:
      return True
    return False

  def complete_movement_phase(self):
    self.logs.write('\nBEGINNING OF TURN {} MOVEMENT PHASE\n\n'.format(self.turn))

    for player in self.players:
      for ship in player.ships:
        opponent_ships_on_space = not self.check_for_opponent_ships(ship)
        if opponent_ships_on_space:
          continue
        current_coords = ship.coords
        potential_translations = self.get_in_bounds_translations(current_coords) 
        translation = player.choose_translation(self.board, potential_translations, ship)
        self.move_ship(ship, translation)
        moved_to_opponent_space = not self.check_for_opponent_ships(ship)
        if moved_to_opponent_space and ship.coords not in self.combat_coords:
          self.combat_coords.append(ship.coords)

        self.logs.write('\tPlayer {} {} {}: {} -> {}\n'.format(ship.player_number, ship.name, ship.ship_number, current_coords, ship.coords))
    
    self.print_board()
    self.logs.write('\nEND OF TURN {} MOVEMENT PHASE\n'.format(self.turn))

  
  def complete_combat_phase(self): # prioritization: class, tactics, first in square
    self.logs.write('\nBEGINNING OF TURN {} COMBAT PHASE\n'.format(self.turn))
    if self.winner != None:
      return
    to_delete_coords = []
    print(self.combat_coords)
    
    for coords in self.combat_coords:
      self.logs.write('\n\t Combat at: {}\n'.format(coords))
      combat_order = sorted(self.get_all_ships_on_space(coords), key=lambda x: x.cls) #by class
      for ship in combat_order:
        if ship.hp <= 0:
          continue

        player = self.players[ship.player_number - 1]
        opponent_ships = self.get_opponent_ships(ship, combat_order) 
        if len(opponent_ships) == 0:
          continue
        target = player.choose_target(opponent_ships) # choose_target
        target_player = self.players[target.player_number - 1]

        self.logs.write('\n\t\tAttacker: Player {} {} {}\n'.format(ship.player_number, ship.name, ship.ship_number))
        self.logs.write('\t\tDefender: Player {} {} {}\n'.format(target.player_number, target.name, target.ship_number))
        
        if self.hit(ship, target):
          self.logs.write('\t\tHit!\n')
          dmg = 1
          target.hp -= dmg
          self.logs.write('\n\t\tPlayer {} {} {} dealt {} dmg to Player {} {} {}\n'.format(ship.player_number, ship.name, ship.ship_number, dmg, target.player_number, target.name, target.ship_number))
          if target.hp <= 0:
            self.remove_from_board(target)
            target_player.remove_ship(target)
            self.logs.write('\t\tPlayer {} {} {} was destroyed\n'.format(target.player_number, target.name, target.ship_number))
            
        else:
          self.logs.write('\t\t(Miss)\n')


      for ship in combat_order:
        if ship.hp <= 0:
          combat_order.remove(ship)
      if self.all_same_team(combat_order):
        to_delete_coords.append(coords)
    for coords in to_delete_coords:
      self.combat_coords.remove(coords)

    self.logs.write('\nEND OF TURN {} COMBAT PHASE\n'.format(self.turn))

  def check_for_winner(self):
    p1_ships = self.players[0].ships
    p1_home_colony_coords = self.players[0].home_colony.coords
    p2_ships = self.players[1].ships
    p2_home_colony_coords = self.players[1].home_colony.coords

    if any(p1_ships[i].coords == p2_home_colony_coords for i in range(len(p1_ships))) and any(p2_ships[i].coords == p1_home_colony_coords for i in range(len(p2_ships))):
      self.logs.write('\nTIE GAME')
      return 'Tie' 
    elif any(p1_ships[i].coords == p2_home_colony_coords for i in range(len(p1_ships))):
      self.logs.write('\nWINNER: PLAYER 1')
      return 1
    elif any(p2_ships[i].coords == p1_home_colony_coords for i in range(len(p2_ships))):
      self.logs.write('\nWINNER: PLAYER 2')
      return 2
    else:
      return None

  def run_to_completion(self):
    while self.winner == None:
      self.complete_movement_phase()
      self.complete_combat_phase()
      self.turn += 1
      self.winner = self.check_for_winner()

  def print_board(self):
    combat_locations = self.combat_coords
    print('\n')
    for y in range(board_y):
      row_string = ''
      for x in range(board_x):
        if self.board[y][x] == []:
          row_string += '[ ]'
        elif (x,y) in combat_locations:
          row_string += '[*]'
        elif self.board[y][x][0].player_number == 1:
          row_string += '[v]'
        elif self.board[y][x][0].player_number == 2:
          row_string += '[^]'
      print(row_string)
    print('\n')




