from src.sites.SitesAccessBuilder import SitesAccessBuilder
from src.owner.Owner import Owner
from src.sites.SiteType import SiteType
from src.sites.SitesManager import SitesManager
from src.sites.Site import Site
from src.units.Unit import Unit
from src.units.UnitType import UnitType

print()

site = Site(1, [2, 3], 4)
print("site", site)

SM = SitesManager(site)
print("sm", SM)

sab: SitesAccessBuilder = SitesAccessBuilder([site])
print("sab", sab)
print("sab.sites", sab.sites)
print("sab.sites[0]", sab.sites[0])
print("sab.sites[0].pos", sab.sites[0].pos)

print()
