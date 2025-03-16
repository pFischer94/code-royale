import sys

from params import Params
from sites.SitesManager import SitesManager
from sites.SiteType import SiteType
from game.GameManager import GameManager
from units.UnitType import UnitType
from units.UnitsManager import UnitsManager

class PlanStrategy(GameManager):
    def build(self):
        next_barracks = self.SM.sites.planned(SiteType.BARRACKS).get_closest_to(self.um.units.my_queen.pos)
        enemy_towers = self.SM.sites.enemy.towers.get()
        # TODO: build towers closer to center
        next_tower = self.SM.sites.planned(SiteType.TOWER).safe(enemy_towers).get_closest_to(self.um.units.my_queen.pos)
        enemy_units = self.um.units.enemy.get()
        # TODO: if not safe build tower instead
        next_mine = self.SM.sites.planned(SiteType.MINE).enough_gold.safe(enemy_units).get_closest_to(self.um.units.my_queen.pos)
        
        if not self.SM.sites.my.mines.len() and next_mine:
            print(f"BUILD {next_mine.id} MINE")
        elif upgrade := self.SM.sites.my.mines.needs_upgrade.get_closest_to(self.um.units.my_queen.pos):
            print(f"BUILD {upgrade.id} MINE")
        # elif not self.SM.sites.my.produces(UnitType.ARCHER).len() and next_barracks:
        #     print(f"BUILD {next_barracks.id} BARRACKS-ARCHER")
        elif not self.SM.sites.my.barracks.len() and next_barracks:
            print(f"BUILD {next_barracks.id} BARRACKS-KNIGHT")
        elif upgrade := self.SM.sites.my.towers.wnfu.get_closest_to(self.um.units.my_queen.pos):
            print(f"BUILD {upgrade.id} TOWER")
        elif next_tower:
            print(f"BUILD {next_tower.id} TOWER")
        elif next_mine:
            print(f"BUILD {next_mine.id} MINE")
        elif next_barracks:
            print(f"BUILD {next_barracks.id} BARRACKS-GIANT")
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
    