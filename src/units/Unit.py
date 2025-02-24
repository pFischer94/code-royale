from owner.Owner import Owner
from units.UnitType import UnitType

class Unit:
    def __init__(self, pos: list[int], type: UnitType, owner: Owner, health: int):
        self.pos = pos
        self.type = type
        self.owner = owner
        self.health = health
    
    def __repr__(self):
        return str(self)
