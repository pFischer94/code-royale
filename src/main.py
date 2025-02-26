import sys

from params import Params
from sites.Side import Side
from sites.SitesManager import SitesManager
from units.UnitsManager import UnitsManager

SM = SitesManager.from_input()
input()
SM.update_from_input()
um = UnitsManager.from_input()

SM.save_start_side(um.units.my_queen.pos)

# TODO: implement these methods
print(f"BUILD {SM.sites.next_barracks_to_build(um.units.my_queen.pos).id} BARRACKS-KNIGHT")
print("TRAIN")

while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    
    SM.update_from_input()
    um = UnitsManager.from_input()
    
    if SM.start_side == Side.UNKNOWN:
        SM.start_side = Side.RIGHT if um.units.my_queen.pos[0] >= Params.MIDDLE[0] else Side.LEFT

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
    if next_barracks := SM.sites.next_barracks_to_build(um.units.my_queen.pos):
        print(f"BUILD {next_barracks.id} BARRACKS-KNIGHT")
    else:
        print("WAIT")
    print("TRAIN")





while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    
    update_sites(sites)
    friendly_sites = FriendlySites(sites)
    # print(friendly_sites, file=sys.stderr, flush=True)

    units = update_units()
    my_queen, enemy_queen, center_of_towers = get_queens(units, center_of_towers)
    
    build_id = find_closest_safely_buildable_site_id(sites, my_queen.pos)
    build_string = get_build_string(build_id, friendly_sites)
    print(build_string)
    
    train_ids: list[int] = find_n_closest_available_barracks(int(gold / 80), sites, enemy_queen.pos)
    train_str: str = ""
    for id in train_ids:
        train_str += " " + str(id)
    print(f"TRAIN{train_str}")
    