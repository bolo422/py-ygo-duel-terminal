from app.db_config import Config

banlists_collection = Config.banlists_collection

def find_banlist(banlist_name, banlist_type):
    """Search for a banlist in the database by its name and type."""
    return banlists_collection.find_one({"name": banlist_name, "type": banlist_type})

def find_banlists_by_type(banlist_type):
    """Search for banlists in the database by their type."""
    return banlists_collection.find({"type": banlist_type})

def insert_banlist(banlist):
    """Insert a banlist into the database."""
    if not find_banlist(banlist["name"], banlist["type"]):
        banlists_collection.insert_one(banlist)
    
def delete_banlist(banlist_name, banlist_type):
    """Delete a banlist from the database."""
    result = banlists_collection.delete_one({"name": banlist_name, "type": banlist_type})
    if result.deleted_count == 0:
        raise ValueError("Banlist not found.")
    
def update_banlist(banlist_name, banlist_type, updated_banlist):
    """Update a banlist's properties."""
    if not find_banlist(banlist_name, banlist_type):
        raise ValueError("Banlist not found.")
    
    banlists_collection.update_one(
        {"name": banlist_name, "type": banlist_type},
        {"$set": updated_banlist}
    )