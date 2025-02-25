from sites.SitesManager import SitesManager
from units.UnitsManager import UnitsManager

SM = SitesManager.from_input()

while True:
    # touched_site: -1 if none
    gold, touched_site = [int(i) for i in input().split()]
    
    SM.update()
    UM = UnitsManager.from_input()

    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # First line: A valid queen action
    # Second line: A set of training instructions
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
    