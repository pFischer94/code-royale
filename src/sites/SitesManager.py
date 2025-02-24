from sites.SitesAccessBuilder import SitesAccessBuilder
from sites.Site import Site
from owner.Owner import Owner

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
