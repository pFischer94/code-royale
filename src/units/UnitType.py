import enum

class UnitType(enum.Enum):
    NONE = (-2, 0, 0)
    QUEEN = (-1, 0, 1)
    KNIGHT = (0, 80, 4)
    ARCHER = (1, 100, 2)
    GIANT = (2, 140, 1)
    
    def __init__(self, type_number, cost, amount):
        self.type_number = type_number
        self.cost = cost
        self.amount = amount
        
    @classmethod
    def from_type_number(cls, type_number) -> "UnitType":
        for unit_type in cls:
            if unit_type.type_number == type_number:
                return unit_type
        raise ValueError(f"UnitType with type_number {type_number} not found.")
