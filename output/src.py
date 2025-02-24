import enum
import math



# sites/Side.py

class Side(enum.Enum):
    UNKNOWN = 0
    LEFT = 1
    RIGHT = 2



# sites/SiteType.py

class SiteType(enum.Enum):
    EMPTY = -1
    GOLDMINE = 0
    TOWER = 1
    BARRACKS = 2
    


# units/UnitType.py

class UnitType(enum.Enum):
    NONE = -2
    QUEEN = -1
    KNIGHT = 0
    ARCHER = 1
    GIANT = 2



# owner/Owner.py

class Owner(enum.Enum):
    NONE = -1
    FRIEND = 0
    ENEMY = 1



# sites/Site.py

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
         
    def is_inside_tower_range(self, towers: list["Site"]) -> bool:
        for tower in towers:
            dist = self.dist_to(tower.pos)
            if dist < tower.attack_radius:
                return True
        return False

    def __repr__(self) -> str:
        shall_be_complete: bool = False
        if shall_be_complete:
            return (f"Site [id = {self.id}, pos = {self.pos}, radius = {self.radius}, gold: {self.gold}, "
                    f"max_gold_rate = {self.max_gold_rate}, type = {self.type}, owner = {self.owner}, "
                    f"gold_rate = {self.gold_rate}, hp = {self.hp}, busy_turns = {self.busy_turns}, "
                    f"attack_radius = {self.attack_radius}, produces_unit = {self.produces_unit}, "
                    f"was_once_fully_upgraded = {self.was_once_fully_upgraded}]")
        else:
            return (f"Site [id = {self.id}, pos = {self.pos}]")
    


# sites/SitesAccessBuilder.py

class SitesAccessBuilder:
    def __init__(self, sites: list[Site]):
        self.sites: list[Site] = sites
    
    def __repr__(self) -> str:
        return f"SitesAccessBuilder [sites = [{self.sites}]]"
    


# sites/SitesManager.py

class SitesManager:
    __CENTER_X: int = 980
    
    def __init__(self):
        self.__sites_dict: dict[int, Site] = {}
        
        num_sites = int(input())
        for i in range(num_sites):
            id, x, y, radius = [int(j) for j in input().split()]
            self.__sites_dict[id] = Site(id, [x, y], radius)
    
    def __init__(self, site: Site):
        self.__sites_dict: dict[int, Site] = {site.id: site}
    
    def update_sites(self) -> None:
        for i in range(len(self.__sites_dict)):
            id, gold, max_gold_rate, type_id, owner_id, param_1, param_2 = [int(j) for j in input().split()]
            self.__sites_dict[id].update(gold, max_gold_rate, type_id, owner_id, param_1, param_2)
    
    @property
    def sites(self) -> SitesAccessBuilder:
        return SitesAccessBuilder([site for site in self.__sites_dict])
    
    def __repr__(self):
        return f"SitesManager [__sites_dict = {self.__sites_dict}]"



# units/Unit.py

class Unit:
    def __init__(self, pos: list[int], type: UnitType, owner: Owner, health: int):
        self.pos = pos
        self.type = type
        self.owner = owner
        self.health = health
    
    def __repr__(self):
        return str(self)



# test.py

print()

site = Site(1, [2, 3], 4)
print("site", site)

SM = SitesManager(site)
print("sm", SM)

sab: SitesAccessBuilder = SitesAccessBuilder([site])
print("sab", sab)
print("sab.sites", sab.sites)
print("sab.sites[0]", sab.sites[0])
print("sab.sites[0].pos", sab.sites[0].pos)

print()



