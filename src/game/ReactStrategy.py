import sys

from params import Params
from sites.SitesManager import SitesManager
from sites.SiteType import SiteType
from game.GameManager import GameManager
from units.UnitType import UnitType
from units.UnitsManager import UnitsManager

class ReactStrategy(GameManager):
    def build(self):
        enemy_towers = self.SM.sites.enemy.towers.get()
        # TODO: close_on_my_side
        site_close = self.SM.sites.buildable.safe(enemy_towers).get_closest_to(self.um.units.my_queen.pos)
        site_center = self.SM.sites.buildable.safe(enemy_towers).get_closest_to(Params.CENTER)
        
        # TODO: not when enemies are close
        if upgrade := self.SM.sites.my.mines.needs_upgrade.get_closest_to(self.um.units.my_queen.pos):
            print(f"BUILD {upgrade.id} MINE")
        elif self.SM.sites.my.mines.len() < Params.TARGET_MINES and site_close:
            print(f"BUILD {site_close.id} MINE")
        elif upgrade := self.SM.sites.my.towers.wnfu.get_closest_to(self.um.units.my_queen.pos):
            print(f"BUILD {upgrade.id} TOWER")
        elif self.SM.sites.my.towers.len() < Params.TARGET_TOWERS and site_center:
            print(f"BUILD {site_center.id} TOWER")
        elif self.SM.sites.my.barracks.produces(UnitType.KNIGHT).len() < Params.TARGET_KNIGHTS_BARRACKS and site_close:
            print(f"BUILD {site_close.id} BARRACKS-KNIGHT")
        elif self.SM.sites.my.barracks.produces(UnitType.GIANT).len() < Params.TARGET_GIANTS_BARRACKS and site_close:
            print(f"BUILD {site_close.id} BARRACKS-GIANT")
        
        
        
        # if not self.SM.sites.my.mines.len() and next_mine:
        #     print(f"BUILD {next_mine.id} MINE")
        # elif upgrade := self.SM.sites.my.mines.needs_upgrade.get_closest_to(self.um.units.my_queen.pos):
        #     print(f"BUILD {upgrade.id} MINE")
        # # elif not self.SM.sites.my.produces(UnitType.ARCHER).len() and next_barracks:
        # #     print(f"BUILD {next_barracks.id} BARRACKS-ARCHER")
        # elif not self.SM.sites.my.barracks.len() and next_barracks:
        #     print(f"BUILD {next_barracks.id} BARRACKS-KNIGHT")
        # elif upgrade := self.SM.sites.my.towers.wnofu.get_closest_to(self.um.units.my_queen.pos):
        #     print(f"BUILD {upgrade.id} TOWER")
        # elif next_tower:
        #     print(f"BUILD {next_tower.id} TOWER")
        # elif next_mine:
        #     print(f"BUILD {next_mine.id} MINE")
        # elif next_barracks:
        #     print(f"BUILD {next_barracks.id} BARRACKS-GIANT")
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
    