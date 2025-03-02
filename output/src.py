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
    
    TOWER_TARGET_RADIUS = 500
    # TODO: refine
    TOWER_MIN_RADIUS = 70

    SAVING_LIMIT = 200
    
    MIN_GOLD_FOR_MINE = 70
    
    ENEMY_UNIT_SAFETY_DIST = 300
    
    # PlanStrategy
    TOWER_SHARE = 0.3
    BARRACKS_AMOUNT = 3
    
    # ReactStrategy
    TARGET_MINES = 3
    TARGET_TOWERS = 3
    TARGET_KNIGHTS_BARRACKS = 1
    TARGET_GIANTS_BARRACKS = 1
    


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
    def from_type_number(cls, type_number) -> "UnitType":
        for unit_type in cls:
            if unit_type.type_number == type_number:
                return unit_type
        raise ValueError(f"UnitType with type_number {type_number} not found.")



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
        self.was_fully_upgraded: bool = False
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
                self.was_fully_upgraded = True
        elif self.type == SiteType.TOWER:
            self.max_gold_rate = 0
            self.hp = param_1
            self.attack_radius = param_2
            if self.attack_radius > Params.TOWER_TARGET_RADIUS:
                self.was_fully_upgraded = True
            elif self.attack_radius < Params.TOWER_MIN_RADIUS:
                self.was_fully_upgraded = False
        elif self.type == SiteType.BARRACKS:
            self.max_gold_rate = 0
            self.busy_turns = param_1
            self.produces_unit = UnitType.from_type_number(param_2)
    
    def is_in_roi(self, start_side: Side) -> bool:
        return (self.pos[0] < Params.CENTER[0]) == (start_side == Side.LEFT)
    
    def is_buildable(self) -> bool:
        return self.type == SiteType.EMPTY or (self.owner == Owner.ENEMY and self.type != SiteType.TOWER)
    
    def needs_upgrade(self) -> bool:
        if self.type == SiteType.MINE:
            return self.gold_rate < self.max_gold_rate
        elif self.type == SiteType.TOWER:
            return self.attack_radius < Params.TOWER_TARGET_RADIUS
        else:
            return False
    
    # TODO: remove
    def is_inside_tower_range(self, towers: list["Site"]) -> bool:
        for tower in towers:
            dist = self.dist_to(tower.pos)
            if dist < tower.attack_radius:
                return True
        return False
    
    def is_too_close_to(self, enemies: list) -> bool:
        for enemy in enemies:
            dist = self.dist_to(enemy.pos)
            if isinstance(enemy, Site) and dist < enemy.attack_radius:
                return True
            if isinstance(enemy, Unit) and dist < Params.ENEMY_UNIT_SAFETY_DIST:
                return True
        return False

    def __repr__(self) -> str:
        shall_be_complete: bool = False
        if shall_be_complete:
            return (f"Site [id = {self.id}, pos = {self.pos}, radius = {self.radius}, gold: {self.gold}, "
                    f"max_gold_rate = {self.max_gold_rate}, type = {self.type}, owner = {self.owner}, "
                    f"gold_rate = {self.gold_rate}, hp = {self.hp}, busy_turns = {self.busy_turns}, "
                    f"attack_radius = {self.attack_radius}, produces_unit = {self.produces_unit}, "
                    f"was_once_fully_upgraded = {self.was_fully_upgraded}]")
        else:
            return (f"Site [id = {self.id:2d}, pos = {str(self.pos):12s}, att_radius = {self.attack_radius:3d}, planned = {str(self.planned_type.name):8s}]")
    


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
    def enemy(self):
        self.sites = [site for site in self.sites if site.owner == Owner.ENEMY]
        return self
    
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
    def wnfu(self):
        self.sites = [site for site in self.sites if not site.was_fully_upgraded]
        return self
    
    @property
    def needs_upgrade(self):
        self.sites = [site for site in self.sites if site.needs_upgrade()]
        return self
    
    @property
    def gold_left(self):
        self.sites = [site for site in self.sites if site.gold > Params.MIN_GOLD_FOR_MINE]
        return self
    
    @property
    def buildable(self):
        self.sites = [site for site in self.sites if site.is_buildable()]
        return self
    
    @property
    def empty(self):
        self.sites = [site for site in self.sites if site.type == SiteType.EMPTY]
        return self
    
    @property
    def furthest_back(self):
        self.sites = sorted(self.sites, key=lambda site: site.pos[0], reverse=self.start_side == Side.RIGHT)
        return self
    
    def planned(self, type: SiteType):
        self.sites = [site for site in self.sites if site.planned_type == type and site.is_buildable()]
        return self
    
    def produces(self, unit_type):
        self.sites = [site for site in self.sites if site.produces_unit == unit_type]
        return self
    
    def safe(self, enemies: list):
        self.sites = [site for site in self.sites if not site.is_too_close_to(enemies)]
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
        # TODO: remove
        # for site in self.__sites_dict.values():
        #     site.side = Side.RIGHT if site.pos[0] >= Params.CENTER[0] else Side.LEFT
    
    # for PlanStrategy, maybe TODO: move there
    def plan_sites(self) -> None:
        sites_in_roi = [site for site in self.__sites_dict.values() if site.is_in_roi(self.start_side)]
        sites_in_roi.sort(key=lambda site: site.pos[0], reverse=self.start_side == Side.LEFT)
        # TODO: plan towers close to center
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
    
    @property
    def enemy(self):
        self.units = [unit for unit in self.units if unit.owner == Owner.ENEMY]
        return self
    
    # @property
    # def friendly(self) -> list[Unit]:
    #     return [unit for unit in self.units if unit.owner == Owner.FRIENDLY]
    
    # @property
    # def enemy(self) -> list[Unit]:
    #     return [unit for unit in self.units if unit.owner == Owner.ENEMY]
    
    def get(self) -> list[Unit]:
        return self.units
    
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
    
    @property
    def sites(self):
        return self.SM.sites
    
    @property
    def units(self):
        return self.um.units
    
    def update(self) -> None:
        self.gold, self.touched_site = [int(i) for i in input().split()]
        self.SM.update_from_input()
        self.um = UnitsManager.from_input()
    
    def build(self):
        raise NotImplementedError("Please Implement this method")
            
    def train(self):
        raise NotImplementedError("Please Implement this method")
    
    def train_big_wave(self):
        barracks = self.SM.sites.my.barracks.get()
        barracks.sort(key=lambda barracks: barracks.dist_to(Params.CENTER))
        ids = []
        for barrack in barracks:
            if barrack.busy_turns <= 0 and self.gold >= barrack.produces_unit.cost:
                self.gold -= barrack.produces_unit.cost
                ids.append(str(barrack.id))
        if ids:
            id_str = ""
            for id in ids:
                id_str += " " + id
            print(f"argh ids: {ids}", file=sys.stderr, flush=True)
            print(f"TRAIN{id_str}")
        else:
            print("TRAIN")
    
    def __repr__(self) -> str:
        return (f"GameManager []")
    


