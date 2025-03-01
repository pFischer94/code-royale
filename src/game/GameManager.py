import math

from params import Params
from sites.SitesManager import SitesManager
from sites.SiteType import SiteType
from units.UnitType import UnitType
from units.UnitsManager import UnitsManager

class GameManager:
    def __init__(self) -> None:
        self.SM = SitesManager.from_input()
        input()
        self.SM.update_from_input()
        self.um = UnitsManager.from_input()
        self.SM.save_start_side(self.um.units.my_queen.pos)
        
        self.gold = 0
        self.touched_site = -1
        self.units_trained = 0

        self.build()
        self.train()
    
    def update(self) -> None:
        self.gold, self.touched_site = [int(i) for i in input().split()]
        self.SM.update_from_input()
        self.um = UnitsManager.from_input()
    
    def build(self):
        if next_barracks := self.SM.sites.planned(SiteType.BARRACKS).get_closest_to(self.um.units.my_queen.pos):
            print(f"BUILD {next_barracks.id} BARRACKS-KNIGHT")
        else:
            print("WAIT")
            
    def train(self):
        if self.units_trained == 0 and (barracks := self.SM.sites.my.barracks.idle.get_closest_to(Params.CENTER)):
                print(f"TRAIN {barracks.id}")
        elif self.gold >= Params.SAVING_LIMIT:
            barracks = self.SM.sites.my.barracks.get()
            barracks.sort(key=lambda barracks: barracks.dist_to(Params.CENTER))
            ids = []
            for barrack in barracks:
                if barrack.busy_turns == 0 and self.gold >= UnitType.KNIGHT.cost:
                    ids.append(barrack.id)
                    self.gold -= UnitType.KNIGHT.cost
            # TODO: fix error "TRAIN "
            print(f"TRAIN {', '.join(ids)}")
        else:
            print("TRAIN")
    
    def __repr__(self) -> str:
        return (f"GameManager []")
    