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
    
    # @property
    # def friendly(self) -> list[Unit]:
    #     return [unit for unit in self.units if unit.owner == Owner.FRIENDLY]
    
    # @property
    # def enemy(self) -> list[Unit]:
    #     return [unit for unit in self.units if unit.owner == Owner.ENEMY]
    
    def get(self) -> list[Unit]:
        return self.units
    
    def __repr__(self) -> str:
        return f"UnitsAccessBuilder [units = {self.units}]"
    