from src.sites.Site import Site

class SitesAccessBuilder:
    def __init__(self, sites: list[Site]):
        self.sites: list[Site] = sites
    
    def __repr__(self) -> str:
        return f"SitesAccessBuilder [sites = [{self.sites}]]"
    