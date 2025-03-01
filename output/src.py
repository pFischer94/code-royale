import math
import enum
import sys



# params.py

class Params:
    WIDTH = 1920
    HEIGHT = 1000
    CENTER = [int(WIDTH / 2), int(HEIGHT / 2)]
    
    # MAX_DIST_TO_MIDDLE = math.dist([0, 0], CENTER)
    # MAX_TOWER_DIST = MAX_DIST_TO_MIDDLE * 0.4
    # MAX_BARRACKS_DIST = MAX_DIST_TO_MIDDLE * 0.6
    
    # if MAX_TOWER_DIST >= MAX_BARRACKS_DIST:
    #     raise Exception("Invalid Params") 
    
    TOWER_SHARE = 0.3
    BARRACKS_AMOUNT = 3
    
    TOWER_TARGET_RADIUS = 350
    
    SAVING_LIMIT = 200


# sites/Side.py

class Side(enum.Enum):
    UNKNOWN = 0
    LEFT = 1
    RIGHT = 2



# sites/SiteType.py

class SiteType(enum.Enum):
    EMPTY = -1
    MINE = 0
    TOWER = 1
    BARRACKS = 2
    


# units/UnitType.py

class UnitType(enum.Enum):
    NONE = (-2, 0, 0)
    QUEEN = (-1, 0, 1)
    KNIGHT = (0, 80, 4)
    ARCHER = (1, 100, 2)
    GIANT = (2, 140, 1)
    
    def __init__(self, type_number, cost, amount):
        self.type_number = type_number
        self.cost = cost
        self.amount = amount
        
    @classmethod
    def from_type_number(cls, type_number):
        for unit_type in cls:
            if unit_type.type_number == type_number:
                return unit_type



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
        self.planned_type = SiteType.EMPTY
        
    def dist_to(self, pos: list[int]) -> float:
        return math.dist(self.pos, pos)
    
    def update(self, gold: int, max_gold_rate: int, type_id: int, owner_id: int, param_1: int, param_2: int) -> None:
        self.gold = gold
        self.max_gold_rate = max_gold_rate
        self.type = SiteType(type_id)
        self.owner = Owner(owner_id)
        
        if self.type == SiteType.MINE:
            self.gold_rate = param_1
            if self.gold_rate == self.max_gold_rate:
                self.was_once_fully_upgraded = True
        elif self.type == SiteType.TOWER:
            self.max_gold_rate = 0
            self.hp = param_1
            self.attack_radius = param_2
            if self.attack_radius > Params.TOWER_TARGET_RADIUS:
                self.was_once_fully_upgraded = True
        elif self.type == SiteType.BARRACKS:
            self.max_gold_rate = 0
            self.busy_turns = param_1
            self.produces_unit = UnitType.from_type_number(param_2)
    
    def is_in_roi(self, start_side: Side) -> bool:
        return (self.pos[0] < Params.CENTER[0]) == (start_side == Side.LEFT)
    
    def is_empty_or_enemy_non_tower(self) -> bool:
        return self.type == SiteType.EMPTY or (self.owner == Owner.ENEMY and self.type != SiteType.TOWER)
    
    def needs_upgrade(self) -> bool:
        if self.type == SiteType.MINE:
            return self.gold_rate < self.max_gold_rate
        elif self.type == SiteType.TOWER:
            return self.attack_radius < Params.TOWER_TARGET_RADIUS
        else:
            return False
    
    # def is_inside_tower_range(self, towers: list["Site"]) -> bool:
    #     for tower in towers:
    #         dist = self.dist_to(tower.pos)
    #         if dist < tower.attack_radius:
    #             return True
    #     return False

    def __repr__(self) -> str:
        shall_be_complete: bool = False
        if shall_be_complete:
            return (f"Site [id = {self.id}, pos = {self.pos}, radius = {self.radius}, gold: {self.gold}, "
                    f"max_gold_rate = {self.max_gold_rate}, type = {self.type}, owner = {self.owner}, "
                    f"gold_rate = {self.gold_rate}, hp = {self.hp}, busy_turns = {self.busy_turns}, "
                    f"attack_radius = {self.attack_radius}, produces_unit = {self.produces_unit}, "
                    f"was_once_fully_upgraded = {self.was_once_fully_upgraded}]")
        else:
            return (f"Site [id = {self.id:2d}, pos = {str(self.pos):12s}, planned: {str(self.planned_type.name):8s}]")
    


# sites/SitesAccessBuilder.py