# game/PlanStrategy.py


class PlanStrategy(GameManager):
    def build(self):
        next_barracks = self.SM.sites.planned(SiteType.BARRACKS).get_closest_to(self.um.units.my_queen.pos)
        enemy_towers = self.SM.sites.enemy.towers.get()
        # TODO: build towers closer to center
        next_tower = self.SM.sites.planned(SiteType.TOWER).safe(enemy_towers).get_closest_to(self.um.units.my_queen.pos)
        enemy_units = self.um.units.enemy.get()
        # TODO: if not safe build tower instead
        next_mine = self.SM.sites.planned(SiteType.MINE).gold_left.safe(enemy_units).get_closest_to(self.um.units.my_queen.pos)
        
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
    


# game/ReactStrategy.py


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
    


# game/OldStrategy.py


class OldStrategy(GameManager):
    def build(self):
        # TODO: test buildable instead of empty
        closest_empty_site = self.sites.empty.get_closest_to(self.units.my_queen.pos)
        upgradeable_mines = sorted(self.sites.my.mines.needs_upgrade.get(), key=lambda site: site.dist_to(self.units.my_queen.pos))
        upgradeable_towers = sorted(self.sites.my.towers.wnfu.get(), key=lambda site: site.dist_to(self.units.my_queen.pos))
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
    


# main.py



GM = OldStrategy()

while True:
    GM.update()
    GM.build()
    GM.train()
        
# python3 merger.py; Get-Content output/src.py | Set-Clipboard
# To debug: print("Debug messages...", file=sys.stderr, flush=True)



