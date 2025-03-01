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
    
    # 3 mines, dont upgrade
    # 4 towers in middle, dont upgrade
    def build(self):
        next_barracks = self.SM.sites.planned(SiteType.BARRACKS).get_closest_to(self.um.units.my_queen.pos)
        next_tower = self.SM.sites.planned(SiteType.TOWER).get_closest_to(self.um.units.my_queen.pos)
        next_mine = self.SM.sites.planned(SiteType.MINE).get_closest_to(self.um.units.my_queen.pos)
        
        if not self.SM.sites.my.mines.len() and next_mine:
            print(f"BUILD {next_mine.id} MINE")
        elif upgrade := self.SM.sites.my.mines.needs_upgrade.get_closest_to(self.um.units.my_queen.pos):
            print(f"BUILD {upgrade.id} MINE")
        # elif not self.SM.sites.my.produces(UnitType.ARCHER).len() and next_barracks:
        #     print(f"BUILD {next_barracks.id} BARRACKS-ARCHER")
        elif not self.SM.sites.my.barracks.len() and next_barracks:
            print(f"BUILD {next_barracks.id} BARRACKS-KNIGHT")
        elif upgrade := self.SM.sites.my.towers.wnofu.get_closest_to(self.um.units.my_queen.pos):
            print(f"BUILD {upgrade.id} TOWER")
        elif next_tower:
            print(f"BUILD {next_tower.id} TOWER")
        elif next_mine:
            print(f"BUILD {next_mine.id} MINE")
        else:
            print("WAIT")
            
    def train(self):
        if not self.units_trained and (barracks := self.SM.sites.my.barracks.idle.get_closest_to(Params.CENTER)):
            self.units_trained = True
            print(f"TRAIN {barracks.id}")
        elif self.gold >= Params.SAVING_LIMIT:
            self.train_big_wave()
        else:
            print("TRAIN")
    
    def train_big_wave(self):
        barracks = self.SM.sites.my.barracks.get()
        barracks.sort(key=lambda barracks: barracks.dist_to(Params.CENTER))
        ids = []
        for barrack in barracks:
            if barrack.busy_turns == 0 and self.gold >= barrack.produces_unit.cost:
                self.gold -= barrack.produces_unit.cost
                ids.append(barrack.id)
        id_str = " " + ', '.join(str(ids))
        print(f"TRAIN{id_str}")
    
    def __repr__(self) -> str:
        return (f"GameManager []")
    