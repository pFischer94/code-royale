from owner.Owner import Owner
from units.Unit import Unit
from units.UnitType import UnitType

class UnitsAccessBuilder:
    def __init__(self, units: list[Unit]):
        self.units: list[Unit] = units
    
    @property
    def my_queen(self) -> Unit:
        return [unit for unit in self.units if unit.type == UnitType.QUEEN and unit.owner == Owner.FRIEND][0]
    
    @property
    def enemy(self):
        self.units = [unit for unit in self.units if unit.owner == Owner.ENEMY]
        return self
    
    @property
    def knights(self):
        self.units = [unit for unit in self.units if unit.type == UnitType.KNIGHT]
        return self
    
    def min_dist_to(self, pos: list[int]) -> int:
        if not self.units:
            return 0
        return min([unit.dist_to(pos) for unit in self.units])
    
    def get(self) -> list[Unit]:
        return self.units
    
    def get_closest_to(self, pos: list[int]) -> Unit:
        closest = sorted(self.units, key=lambda unit: unit.dist_to(pos))
        if closest:
            return closest[0]
        else:
            return None
    
    def __repr__(self) -> str:
        return f"UnitsAccessBuilder [units = {self.units}]"
    