from params import Params
from sites.Side import Side
from sites.Site import Site
from sites.SiteType import SiteType
from owner.Owner import Owner

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
    def idle(self):
        self.sites = [site for site in self.sites if site.busy_turns == 0]
        return self
    
    def planned(self, type: SiteType):
        self.sites = [site for site in self.sites if site.is_buildable(self.start_side)]
        match type:
            case SiteType.TOWER:
                self.sites = [site for site in self.sites if site.dist_to(Params.CENTER) <= Params.MAX_TOWER_DIST]
            case SiteType.BARRACKS:
                self.sites = [site for site in self.sites
                              if Params.MAX_TOWER_DIST < site.dist_to(Params.CENTER) <= Params.MAX_BARRACKS_DIST]
            case SiteType.MINE:
                self.sites = [site for site in self.sites if Params.MAX_BARRACKS_DIST < site.dist_to(Params.CENTER)]
            case _:
                raise Exception("Invalid type")
        return self
    
    def get(self) -> list[Site]:
        return self.sites
    
    def get_closest_to(self, pos):
        if sites := sorted(self.sites, key=lambda site: site.dist_to(pos)):
            return sites[0]
        else: return None

    def __repr__(self) -> str:
        return f"SitesAccessBuilder [sites = {self.sites}]"
    