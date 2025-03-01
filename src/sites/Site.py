import math
import sys

from owner.Owner import Owner
from params import Params
from sites.Side import Side
from sites.SiteType import SiteType
from units.UnitType import UnitType
from units.Unit import Unit

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
    