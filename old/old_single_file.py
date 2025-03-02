import math
import enum


#
 #####  #          #     #####   #####  #######  ##### 
#     # #         # #   #     # #     # #       #     #
#       #        #   #  #       #       #       #      
#       #       #     #  #####   #####  #####    ##### 
#       #       #######       #       # #             #
#     # #       #     # #     # #     # #       #     #
 #####  ####### #     #  #####   #####  #######  ##### 


WIDTH = 1920
HEIGHT = 1000
CENTER = [int(WIDTH / 2), int(HEIGHT / 2)]
CENTER_GAP = 300
    
class SiteType(enum.Enum):
    EMPTY = -1
    GOLDMINE = 0
    TOWER = 1
    BARRACKS = 2
    
class Owner(enum.Enum):
    NONE = -1
    FRIEND = 0
    ENEMY = 1
    
class UnitType(enum.Enum):
    NONE = -2
    QUEEN = -1
    KNIGHT = 0
    ARCHER = 1
    GIANT = 2

class Side(enum.Enum):
    UNKNOWN = 0
    LEFT = 1
    RIGHT = 2


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
       
    def is_empty_or_enemy_non_tower(self) -> bool:
        return self.type == SiteType.EMPTY or (self.owner == Owner.ENEMY and self.type != SiteType.TOWER)
         
    def is_inside_enemy_tower_range(self, enemy_towers: list["Site"]) -> bool:
        for tower in enemy_towers:
            dist = self.dist_to(tower.pos)
            if dist < tower.attack_radius:
                return True
        return False

    def is_on_my_side(self) -> bool:
        if center_of_towers[0] > CENTER[0]:
            return self.pos[0] >= CENTER[0]
        else:
            return self.pos[0] < CENTER[0]

    def __str__(self) -> str:
        return f"{self.id}"
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
        wofu = "WOFU" if self.was_once_fully_upgraded else ""
        res += f"{wofu}"
        # res += f" pos[0]: {self.pos[0]}, pos[1]: {self.pos[1]}"
        return res;
    
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
            res += f"{str(site)} \n"
        return res

class SitesManager:
    CENTER_X: int = 980
    
    @classmethod
    def from_input(cls):
        __sites_dict: dict[int, Site] = {}
        
        num_sites = int(input())
        for i in range(num_sites):
            id, x, y, radius = [int(j) for j in input().split()]
            __sites_dict[id] = Site(id, [x, y], radius)
            
        sites: list[Site] = [site for site in __sites_dict.values()]
    
    def __init__(self, site: Site):
        self.__sites_dict: dict[int, Site] = {}
        self.sites: list[Site] = [site for site in self.__sites_dict.values()]
        self.__sites_dict[0] = site
    
    def update_sites(self):
        for i in range(len(self.__sites_dict)):
            id, gold, max_gold_rate, type_id, owner_id, param_1, param_2 = [int(j) for j in input().split()]
            self.__sites_dict[id].update(gold, max_gold_rate, type_id, owner_id, param_1, param_2)
    
    @property
    def friendly(self) -> list[Site]:
        return [site for site in self.sites if site.owner == Owner.FRIEND]


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


def update_units() -> list[Unit]:
    units: list[Unit] = []
    num_units = int(input())
    for i in range(num_units):
        x, y, owner, type, health = [int(j) for j in input().split()]
        units.append(Unit([x, y], UnitType(type), Owner(owner), health))
    return units

def get_queens(units: list[Unit], center_of_towers: list[int]) -> tuple[Unit, Unit, list[int]]:
    my_queen = next(unit for unit in units if unit.type == UnitType.QUEEN and unit.owner == Owner.FRIEND)
    if center_of_towers[0] < 0:
        if my_queen.pos[0] > CENTER[0]:
            center_of_towers = [CENTER[0] + CENTER_GAP, CENTER[1]]
        else:
            center_of_towers = [CENTER[0] - CENTER_GAP, CENTER[1]]
    enemy_queen = next(unit for unit in units if unit.type == UnitType.QUEEN and unit.owner == Owner.ENEMY)
    return my_queen, enemy_queen, center_of_towers

