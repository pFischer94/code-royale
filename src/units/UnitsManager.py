from owner.Owner import Owner
from units.UnitsAccessBuilder import UnitsAccessBuilder
from units.Unit import Unit
from units.UnitType import UnitType

class UnitsManager:
    def __init__(self, units: list[Unit]):
        self.__units: list[Unit] = units
    
    @classmethod
    def from_input(clf):
        units: list[Unit] = []
        num_units = int(input())
        for i in range(num_units):
            x, y, owner, type, health = [int(j) for j in input().split()]
            units.append(Unit([x, y], UnitType(type), Owner(owner), health))
        return cls(units)
    
    @property
    def units(self) -> UnitsAccessBuilder:
        return UnitsAccessBuilder(self.__units)
    
    def __repr__(self):
        return f"UnitsManager [units = {self.__units}]"
