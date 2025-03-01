from sites.SitesAccessBuilder import SitesAccessBuilder
from owner.Owner import Owner
from sites.SiteType import SiteType
from sites.SitesManager import SitesManager
from sites.Site import Site
from units.Unit import Unit
from units.UnitType import UnitType
from units.UnitsAccessBuilder import UnitsAccessBuilder
from units.UnitsManager import UnitsManager

print()

site = Site(1, [2, 3], 4)
print("site", site)
SM = SitesManager({site.id: site})
print("SM", SM)
sab: SitesAccessBuilder = SM.sites
print("sab", sab)

print()

unit = Unit([1, 2], UnitType.QUEEN, Owner.FRIEND, 3)
print("unit", unit)
UM = UnitsManager([unit])
print("UM", UM)
uab: UnitsAccessBuilder = UM.units
print("uab", uab)

print()

SM.save_start_side(UM.units.my_queen.pos)
print(SM)

print()

print("WAIT")
print("TRAIN")

print()
