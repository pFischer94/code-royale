import sys

from params import Params
from sites.Side import Side
from sites.SitesAccessBuilder import SitesAccessBuilder
from sites.Site import Site
from sites.SiteType import SiteType

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
    
    # PlanStrategy
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
