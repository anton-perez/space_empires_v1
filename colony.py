class Colony:
  def __init__(self, coords):
    self.player_number = None
    self.coords = coords
    self.is_home_colony = False

  def set_player_number(self, player_number):
    self.player_number = player_number
