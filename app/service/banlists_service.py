from app.crud.banlists_crud import find_banlists_by_type as find_banlists_by_type_crud, insert_banlist as insert_banlist_crud, find_banlist as find_banlist_crud, update_banlist as update_banlist_crud, delete_banlist as delete_banlist_crud

def find_banlists(type="BAN"):
    banlists = find_banlists_by_type_crud(type)
    banlists_dict = {}
    for banlist in banlists:
        banlists_dict[banlist["name"]] = banlist["cards"]
    return banlists_dict

def find_banlist(name, type):
    return find_banlist_crud(name, type)

def find_detailed_banlists(type="BAN"):
    banlists = find_banlists_by_type_crud(type)
    return banlists

def create_or_update_banlist(name, type, cards, maxQuantityPerDeck=None):
    if not type or not name:
        raise ValueError("Banlist name and type are required.")
    
    banlist = find_banlist(name, type)
    if banlist:
        banlist["name"] = name
        banlist["type"] = type
        if cards:
            banlist["cards"] = cards
        if maxQuantityPerDeck:
            banlist["maxQuantityPerDeck"] = maxQuantityPerDeck
        update_banlist_crud(name, type, banlist)
    else:
        banlist = create_banlist(name, type, cards, maxQuantityPerDeck)

def delete_banlist(name, type):
    delete_banlist_crud(name, type)

def create_banlist(name, type, cards, maxQuantityPerDeck):
    if not maxQuantityPerDeck:
            maxQuantityPerDeck = get_default_max_quantity_per_deck(type)

    banlist = {
        "name": name,
        "type": type,
        "cards": cards,
        "maxQuantityPerDeck": maxQuantityPerDeck
    }
    insert_banlist_crud(banlist)
    return banlist

def get_default_max_quantity_per_deck(type):
    if type == "BAN":
        return 0
    elif type == "LIMITED":
        return 1
    elif type == "SEMI_LIMITED":
        return 2
    return None