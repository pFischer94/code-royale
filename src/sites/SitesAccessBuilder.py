from owner.Owner import Owner
from sites.Site import Site

class SitesAccessBuilder:
    def __init__(self, sites: list[Site]):
        self.sites: list[Site] = sites
    
    # @property
    # def friendly(self) -> list[Site]:
    #     return [site for site in self.sites if site.owner == Owner.FRIENDLY]
    
    # @property
    # def enemy(self) -> list[Site]:
    #     return [site for site in self.sites if site.owner == Owner.ENEMY]
    
    # def get(self) -> list[Site]:
    #     return self.sites
    
    def __repr__(self) -> str:
        return f"SitesAccessBuilder [sites = {self.sites}]"
    