import sys

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
        self.SM.plan_sites()
        
        self.gold = 0
        self.touched_site = -1
        self.units_trained = False

        self.build()
        self.train()
    
    def update(self) -> None:
        self.gold, self.touched_site = [int(i) for i in input().split()]
        self.SM.update_from_input()
        self.um = UnitsManager.from_input()
    
    def build(self):
        raise NotImplementedError("Please Implement this method")
            
    def train(self):
        raise NotImplementedError("Please Implement this method")
    
    def train_big_wave(self):
        barracks = self.SM.sites.my.barracks.get()
        barracks.sort(key=lambda barracks: barracks.dist_to(Params.CENTER))
        ids = []
        for barrack in barracks:
            if barrack.busy_turns <= 0 and self.gold >= barrack.produces_unit.cost:
                self.gold -= barrack.produces_unit.cost
                ids.append(str(barrack.id))
        if ids:
            id_str = ""
            for id in ids:
                id_str += " " + id
            print(f"argh ids: {ids}", file=sys.stderr, flush=True)
            print(f"TRAIN{id_str}")
        else:
            print("TRAIN")
    
    def __repr__(self) -> str:
        return (f"GameManager []")
    