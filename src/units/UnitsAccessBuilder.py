from units.Unit import Unit

class UnitsAccessBuilder:
    def __init__(self, units: list[Unit]):
        self.units: list[Unit] = units
    
    # @property
    # def friendly(self) -> list[Unit]:
    #     return [unit for unit in self.units if unit.owner == Owner.FRIENDLY]
    
    # @property
    # def enemy(self) -> list[Unit]:
    #     return [unit for unit in self.units if unit.owner == Owner.ENEMY]
    
    # def get(self) -> list[Unit]:
    #     return self.units
    
    def __repr__(self) -> str:
        return f"UnitsAccessBuilder [units = {self.units}]"
    