import sys
import math
from enum import Enum



# TODO: maybe 400
BORDER_X = 450
MIN_GOLD = 80
SAFETY_PUFFER_TOWER = 40
SAFETY_DIST_KNIGHT = 100
MIN_RADIUS = 300
MAX_RADIUS = 500



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
        self.shall_not_be_upgraded: bool = False
        
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
                self.shall_not_be_upgraded = True
            else:
                self.shall_not_be_upgraded = False
        elif self.type == SiteType.TOWER:
            self.max_gold_rate = 0
            self.hp = param_1
            self.attack_radius = param_2
            if self.attack_radius > MAX_RADIUS:
                self.shall_not_be_upgraded = True
            elif self.attack_radius < MIN_RADIUS:
                self.shall_not_be_upgraded = False
        elif self.type == SiteType.BARRACKS:
            self.max_gold_rate = 0
            self.busy_turns = param_1
            self.produces_unit = UnitType(param_2)
            
    def __str__(self) -> str:
        res: str = ""
        # all
        res += f"  {self.id:2d} | {self.type.name:8s} | "
        # goldmines
        if self.type == SiteType.GOLDMINE:
            res += f"    {self.max_gold_rate:2d} |       | "
        # towers
        elif self.type == SiteType.TOWER:
            res += f"       |   {self.attack_radius:3d} | "
        # barracks
        else:
            res += "       |       |     "
        # all
        wofu = "WOFU" if self.shall_not_be_upgraded else ""
        res += f"{wofu}"
        return res
    
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
        return [site for site in self.sites if site.type == SiteType.TOWER and not site.shall_not_be_upgraded]

    def get_towers_sorted_by_range_asc(self) -> list[Site]:
        return sorted([site for site in self.sites if site.type == SiteType.TOWER], key=lambda site: site.attack_radius)
    
    def find_outest_tower(self) -> Site | None:
        outest_towers = sorted([site for site in self.sites if site.type == SiteType.TOWER], key=lambda site: min(site.pos[0], 1920 - site.pos[0]))
        if outest_towers:
            return outest_towers[0]
        else:
            return None 
    
    def find_outest_tower_with_gold(self) -> Site | None:
        outest_towers = sorted([site for site in self.sites if site.type == SiteType.TOWER], key=lambda site: min(site.pos[0], 1920 - site.pos[0]))
        outest_towers_with_gold = [tower for tower in outest_towers if tower.gold > MIN_GOLD]
        if outest_towers_with_gold:
            return outest_towers_with_gold[0]
        else:
            return None 
    
    def __str__(self):
        res: str = "friendly_sites: \n"
        res += "  ID | type     | max_GR | att_r | WOFU \n"
        res += " ----|----------|--------|-------|------ \n"
        for site in sorted(self.sites, key=lambda site: site.type.name):
            res += f"{str(site)} \n"
        return res

class Unit:
    def __init__(self, pos: list[int], type: UnitType, owner: Owner, health: int):
        self.pos = pos
        self.type = type
        self.owner = owner
        self.health = health
        
    def __repr__(self) -> str:
        return f" {self.type:6s} [{self.pos[0], self.pos[1]}]"



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

def is_too_close_to_tower_range(pos: list[int], towers: list[Site]) -> bool:
    for tower in towers:
        dist = math.dist(pos, tower.pos)
        if dist <= tower.attack_radius + SAFETY_PUFFER_TOWER:
            return True
    return False