class SitesAccessBuilder:
    def __init__(self, sites: list[Site], start_side: Side):
        self.sites: list[Site] = sites
        self.start_side = start_side
    
    @property
    def my(self):
        self.sites = [site for site in self.sites if site.owner == Owner.FRIEND]
        return self
    
    @property
    def enemy(self) -> list[Site]:
        return [site for site in self.sites if site.owner == Owner.ENEMY]
    
    @property
    def barracks(self):
        self.sites = [site for site in self.sites if site.type == SiteType.BARRACKS]
        return self
    
    @property
    def mines(self):
        self.sites = [site for site in self.sites if site.type == SiteType.MINE]
        return self
    
    @property
    def towers(self):
        self.sites = [site for site in self.sites if site.type == SiteType.TOWER]
        return self
    
    @property
    def idle(self):
        self.sites = [site for site in self.sites if site.busy_turns == 0]
        return self
    
    @property
    def wnofu(self):
        self.sites = [site for site in self.sites if not site.was_once_fully_upgraded]
        return self
    
    @property
    def needs_upgrade(self):
        self.sites = [site for site in self.sites if site.needs_upgrade()]
        return self
    
    def planned(self, type: SiteType):
        self.sites = [site for site in self.sites if site.planned_type == type and site.is_empty_or_enemy_non_tower()]
        return self
    
    def produces(self, unit_type):
        self.sites = [site for site in self.sites if site.produces_unit == unit_type]
        return self
    
    def get(self) -> list[Site]:
        return self.sites
    
    def get_closest_to(self, pos):
        if sites := sorted(self.sites, key=lambda site: site.dist_to(pos)):
            return sites[0]
        else: return None
    
    def len(self):
        return len(self.sites)

    def __repr__(self) -> str:
        return f"SitesAccessBuilder [sites = {self.sites}]"
    


# sites/SitesManager.py


class SitesManager:
    def __init__(self, sites: dict[int, Site]):
        self.__sites_dict: dict[int, Site] = sites
        self.start_side = Side.UNKNOWN
    
    @classmethod
    def from_input(cls):
        sites_dict: dict[int, Site] = {}
        num_sites = int(input())
        for i in range(num_sites):
            id, x, y, radius = [int(j) for j in input().split()]
            sites_dict[id] = Site(id, [x, y], radius)
        return cls(sites_dict)
    
    def update_from_input(self) -> None:
        for i in range(len(self.__sites_dict)):
            id, gold, max_gold_rate, type_id, owner_id, param_1, param_2 = [int(j) for j in input().split()]
            self.__sites_dict[id].update(gold, max_gold_rate, type_id, owner_id, param_1, param_2)
    
    def save_start_side(self, queen_pos: list[int]) -> None:
        self.start_side = Side.RIGHT if queen_pos[0] >= Params.CENTER[0] else Side.LEFT
        for site in self.__sites_dict.values():
            site.side = Side.RIGHT if site.pos[0] >= Params.CENTER[0] else Side.LEFT
    
    def plan_sites(self) -> None:
        sites_in_roi = [site for site in self.__sites_dict.values() if site.is_in_roi(self.start_side)]
        sites_in_roi.sort(key=lambda site: site.pos[0], reverse=self.start_side == Side.LEFT)
        print(len(sites_in_roi), file=sys.stderr, flush=True)
        tower_amount = Params.TOWER_SHARE * len(sites_in_roi)
        for i in range(len(sites_in_roi)):
            site = sites_in_roi[i]
            if i < tower_amount:
                site.planned_type = SiteType.TOWER
            elif i < tower_amount + Params.BARRACKS_AMOUNT:
                site.planned_type = SiteType.BARRACKS
            else:
                site.planned_type = SiteType.MINE
            print(site, file=sys.stderr, flush=True)
    
    @property
    def sites(self) -> SitesAccessBuilder:
        """Generates new SitesAccessBuilder with all sites and start_side."""
        
        return SitesAccessBuilder([site for site in self.__sites_dict.values()], self.start_side)
    
    def __repr__(self):
        res = f"SitesManager [start_side = {self.start_side}] sites:\n"
        for site in self.__sites_dict.values():
            res += f"{site}\n"
        return res



# units/Unit.py

class Unit:
    def __init__(self, pos: list[int], type: UnitType, owner: Owner, health: int):
        self.pos = pos
        self.type = type
        self.owner = owner
        self.health = health
    
    def __repr__(self):
        return (f"Unit [pos = {self.pos}, type = {self.type}, owner = {self.owner}, health = {self.health}]")



# units/UnitsAccessBuilder.py

class UnitsAccessBuilder:
    def __init__(self, units: list[Unit]):
        self.units: list[Unit] = units
    
    @property
    def my_queen(self) -> Unit:
        return [unit for unit in self.units if unit.type == UnitType.QUEEN and unit.owner == Owner.FRIEND][0]
    
    # @property
    # def friendly(self) -> list[Unit]:
    #     return [unit for unit in self.units if unit.owner == Owner.FRIENDLY]
    
    # @property
    # def enemy(self) -> list[Unit]:
    #     return [unit for unit in self.units if unit.owner == Owner.ENEMY]
    
    # def get(self) -> list[Unit]:
    #     return self.units
    
    def __repr__(self) -> str:
        return f"UnitsAccessBuilder [units = {self.units}]"
    


# units/UnitsManager.py

class UnitsManager:
    def __init__(self, units: list[Unit]):
        self.__units: list[Unit] = units
    
    @classmethod
    def from_input(cls):
        units: list[Unit] = []
        num_units = int(input())
        for i in range(num_units):
            x, y, owner, type, health = [int(j) for j in input().split()]
            units.append(Unit([x, y], UnitType.from_type_number(type), Owner(owner), health))
        return cls(units)
    
    @property
    def units(self) -> UnitsAccessBuilder:
        return UnitsAccessBuilder(self.__units)
    
    def __repr__(self):
        return f"UnitsManager [units = {self.__units}]"



# game/GameManager.py


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
    


# main.py



GM = GameManager()

while True:
    GM.update()
    GM.build()
    GM.train()
        
# python3 merger.py; Get-Content output/src.py | Set-Clipboard
# To debug: print("Debug messages...", file=sys.stderr, flush=True)



