import sys
import math
from enum import Enum


#
 #####  #          #     #####   #####  #######  ##### 
#     # #         # #   #     # #     # #       #     #
#       #        #   #  #       #       #       #      
#       #       #     #  #####   #####  #####    ##### 
#       #       #######       #       # #             #
#     # #       #     # #     # #     # #       #     #
 #####  ####### #     #  #####   #####  #######  ##### 


class SiteType(Enum):
    EMPTY = -1
    GOLDMINE = 0
    TOWER = 1
    BARRACKS = 2
    
class Owner(Enum):
    NONE = -1
    FRIEND = 0
    ENEMY = 1
    
class UnitType(Enum):
    NONE = -2
    QUEEN = -1
    KNIGHT = 0
    ARCHER = 1
    GIANT = 2


class Site:
    def __init__(self, id: int, pos: list[int], radius: int):
        # init
        self.id = id
        self.pos = pos
        self.radius = radius
        
        # every
        self.gold: int = -1
        self.max_gold_rate = -1
        self.type: SiteType = SiteType.EMPTY
        self.owner: Owner = Owner.NONE
        
        # param_1
        self.gold_rate: int = 0
        self.hp: int = -1
        self.busy_turns: int = -1
        
        # param_2
        self.attack_radius = -1
        self.produces_unit = UnitType.NONE
        
        # custom
        self.was_once_fully_upgraded: bool = False
        
    def is_available(self):
        return self.type == SiteType.BARRACKS and self.owner == Owner.FRIEND and not self.busy_turns
    
    def dist_to(self, pos: list[int]) -> float:
        return math.dist(self.pos, pos)
    
    def update(self, gold: int, max_gold_rate: int, type_id: int, owner_id: int, param_1: int, param_2: int) -> None:
        self.gold = gold
        self.max_gold_rate = max_gold_rate
        self.type = SiteType(type_id)
        self.owner = Owner(owner_id)
        
        if self.type == SiteType.GOLDMINE:
            self.gold_rate = param_1
            if self.gold_rate == self.max_gold_rate:
                self.was_once_fully_upgraded = True
        elif self.type == SiteType.TOWER:
            self.max_gold_rate = 0
            self.hp = param_1
            self.attack_radius = param_2
            if self.attack_radius > 500:
                self.was_once_fully_upgraded = True
        elif self.type == SiteType.BARRACKS:
            self.max_gold_rate = 0
            self.busy_turns = param_1
            self.produces_unit = UnitType(param_2)
    
class FriendlySites:
    def __init__(self, sites: dict[int, Site]):
        self.sites: list[Site] = [site for site in sites.values() if site.owner == Owner.FRIEND]

    def get_by_type(self, type: SiteType) -> list[Site]:
        return [site for site in self.sites if site.type == type]

    def get_barracks_producing(self, type: UnitType) -> list[Site]:
        return [site for site in self.sites if site.type == SiteType.BARRACKS and site.produces_unit == type]

    def get_mines_to_upgrade(self) -> list[Site]:
        return [site for site in self.sites if site.type == SiteType.GOLDMINE and site.gold_rate < site.max_gold_rate]

    def get_towers_to_upgrade(self) -> list[Site]:
        return [site for site in self.sites if site.type == SiteType.TOWER and not site.was_once_fully_upgraded]

    def get_towers_sorted_by_range_asc(self) -> list[Site]:
        return sorted([site for site in self.sites if site.type == SiteType.TOWER], key=lambda site: site.attack_radius)
    
    def __str__(self):
        res: str = "friendly_sites: \n"
        res += "  ID | type     | max_GR | att_r | WOFU \n"
        res += " ----|----------|--------|-------|------ \n"
        for site in sorted(self.sites, key=lambda site: site.type.name):
            
            # all
            res += f"  {site.id:2d} | {site.type.name:8s} | "
            
            # mines
            if site.type == SiteType.GOLDMINE:
                res += f"    {site.max_gold_rate:2d} |       | "
            
            # towers
            elif site.type == SiteType.TOWER:
                res += f"       |   {site.attack_radius:3d} | "
                
            # barracks
            else:
                res += "       |       |     "
            
            wofu = "WOFU" if site.was_once_fully_upgraded else ""
            res += f"{wofu} \n"
        return res

class Unit:
    def __init__(self, pos: list[int], type: UnitType, owner: Owner, health: int):
        self.pos = pos
        self.type = type
        self.owner = owner
        self.health = health



