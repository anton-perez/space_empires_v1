class Ship:
  def update_coords(self, new_coords):
    self.coords = new_coords
  
  def set_player_number(self, player_num):
    self.player_num = player_num

  def set_ship_number(self, ship_num):
    self.ship_num = ship_num
  

class Scout(Ship):
  def __init__(self, initial_coords):
    self.player_num = None #player_num
    self.ship_num = None #ship_num
    self.name = 'Scout'
    self.hp = 1
    self.atk = 3
    self.df = 0
    self.ship_class = 'E' #ship_class
    self.obj_type = 'Ship'
    self.coords = initial_coords

class BattleCruiser(Ship):
  def __init__(self, initial_coords):
    self.player_num = None
    self.ship_num = None
    self.name = 'BattleCruiser'
    self.hp = 2
    self.atk = 5
    self.df = 1
    self.ship_class = 'B'
    self.obj_type = 'Ship'
    self.coords = initial_coords
    