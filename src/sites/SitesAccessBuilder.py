from params import Params
from sites.Side import Side
from sites.Site import Site

class SitesAccessBuilder:
    def __init__(self, sites: list[Site], start_side: Side):
        self.sites: list[Site] = sites
        self.start_side = start_side
        
    def __planned_barracks(self):
        self.sites = [site for site in self.sites 
                if site.side == self.start_side 
                and Params.MAX_TOWER_DIST < site.dist_to(Params.MIDDLE) <= Params.MAX_BARRACKS_DIST
                and site.is_empty_or_enemy_non_tower()]
        return self
    
    # @property
    # def friendly(self) -> list[Site]:
    #     return [site for site in self.sites if site.owner == Owner.FRIENDLY]
    
    # @property
    # def enemy(self) -> list[Site]:
    #     return [site for site in self.sites if site.owner == Owner.ENEMY]
    
    # def get(self) -> list[Site]:
    #     return self.sites
    
    def __get_closest_to(self, pos):
        if sites := sorted(self.sites, key=lambda site: site.dist_to(pos)):
            return sites[0]
        else: return None

    def next_barracks_to_build(self, pos):
        if site := self.__planned_barracks().__get_closest_to(pos):
            return site
        else: return None
    
    def __repr__(self) -> str:
        return f"SitesAccessBuilder [sites = {self.sites}]"
    