import random
import sys
sys.path.append('')
from ships import *
from colony import *
from ship_data import *
sys.path.append('logs')
from logger import *
# random.seed(3)

class Game:
  def __init__(self, players, board_size=[7,7]):
    self.logs = Logger('/home/runner/spaceempiresv1/logs/game-logs.txt')
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
      init_coords = (mid_x, (player.player_num-1)*(board_y-1))
      
      home_colony = Colony(init_coords) # add home colony
      home_colony.is_home_colony = True
      player.set_home_colony(home_colony)
      player.cp = 150

      # for _ in range(3):# add scouts
      #   player.add_ship(Scout(init_coords))
      # for _ in range(3):# add battlecruisers
      #   player.add_ship(BattleCruiser(init_coords))

      player_ships = player.buy_ships(player.cp)
      total_cost = self.calc_total_cost(player_ships)
      if total_cost > player.cp:
        self.logs.write('\n\tPlayer {} went over budget'.format(player.player_num))
        continue
      player.cp -= total_cost
      for name in player_ships:
        for i in range(player_ships[name]):
          ship = ship_objects[name](init_coords)
          if ship == None:
            continue
          player.add_ship(ship)

  def calc_total_cost(self, ship_dict):
    total = 0

    if ship_dict != None:
      for name in ship_dict:
        for ship_info in all_ships:
          if ship_info['name'] == name:
            total += ship_dict[name] * ship_info['cp_cost']
    return total

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
    self.update_simple_boards()
    

  def update_simple_boards(self):
    simple_board = {}
    for y in range(board_y):
      for x in range(board_x):
        simple_board[(x,y)] = [self.get_info_from_obj(obj) for obj in self.board[y][x]]
  
    for player in self.players:
      #player.strategy.update_simple_board(simple_board) 
      player.strategy.simple_board = simple_board 
      player.strategy.turn = self.turn


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

  def get_player_ships_on_space(coords, player_num):
    x, y = coords
    return [ship for ship in self.get_all_ships_on_space(coords) if ship.player_num == player_num]

  def check_for_opponent_ships(self, obj):
    for ship in self.get_all_ships_on_space(obj.coords):
      if obj.player_num != ship.player_num:
        return True
    return False
  
  def get_opponent_ships(self, ship, combat_order):
    return [obj for obj in combat_order if obj.player_num != ship.player_num and obj.hp > 0]

  def all_same_team(self, ship_list):
    return len(set([ship.player_num for ship in ship_list])) == 1

  def get_info_from_obj(self, obj):
    return obj.__dict__

  def get_obj_from_info(self, obj_info):
    x, y = obj_info['coords']
    for obj in self.board[y][x]:
      if self.get_info_from_obj(obj) == obj_info:
        return obj
    

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
    if roll <= threshold or roll == 1:
      return True
    return False

  def maintenance(self, player):
    self.logs.write('\n\tMaintenance for Player {}:\n'.format(player.player_num))
    #initial cp
    total_maint_cost = 0
    for i, ship in enumerate(player.ships):
      if total_maint_cost + ship.maint_cost <= player.cp:
        total_maint_cost += ship.maint_cost
        self.logs.write('\t\tMaintenance done for Player {} {} {}\n'.format(ship.player_num, ship.name, ship.ship_num))
      else:
        self.logs.write('\n\tPlayer {} has insufficient funds for further ship maintenance. Removing the remaining ships:\n'.format(player.player_num))
        for rmvd_ship in player.ships[i:]:
          self.logs.write('\t\tPlayer {} {} {}\n'.format(rmvd_ship.player_num, rmvd_ship.name, rmvd_ship.ship_num))
          self.remove_from_board(rmvd_ship)
        player.ships = player.ships[:i]
        break
    
    player.cp -= total_maint_cost
    #final cp

  def complete_movement_phase(self):
    self.logs.write('\nBEGINNING OF TURN {} MOVEMENT PHASE\n\n'.format(self.turn))

    for player in self.players:
      for ship in player.ships:
        opponent_ships_on_space = self.check_for_opponent_ships(ship)
        if opponent_ships_on_space:
          continue
        current_coords = ship.coords
        potential_translations = self.get_in_bounds_translations(current_coords) 
        ship_info = self.get_info_from_obj(ship)
        translation = player.choose_translation(ship_info, potential_translations)

        if translation not in potential_translations:
          self.logs.write('\tPlayer {} {} {} tried to make an invalid move: {}\n'.format(ship.player_num, ship.name, ship.ship_num, translation))
          translation = (0,0)

        self.move_ship(ship, translation)
        moved_to_opponent_space = self.check_for_opponent_ships(ship)
        if moved_to_opponent_space and ship.coords not in self.combat_coords:
          self.combat_coords.append(ship.coords)

        self.update_simple_boards()
        self.logs.write('\tPlayer {} {} {}: {} -> {}\n'.format(ship.player_num, ship.name, ship.ship_num, current_coords, ship.coords))
    
    # self.print_board()
    self.logs.write('\nEND OF TURN {} MOVEMENT PHASE\n'.format(self.turn))

  def complete_combat_phase(self): # prioritization: class, tactics, first in square
    self.logs.write('\nBEGINNING OF TURN {} COMBAT PHASE\n'.format(self.turn))
    if self.winner != None:
      return
    to_delete_coords = []
    
    for coords in self.combat_coords:
      self.logs.write('\n\t Combat at: {}\n'.format(coords))
      combat_order = sorted(self.get_all_ships_on_space(coords), key=lambda x: x.ship_class) #by class
      while not self.all_same_team(combat_order):
        for ship in combat_order:
          if ship.hp <= 0:
            continue

          player = self.players[ship.player_num - 1]
          opponent_ships = self.get_opponent_ships(ship, combat_order) 
          if len(opponent_ships) == 0:
            continue
          ship_info = self.get_info_from_obj(ship)
          combat_order_info = [self.get_info_from_obj(ship) for ship in combat_order if ship.hp > 0] 
          target_info = player.choose_target(ship_info, combat_order_info) # choose_target
          target = self.get_obj_from_info(target_info)
          target_player = self.players[target.player_num - 1]

          self.logs.write('\n\t\tAttacker: Player {} {} {}\n'.format(ship.player_num, ship.name, ship.ship_num))
          self.logs.write('\t\tDefender: Player {} {} {}\n'.format(target.player_num, target.name, target.ship_num))
          
          if self.hit(ship, target):
            self.logs.write('\t\tHit!\n')
            dmg = 1
            target.hp -= dmg
            self.logs.write('\n\t\tPlayer {} {} {} dealt {} dmg to Player {} {} {}\n'.format(ship.player_num, ship.name, ship.ship_num, dmg, target.player_num, target.name, target.ship_num))
            if target.hp <= 0:
              self.remove_from_board(target)
              target_player.remove_ship(target)
              self.logs.write('\t\tPlayer {} {} {} was destroyed\n'.format(target.player_num, target.name, target.ship_num))
              self.update_simple_boards()
              
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

  def complete_economic_phase(self):
    self.logs.write('\nBEGINNING OF TURN {} ECONOMIC PHASE\n'.format(self.turn))
    for player in self.players:
      player.cp += 10
      
      self.maintenance(player)

      player_ships = player.buy_ships(player.cp)
      total_cost = self.calc_total_cost(player_ships)
      if total_cost > player.cp:
        self.logs.write('\n\tPlayer {} went over budget'.format(player.player_num))
        continue
      player.cp -= total_cost
      if player_ships != None:
        self.logs.write('\n\tPlayer {} buys the following ships:'.format(player.player_num))
        for name in player_ships:
          for i in range(player_ships[name]):
            init_coords = player.home_colony.coords
            ship = ship_objects[name](init_coords)
            if ship == None:
              continue
            player.add_ship(ship)
            self.add_to_board(ship)
            self.logs.write('\n\t\t Player {} {} {}'.format(ship.player_num, ship.name, ship.ship_num))
          self.logs.write('\n')


    self.logs.write('\nEND OF TURN {} ECONOMIC PHASE\n'.format(self.turn))

  def remove_player(self, player):
    for ship in player.ships:
      self.remove_from_board(ship)
    for colony in player.colonies:
      self.remove_from_board(colony)
    self.remove_from_board(player.home_colony)
    self.players.remove(player)
    
  def check_for_winner(self):
    for player in self.players:
      if self.check_for_opponent_ships(player.home_colony):
        self.logs.write('\nPLAYER {} HAS BEEN REMOVED FROM THE GAME\n'.format(player.player_num))
        self.remove_player(player)
    if len(self.players) == 1:
      self.logs.write('\nPLAYER {} HAS WON'.format(self.players[0].player_num))
      return self.players[0].player_num
    if len(self.players) == 0:
      self.logs.write('TIE GAME')
      return "Tie"

  def run_to_completion(self):
    while self.winner == None:
      self.complete_movement_phase()
      self.complete_combat_phase()
      self.complete_economic_phase()
      self.turn += 1
      self.winner = self.check_for_winner()

  def run_until(self, n):
    while self.turn <= n and self.winner == None:
      self.complete_movement_phase()
      self.complete_combat_phase()
      self.complete_economic_phase()
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
        elif self.board[y][x][0].player_num == 1:
          row_string += '[v]'
        elif self.board[y][x][0].player_num == 2:
          row_string += '[^]'
      print(row_string)
    print('\n')




