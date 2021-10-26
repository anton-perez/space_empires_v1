class Colony:
  def __init__(self, coords):
    self.player_num = None
    self.coords = coords
    self.obj_type = "Colony"
    self.is_home_colony = False

  def set_player_number(self, player_num):
    self.player_num = player_num