def get_build_string(closest_empty_site: Site, friendly_sites: FriendlySites, enemy_towers, are_enemy_knights_close) -> str:
    upgradeable_mines = friendly_sites.get_mines_to_upgrade()
    upgradeable_towers = friendly_sites.get_towers_to_upgrade()
    safely_upgradeable_towers = [tower for tower in upgradeable_towers if not is_too_close_to_tower_range(tower.pos, enemy_towers)]
    my_towers = friendly_sites.get_towers_sorted_by_range_asc()
    
    # TODO: 1: dont build mine when creeps close, and not with no gold
    # TODO: 2: dont run in towers
    # TODO: 3: no more empty sites
    # TODO: 4: late game: more mines, giants, save gold for huge wave?
    
    # if knights are close
        # if towers >= 2
            # upgrade outest tower
        # else
            # if knights left
                # next empty on right build tower
            # else
                # next empty on left build tower
                
    
    # mines
    if len(upgradeable_mines) > 0 and not are_enemy_knights_close:
        return f"BUILD {upgradeable_mines[0].id} MINE"
    elif len(friendly_sites.get_by_type(SiteType.GOLDMINE)) < 3:
        if closest_empty_site != None and closest_empty_site.gold > MIN_GOLD and not are_enemy_knights_close:
            return f"BUILD {closest_empty_site.id} MINE"
        else:
            outest_tower_with_gold = friendly_sites.find_outest_tower_with_gold()
            if outest_tower_with_gold and not are_enemy_knights_close:
                return f"BUILD {outest_tower_with_gold.id} MINE"
    
    # barracks
    if closest_empty_site != None and len(friendly_sites.get_barracks_producing(UnitType.KNIGHT)) < 1: 
        return f"BUILD {closest_empty_site.id} BARRACKS-KNIGHT"
    
    # towers
    # TODO: check and combine (safely_)upgradeable_towers
    elif upgradeable_towers: 
        return f"BUILD {upgradeable_towers[0].id} TOWER"
    # TODO: build giant if towers >= 5
    elif closest_empty_site != None:
        is_outside = closest_empty_site.pos[0] < BORDER_X or closest_empty_site.pos[0] > 1920 - BORDER_X
        if is_outside and len(my_towers) >= 3 and closest_empty_site.gold > MIN_GOLD and not are_enemy_knights_close:
            return f"BUILD {closest_empty_site.id} MINE"
        else:
            return f"BUILD {closest_empty_site.id} TOWER"
    elif safely_upgradeable_towers:
        return f"BUILD {upgradeable_towers[0].id} TOWER"
    else:
        outest_tower = friendly_sites.find_outest_tower()
        if (outest_tower):
            return f"BUILD {outest_tower.id} TOWER"
        else:
            # TODO: move to outside
            return "WAIT"
    
def find_closest_empty_site_to_pos(sites: dict[int, Site], pos: list[int], enemy_towers) -> Site | None:
    min_dist = 10000
    res_site = None
    for site in sites.values():
        if site.type == SiteType.EMPTY and not is_too_close_to_tower_range(site.pos, enemy_towers):
            dist = site.dist_to(pos)
            if dist < min_dist:
                min_dist = dist
                res_site = site
    return res_site

def find_n_closest_available_barracks(n: int, sites: dict[int, Site], pos: list[int]) -> list[int]:
    closest: list[Site] = sorted([site for site in sites.values() if site.is_available()], key=lambda site: site.dist_to(pos))
    return [site.id for site in closest[0:n]]

def are_enemy_knights_close(pos: list[int], enemy_knights: list[Unit]) -> bool:
    for knight in enemy_knights:
        dist = math.dist(pos, knight.pos)
        if dist <= SAFETY_DIST_KNIGHT:
            print("enemy knights are close", file=sys.stderr, flush=True)
            return True
    return False


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
    # print(friendly_sites, file=sys.stderr, flush=True)
    enemy_towers = [site for site in sites.values() if (site.owner == Owner.ENEMY and site.type == SiteType.TOWER)]

    units = update_units()
    my_queen, enemy_queen = get_queens(units)
    enemy_knights = [unit for unit in units if unit.owner == Owner.ENEMY and unit.type == UnitType.KNIGHT]
    
    closest_empty_site = find_closest_empty_site_to_pos(sites, my_queen.pos, enemy_towers)
    build_string = get_build_string(closest_empty_site, friendly_sites, enemy_towers, are_enemy_knights_close(my_queen.pos, enemy_knights))
    print(build_string)

    train_ids: list[int] = find_n_closest_available_barracks(int(gold / 80), sites, enemy_queen.pos)
    train_str: str = ""
    for id in train_ids:
        train_str += " " + str(id)
    print(f"TRAIN{train_str}")
    

    
# last rank 2166

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

# TODO: dont build on other side
# TODO: run away from enemy knights
