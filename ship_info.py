from ships import *

scout = {'name':"Scout",'hp':1,'atk':3,'df':0,'ship_class':"E",'cp_cost':6}
battlecruiser = {'name':"BattleCruiser",'hp':2,'atk':5,'df':1,'ship_class':"B",'cp_cost':15}
battleship = {'name':"BattleShip",'hp':3,'atk':5,'df':2,'ship_class':"A",'cp_cost':20}
cruiser = {'name':"Cruiser",'hp':2,'atk':4,'df':1,'ship_class':"C",'cp_cost':12}
destroyer = {'name':"Destroyer",'hp':1,'atk':4,'df':0,'ship_class':"D",'cp_cost':9}
dreadnaught = {'name':"Dreadnaught",'hp':3,'atk':6,'df':3,'ship_class':"A",'cp_cost':24}
all_ship_infos = [scout, battlecruiser, battleship, cruiser, destroyer, dreadnaught]
ship_objects = {'Scout':Scout, 'BattleCruiser': BattleCruiser, 'BattleShip': BattleShip, 'Cruiser': Cruiser, 'Destroyer': Destroyer, 'Dreadnaught':Dreadnaught}