import sys

from params import Params
from game.GameManager import GameManager
from units.UnitType import UnitType
from sites.Side import Side

class OldStrategy(GameManager):
    def build(self):
        # TODO: barracks later, driven by gold
        # TODO: late game: more mines, giants, save gold for huge wave?
        
        enemy_units = self.units.enemy.get()
        enemy_towers = self.sites.enemy.towers.get()
        # TODO: test buildable instead of empty everywhere
        # TODO: ignore enemy towers?
        upgradeable_mines = sorted(self.sites.my.mines.needs_upgrade.safe(enemy_towers + enemy_units).get(), 
                                   key=lambda site: site.dist_to(self.units.my_queen.pos))
        # TODO: safe from enemy towers?
        upgradeable_towers = sorted(self.sites.my.towers.wnfu.get(), 
                                    key=lambda site: site.dist_to(self.units.my_queen.pos))
        closest_empty_site = self.sites.empty.safe(enemy_towers).get_closest_to(self.units.my_queen.pos)
        closest_empty_site_for_mine = self.sites.empty.enough_gold.safe(enemy_towers + enemy_units).get_closest_to(self.units.my_queen.pos)
        
        # tower_sites = sorted(sorted(self.sites.my_side.empty.get(), key=lambda site: site.dist_to(Params.CENTER))[0:3], key=lambda site: site.dist_to(self.units.my_queen.pos))
        # mine_sites = self.sites.empty.enough_gold.furthest_back.get()
        # is_queen_safe = self.units.enemy.knights.min_dist_to(self.units.my_queen.pos) <= Params.ENEMY_KNIGHT_SAFETY_DIST
        
        print("closest_empty_site_for_mine:", closest_empty_site_for_mine, file=sys.stderr, flush=True)
        # print("is_queen_safe:", is_queen_safe, file=sys.stderr, flush=True)
        
        if self.units.my_queen.health < Params.MIN_QUEEN_HEALTH:
            hide_x = Params.WIDTH if self.SM.start_side == Side.RIGHT else 0
            print(f"MOVE {hide_x} {int(Params.HEIGHT / 2)}")
        
        # MINES
        elif upgradeable_mines:
            print(f"BUILD {upgradeable_mines[0].id} MINE")
        elif self.sites.my.mines.len() < Params.TARGET_MINES and closest_empty_site_for_mine:
            print(f"BUILD {closest_empty_site_for_mine.id} MINE")
            
        # BARRACKS KNIGHT
        elif self.sites.my.barracks.produces(UnitType.KNIGHT).len() < Params.TARGET_KNIGHTS_BARRACKS and closest_empty_site:
            print(f"BUILD {closest_empty_site.id} BARRACKS-KNIGHT")
        
        # TOWERS
        elif upgradeable_towers:
            print(f"BUILD {upgradeable_towers[0].id} TOWER")
        elif self.sites.my.towers.len() < Params.TARGET_TOWERS and closest_empty_site:
            print(f"BUILD {closest_empty_site.id} TOWER")
            
        # # BARRACKS GIANT
        # elif self.sites.my.barracks.produces(UnitType.GIANT).len() < Params.TARGET_GIANTS_BARRACKS and closest_empty_site:
        #     print(f"BUILD {closest_empty_site.id} BARRACKS-GIANT")
        
        # MINE OR TOWER
        elif closest_empty_site_for_mine: # and is_queen_safe:
            # TODO: furthest back?
            print(f"BUILD {closest_empty_site_for_mine.id} MINE")
        elif closest_empty_site:
            print(f"BUILD {closest_empty_site.id} TOWER")
        
        # HIDE
        else:
            # TODO: extract private method
            hide_x = Params.WIDTH if self.SM.start_side == Side.RIGHT else 0
            print(f"MOVE {hide_x} {int(Params.HEIGHT / 2)}")
            
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
    