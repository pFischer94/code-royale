import sys

from game.PlanStrategy import PlanStrategy
from game.ReactStrategy import ReactStrategy
from game.OldStrategy import OldStrategy
from params import Params
from sites.Side import Side
from sites.SitesManager import SitesManager
from units.UnitsManager import UnitsManager


GM = OldStrategy()

while True:
    GM.update()
    GM.build()
    GM.train()
        
# python3 merger.py; Get-Content output/src.py | Set-Clipboard
# To debug: print("Debug messages...", file=sys.stderr, flush=True)
