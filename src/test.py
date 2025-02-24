from sites.SitesAccessBuilder import SitesAccessBuilder
from owner.Owner import Owner
from sites.SiteType import SiteType
from sites.SitesManager import SitesManager
from sites.Site import Site
from units.Unit import Unit
from units.UnitType import UnitType

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
