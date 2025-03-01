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
    