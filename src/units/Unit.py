import math

from owner.Owner import Owner
from units.UnitType import UnitType

class Unit:
    def __init__(self, pos: list[int], type: UnitType, owner: Owner, health: int):
        self.pos = pos
        self.type = type
        self.owner = owner
        self.health = health
    
    def dist_to(self, pos: list[int]) -> float:
        return math.dist(self.pos, pos)
    
    def __repr__(self):
        return (f"Unit [pos = {self.pos}, type = {self.type}, owner = {self.owner}, health = {self.health}]")