def get_new_tower_id() -> int:
    available_sites = [site for site in sites.values() if site.is_empty_or_enemy_non_tower()]
    sorted_sites = sorted(available_sites, key=lambda site: site.dist_to(center_of_towers))
    return sorted_sites[0].id if sorted_sites else -1

def get_new_mine_id() -> int:
    available_sites = [site for site in sites.values() if site.is_empty_or_enemy_non_tower()]
    sorted_sites = sorted(available_sites, key=lambda site: site.pos[0], reverse=center_of_towers[0] > CENTER[0])
    return sorted_sites[0].id if sorted_sites else -1
    
def get_build_string(build_id: int, friendly_sites: FriendlySites) -> str:
    upgradeable_mines = friendly_sites.get_mines_to_upgrade()
    upgradeable_towers = friendly_sites.get_towers_to_upgrade()
    
    # barracks
    if len(friendly_sites.get_barracks_producing(UnitType.KNIGHT)) < 1 and build_id >= 0: 
        return f"BUILD {build_id} BARRACKS-KNIGHT"
    
    # towers
    new_tower_id = get_new_tower_id()
    if len(friendly_sites.get_by_type(SiteType.TOWER)) < 3 and new_tower_id >= 0:
        return f"BUILD {new_tower_id} TOWER"
    if upgradeable_towers: 
        return f"BUILD {upgradeable_towers[0].id} TOWER"
    
    # mines
    new_mine_id = get_new_mine_id()
    if len(upgradeable_mines) > 0:
        return f"BUILD {upgradeable_mines[0].id} MINE"
    if len(friendly_sites.get_by_type(SiteType.GOLDMINE)) < 3 and new_mine_id >= 0:
        return f"BUILD {new_mine_id} MINE"
    else:
        return f"BUILD {friendly_sites.get_by_type(SiteType.TOWER)[0].id} TOWER"

def find_closest_safely_buildable_site_id(sites: dict[int, Site], pos: list[int]) -> int:
    enemy_towers = [site for site in sites.values() if site.owner == Owner.ENEMY and site.type == SiteType.TOWER]
    
    min_dist = 10000
    id = -1
    for site in sites.values():
        if site.is_empty_or_enemy_non_tower() and site.is_on_my_side() and not site.is_inside_enemy_tower_range(enemy_towers):
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


sites = SitesManager()

while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    
    sites.update_sites(sites)
    friendly_sites = FriendlySites(sites)
    # print(friendly_sites, file=sys.stderr, flush=True)

    units = update_units()
    my_queen, enemy_queen, center_of_towers = get_queens(units, center_of_towers)
    
    build_id = find_closest_safely_buildable_site_id(sites, my_queen.pos)
    build_string = get_build_string(build_id, friendly_sites)
    print(build_string)
    
    train_ids: list[int] = find_n_closest_available_barracks(int(gold / 80), sites, enemy_queen.pos)
    train_str: str = ""
    for id in train_ids:
        train_str += " " + str(id)
    print(f"TRAIN{train_str}")
    
# print("Hello")
# sm = SitesManager(Site(0, [1, 2], 3))
# print(sm.sites)
# print(sm.friendly)
# sm.sites[0].owner = Owner.FRIEND
# print(sm.friendly)

    
# TODO: 1: dont rebuild mines
# DONE: 2: dont run in towers
# TODO: 3: stages:
#           0. save 3 mine spots
#           1. barrack, one push
#           2. build and upgrade 3-5 towers
#           3. build on mine spots
#           4. save for huge wave
# TODO: 4: counter many towers: giants or save gold for huge wave

# TODO: if all sites full

# a second mine on mined-out site does not give new gold
# barracks and mines can be destroyed and built over by queen

# 224 mit nr 7
# 87?
# 221 mit nr 6