####### #     # #     #  #####  ####### ### ####### #     #  ##### 
#       #     # ##    # #     #    #     #  #     # ##    # #     #
#       #     # # #   # #          #     #  #     # # #   # #      
#####   #     # #  #  # #          #     #  #     # #  #  #  ##### 
#       #     # #   # # #          #     #  #     # #   # #       #
#       #     # #    ## #     #    #     #  #     # #    ## #     #
#        #####  #     #  #####     #    ### ####### #     #  #####    


def update_sites(sites: dict[int, Site]):
    for i in range(len(sites)):
        id, gold, max_gold_rate, type_id, owner_id, param_1, param_2 = [int(j) for j in input().split()]
        sites[id].update(gold, max_gold_rate, type_id, owner_id, param_1, param_2)

def update_units() -> list[Unit]:
    units: list[Unit] = []
    num_units = int(input())
    for i in range(num_units):
        x, y, owner, type, health = [int(j) for j in input().split()]
        units.append(Unit([x, y], UnitType(type), Owner(owner), health))
    return units

def get_queens(units: list[Unit]) -> tuple[Unit, Unit]:
    my_queen = next(unit for unit in units if unit.type == UnitType.QUEEN and unit.owner == Owner.FRIEND)
    enemy_queen = next(unit for unit in units if unit.type == UnitType.QUEEN and unit.owner == Owner.ENEMY)
    return my_queen, enemy_queen

def get_build_string(closest_empty_side_id: int, friendly_sites: FriendlySites) -> str:
    upgradeable_mines = friendly_sites.get_mines_to_upgrade()
    upgradeable_towers = friendly_sites.get_towers_to_upgrade()
    
    # mines
    if len(upgradeable_mines) > 0:
        return f"BUILD {upgradeable_mines[0].id} MINE"
    elif len(friendly_sites.get_by_type(SiteType.GOLDMINE)) < 3:
        return f"BUILD {closest_empty_side_id} MINE"
    
    # barracks
    elif len(friendly_sites.get_barracks_producing(UnitType.KNIGHT)) < 1: 
        return f"BUILD {closest_empty_side_id} BARRACKS-KNIGHT"
    
    # towers
    elif len(upgradeable_towers) > 0: 
        return f"BUILD {upgradeable_towers[0].id} TOWER"
    else:
        return f"BUILD {closest_empty_side_id} TOWER"

def find_closest_not_friendly_site_id_to_pos(sites: dict[int, Site], pos: list[int]) -> int:
    min_dist = 10000
    id = -1
    for site in sites.values():
        if site.owner != Owner.FRIEND:
            dist = site.dist_to(pos)
            if dist < min_dist:
                min_dist = dist
                id = site.id
    return id

def find_n_closest_available_barracks(n: int, sites: dict[int, Site], pos: list[int]) -> list[int]:
    closest: list[Site] = sorted([site for site in sites.values() if site.is_available()], key=lambda site: site.dist_to(pos))
    return [site.id for site in closest[0:n]]


#
 #####     #    #     # #######    #       ####### ####### ###### 
#     #   # #   ##   ## #          #       #     # #     # #     #
#        #   #  # # # # #          #       #     # #     # #     #
#  #### #     # #  #  # #####      #       #     # #     # ###### 
#     # ####### #     # #          #       #     # #     # #      
#     # #     # #     # #          #       #     # #     # #      
 #####  #     # #     # #######    ####### ####### ####### #      


sites: dict[int, Site] = {}
num_sites = int(input())

for i in range(num_sites):
    id, x, y, radius = [int(j) for j in input().split()]
    sites[id] = Site(id, [x, y], radius)


while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    
    update_sites(sites)
    friendly_sites = FriendlySites(sites)
    print(friendly_sites, file=sys.stderr, flush=True)

    units = update_units()
    my_queen, enemy_queen = get_queens(units)
    
    closest_empty_site_id = find_closest_not_friendly_site_id_to_pos(sites, my_queen.pos)
    build_string = get_build_string(closest_empty_site_id, friendly_sites)
    print(build_string)

    train_ids: list[int] = find_n_closest_available_barracks(int(gold / 80), sites, enemy_queen.pos)
    train_str: str = ""
    for id in train_ids:
        train_str += " " + str(id)
    print(f"TRAIN{train_str}")
    

    
# last rank 195

# TODO: 1: dont rebuild mines
# TODO: 2: dont run in towers
# TODO: 3: stages:
#           0. save 3 mine spots
#           1. barrack, one push
#           2. build and upgrade 3-5 towers
#           3. build on mine spots
#           4. save for huge wave
# TODO: 4: counter many towers: giants or save gold for huge wave

# TODO: does a second mine on used site give new gold?
# TODO: if all sites full
