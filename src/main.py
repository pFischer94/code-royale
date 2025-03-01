import sys

from game.GameManager import GameManager
from params import Params
from sites.Side import Side
from sites.SitesManager import SitesManager
from units.UnitsManager import UnitsManager

# python3 merger.py; Get-Content output/src.py | Set-Clipboard

GM = GameManager()

while True:
    GM.update()
    GM.build()
    GM.train()
    
    # find BUILD action
        # save 3 
        # one knights barrack, TRAIN once
        # 3 mines, dont upgrade
        # 4 towers in middle, dont upgrade
        
        # save for huge wave
    
    # find TRAIN action

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)
    # First line: A valid queen action
    # Second line: A set of training instructions
