class Ship:
  def update_coords(self, new_coords):
    self.coords = new_coords
  
  def set_player_number(self, player_number):
    self.player_number = player_number

  def set_ship_number(self, ship_number):
    self.ship_number = ship_number

class Scout(Ship):
  def __init__(self, initial_coords):
    self.player_number = None
    self.ship_number = None
    self.name = 'Scout'
    self.hp = 1
    self.atk = 3
    self.df = 0
    self.cls = 'E'
    self.coords = initial_coords

class Battlecruiser(Ship):
  def __init__(self, initial_coords):
    self.player_number = None
    self.ship_number = None
    self.name = 'Battlecruiser'
    self.hp = 2
    self.atk = 5
    self.df = 1
    self.cls = 'B'
    self.coords = initial_coords
    