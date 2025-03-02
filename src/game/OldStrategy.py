import sys

from params import Params
from sites.SitesManager import SitesManager
from sites.SiteType import SiteType
from game.GameManager import GameManager
from units.UnitType import UnitType
from units.UnitsManager import UnitsManager

class OldStrategy(GameManager):
    def build(self):
        # TODO: test buildable instead of empty
        closest_empty_site = self.sites.empty.get_closest_to(self.units.my_queen.pos)
        upgradeable_mines = sorted(self.sites.my.mines.needs_upgrade.get(), key=lambda site: site.dist_to(self.units.my_queen.pos))
        upgradeable_towers = sorted(self.sites.my.towers.wnfu.get(), key=lambda site: site.dist_to(self.units.my_queen.pos))
        # TODO: remaining gold > MIN_GOLD_FOR_MINE
        mine_sites = self.sites.empty.furthest_back.get()
        tower_sites = sorted(sorted(self.sites.empty.get(), key=lambda site: site.dist_to(Params.CENTER))[0:3], key=lambda site: site.dist_to(self.units.my_queen.pos))
        
        if upgradeable_mines:
            print(f"BUILD {upgradeable_mines[0].id} MINE")
        elif self.sites.my.mines.len() < Params.TARGET_MINES and closest_empty_site:
            print(f"BUILD {closest_empty_site.id} MINE")
            
        elif self.sites.my.barracks.produces(UnitType.KNIGHT).len() < Params.TARGET_KNIGHTS_BARRACKS and closest_empty_site:
            print(f"BUILD {closest_empty_site.id} BARRACKS-KNIGHT")
        
        elif upgradeable_towers:
            print(f"BUILD {upgradeable_towers[0].id} TOWER")
        elif self.sites.my.towers.len() < Params.TARGET_TOWERS and tower_sites:
            print(f"BUILD {tower_sites[0].id} TOWER")
            
        elif self.sites.my.barracks.produces(UnitType.GIANT).len() < Params.TARGET_GIANTS_BARRACKS and closest_empty_site:
            print(f"BUILD {closest_empty_site.id} BARRACKS-GIANT")
        
        elif mine_sites:
            print(f"BUILD {mine_sites[0].id} MINE")
        
        else:
            print(f"WAIT")
            
    def train(self):
        barracks = sorted(self.sites.my.barracks.idle.get(), key=lambda site: site.produces_unit.value)
        
        ids = []
        for barrack in barracks:
            if (self.gold >= barrack.produces_unit.cost):
                ids.append(str(barrack.id))
                self.gold -= barrack.produces_unit.cost
        if ids:
            id_str = ""
            for id in ids:
                id_str += " " + id
            print(f"TRAIN{id_str}")
        else:
            print(f"TRAIN")
    