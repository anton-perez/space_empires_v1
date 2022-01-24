class Ship:
  def update_coords(self, new_coords):
    self.coords = new_coords
  
  def set_player_number(self, player_num):
    self.player_num = player_num

  def set_ship_number(self, ship_num):
    self.ship_num = ship_num
  

class Scout(Ship):
  def __init__(self, initial_coords):
    self.name = 'Scout'
    self.player_num = None
    self.ship_num = None 
    self.hp = 1
    self.atk = 3
    self.df = 0
    self.ship_class = 'E'
    self.cp_cost = 6
    self.maint_cost = 1
    self.obj_type = 'Ship'
    self.coords = initial_coords

class BattleCruiser(Ship):
  def __init__(self, initial_coords):
    self.name = 'BattleCruiser'
    self.player_num = None
    self.ship_num = None
    self.hp = 2
    self.atk = 5
    self.df = 1
    self.ship_class = 'B'
    self.cp_cost = 15
    self.maint_cost = 2
    self.obj_type = 'Ship'
    self.coords = initial_coords
    
class BattleShip(Ship): 
  def __init__(self, initial_coords):
    self.name = 'BattleShip'
    self.player_num = None
    self.ship_num = None
    self.hp = 3
    self.atk = 5
    self.df = 2
    self.ship_class = 'A'
    self.cp_cost = 20
    self.maint_cost = 3
    self.obj_type = 'Ship'
    self.coords = initial_coords

class Cruiser(Ship): 
  def __init__(self, initial_coords):
    self.name = 'Cruiser'
    self.player_num = None
    self.ship_num = None
    self.hp = 2
    self.atk = 4
    self.df = 1
    self.ship_class = 'C'
    self.cp_cost = 12
    self.maint_cost = 2
    self.obj_type = 'Ship'
    self.coords = initial_coords

class Destroyer(Ship):
  def __init__(self, initial_coords):
    self.name = 'Destroyer'
    self.player_num = None
    self.ship_num = None
    self.hp = 1
    self.atk = 4
    self.df = 0
    self.ship_class = 'D'
    self.cp_cost = 9
    self.maint_cost = 1
    self.obj_type = 'Ship'
    self.coords = initial_coords

class Dreadnaught(Ship):
  def __init__(self, initial_coords):
    self.name = "Dreadnaught"
    self.player_num = None
    self.ship_num = None
    self.hp = 3
    self.atk = 6
    self.df = 3
    self.ship_class = 'A'
    self.cp_cost = 24
    self.maint_cost = 3
    self.obj_type = 'Ship'
    self.coords = initial_coords