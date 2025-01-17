from flask import Flask, request, jsonify, Blueprint
from app.crud.trunk_crud import TrunkCRUD
from app.auth import user_required, admin_required, login_user
from app.card_search import search_card_by_id, search_cards_by_ids
from app.db_config import Config
from app.models.trunk import Trunk
from app.service.banlists_service import find_banlists, find_banlist, find_detailed_banlists,create_or_update_banlist, delete_banlist

app = Flask(__name__)

# Initialize TrunkCRUD
trunk_crud = TrunkCRUD(Config.MONGO_URI, Config.MONGO_DBNAME, "trunks")

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Hello, Flask!"

### Helper Methods ###

def normalize_deck_type(deck_type):
    """Normalize deck type."""
    deck_type = deck_type.lower()
    if deck_type in ["trunk", "main", "side", "extra"]:
        return deck_type + "_deck"
    return deck_type

def is_card_quantity_allowed(deck, deck_type):
    """Check if a deck exceeds the maximum number of cards."""
    if deck_type == "main_deck" and sum(deck.values()) > 60:
        return False, "Main deck cannot exceed 60 cards."
    if deck_type in ["side_deck", "extra_deck"] and sum(deck.values()) > 15:
        return False, "Side and Extra decks cannot exceed 15 cards."
    return True, ""

### USER ROUTES ###

@main.route('/detail_card', methods=['GET'])
@user_required
def detail_card():
    """
    Detail a card by id
    Example:
    curl --location 'http://localhost:5000/detail_card?id=73262676' \
    --header 'Authorization: Basic ****'
    """

    card_id = request.args.get('id')
    if not card_id:
        return jsonify({"error": "Missing 'id' parameter"}), 400
    
    card = search_card_by_id(card_id)
    if not card:
        return jsonify({"error": "Card not found"}), 404
    return jsonify(card), 200

@main.route('/detail_cards', methods=['GET'])
@user_required
def detail_cards():
    """
    Detail a cards by ids
    Example:
    curl --location 'http://localhost:5000/detail_cards?ids=73262676,9999999' \
    --header 'Authorization: Basic ****'
    """
    card_ids = request.args.get('ids')
    if not card_ids:
        return jsonify({"error": "Missing 'ids' parameter"}), 400
    
    card_ids = card_ids.split(',')
    cards = search_cards_by_ids(card_ids)

    if not cards:
        return jsonify({"error": "Cards not found"}), 404
    
    cards = [card.to_dict() for card in cards]

    return jsonify(cards), 200

@main.route('/banned', methods=['GET'])
@user_required
def get_banned():
    """
    Get banned cards lists
    Example:
    curl --location --request GET 'http://localhost:5000/banned' \
    --header 'Authorization: Basic ****'
    """
    return jsonify(find_banlists("BAN")), 200

@main.route('/semi_limited', methods=['GET'])
@user_required
def get_semi_limited():
    """
    Get semi-limited cards lists
    Example:
    curl --location --request GET 'http://localhost:5000/semi_limited' \
    --header 'Authorization: Basic ****'
    """
    return jsonify(find_banlists("SEMI_LIMITED")), 200

@main.route('/limited', methods=['GET'])
@user_required
def get_limited():
    """
    Get limited cards lists
    Example:
    curl --location --request GET 'http://localhost:5000/limited' \
    --header 'Authorization: Basic ****'
    """
    return jsonify(find_banlists("LIMITED")), 200

@main.route('/detailed_banlist', methods=['GET'])
@user_required
def get_detailed_banlists():
    """
    Get detailed banlists
    Name is optional, if not informed will return all banlists of informed type
    Example:
    curl --location --request GET 'http://localhost:5000/detailed_banlist?name=TCG%20Banlist&type=BAN' \
    --header 'Authorization: Basic ****'
    """

    # not implemented yet
    return jsonify({"error": "Not implemented yet"}), 501

    name = request.args.get('name')
    type = request.args.get('type')
    if not type:
        return jsonify({"error": "Missing 'type' parameter"}), 400
    
    if name:
        banlist = find_banlist(name, type)
        if not banlist:
            return jsonify({"error": "Banlist not found"}), 404
        banlist['_id'] = str(banlist['_id'])
        return jsonify(banlist), 200
    else:
        banlists = find_detailed_banlists(type)
        # fix _id to be a string
        for banlist in banlists:
            banlist['_id'] = str(banlist['_id'])
        return jsonify(banlists), 200

@main.route('/get_trunk', methods=['GET'])
@user_required
def get_trunk():
    """
    Route to return a user's trunk.
    Example:
    curl --location --request GET 'http://localhost:5000/get_trunk?username=player1' \
    --header 'Authorization: Basic ****'
    """
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Missing 'username' parameter"}), 400
    
    trunk = trunk_crud.get_trunk_by_username(username)
    if not trunk:
        return jsonify({"error": "Trunk not found"}), 404
    
    trunk = Trunk.from_dict(trunk)
    trunk = trunk.to_dict()
    return jsonify(trunk), 200

@main.route('/get_detailed_trunk', methods=['GET'])
@user_required
def get_detailed_trunk():
    """
    Route to return a user's trunk with card details.
    Example:
    curl --location --request GET 'http://localhost:5000/get_detailed_trunk?username=player1' \
    --header 'Authorization: Basic ****'
    """
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Missing 'username' parameter"}), 400
    
    trunk = trunk_crud.get_trunk_by_username(username)
    if not trunk:
        return jsonify({"error": "Trunk not found"}), 404
    
    trunk = Trunk.from_dict(trunk)
    trunk = trunk.to_dict()
    cards_ids = []
    
    for deck_type in ["trunk_deck", "main_deck", "side_deck", "extra_deck"]:
        cards_ids.extend(set(trunk[deck_type].keys()))
    
    print("cards_ids:", cards_ids)

    cards = search_cards_by_ids(cards_ids)
    print('cards before:', cards)
    cards = [card.to_dict() for card in cards]

    print('cards:', cards)
    return jsonify({"trunk": trunk, "cards": cards}), 200

@main.route('/move_card', methods=['PATCH'])
@user_required
def move_card():
    """
    Route to move a card between decks.
    Example:
    curl --location --request PATCH 'http://localhost:5000/move_card' \
    --header 'Content-Type: application/json' \
    --header 'Authorization: Basic ***' \
    --data '{
        "source_deck": "main",
        "destination_deck": "side",
        "card_id": 9999999,
        "quantity": 1,
        "username": "boloplayer"
    }'
    """
    data = request.json
    if 'source_deck' not in data or 'destination_deck' not in data or 'card_id' not in data or 'quantity' not in data or 'username' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    username = data['username']
    source_deck = data['source_deck']
    source_deck = normalize_deck_type(source_deck)
    destination_deck = data['destination_deck']
    destination_deck = normalize_deck_type(destination_deck)
    card_id = data['card_id']
    card_id = str(card_id)
    quantity = data['quantity']
    quantity = int(quantity)

    trunk = trunk_crud.get_trunk_by_username(username)
    if not trunk:
        return jsonify({"error": "Trunk not found"}), 404

    trunk = Trunk.from_dict(trunk)
    trunk.move_cards(card_id, quantity, source_deck, destination_deck)
    trunk = trunk.to_dict()

    valid, message = is_card_quantity_allowed(trunk[source_deck], source_deck)
    if not valid:
        return jsonify({"error": message}), 400
    
    valid, message = is_card_quantity_allowed(trunk[destination_deck], destination_deck)
    if not valid:
        return jsonify({"error": message}), 400

    trunk_crud.update_trunk(username, trunk)
    return jsonify({"message": f"Moved {quantity} of card {card_id} from {source_deck} to {destination_deck}."}), 200

@main.route('/login', methods=['POST'])
def login():
    """
    Route to login a user.
    Example:
    curl --location --request POST 'http://localhost:5000/login' \
    --header 'Content-Type: application/json' \
    --data '{
        "username": "player1",
        "password": "password
    }'
    """
    # this method should check on users database and if login is valid, return a basic token representing the login:password
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({"error": "Missing required parameters"}), 400
    
    token = login_user()
    if not token:
        return jsonify({"error": "Invalid username or password"}), 401
    return jsonify({"token": token}), 200

### ADMIN ROUTES ###

@main.route('/admin/create_trunk', methods=['POST'])
@admin_required
def create_trunk():
    """Route to create a new trunk."""
    data = request.json
    if 'username' not in data:
        return jsonify({"error": "Missing 'username' parameter"}), 400

    trunk_crud.create_trunk(data['username'])
    return jsonify({"message": "Trunk created successfully."}), 201

@main.route('/admin/delete_trunk', methods=['DELETE'])
@admin_required
def delete_trunk():
    """Route to delete a user's trunk."""
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Missing 'username' parameter"}), 400

    trunk_crud.delete_trunk(username)
    return jsonify({"message": f"Trunk for {username} deleted."}), 200

@main.route('/admin/update_trunk', methods=['PATCH'])
@admin_required
def update_trunk():
    """Route to update a trunk."""
    data = request.json
    print('data:', data)
    if 'username' not in data:
        return jsonify({"error": "Cannot update without a username"}), 400
    
    if 'new_username' not in data and 'trunk_deck' not in data and 'main_deck' not in data and 'side_deck' not in data and 'extra_deck' not in data:
        return jsonify({"error": "Missing required parameters"}), 400
    
    trunk = trunk_crud.get_trunk_by_username(data['username'])

    if not trunk:
        return jsonify({"error": "Trunk not found"}), 404
    
    for key in data:
        if key in trunk:
            trunk[key] = data[key]
    
    trunk_crud.update_trunk(data['username'], trunk)
    return jsonify({"message": f"Trunk for {data['username']} updated."}), 200

@main.route('/admin/add_card', methods=['PATCH'])
@admin_required
def add_card():
    """Route to add a card to a user's trunk."""
    data = request.json
    if 'username' not in data or 'card_id' not in data or 'quantity' not in data or 'deck_type' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    trunk = trunk_crud.get_trunk_by_username(data['username'])
    if not trunk:
        return jsonify({"error": "Trunk not found"}), 404

    deck_type = data['deck_type']
    deck_type = normalize_deck_type(deck_type)
    card_id = data['card_id']
    quantity = data['quantity']
    quantity = int(quantity)

    trunk[deck_type][card_id] = trunk[deck_type].get(card_id, 0) + quantity

    valid, message = is_card_quantity_allowed(trunk[deck_type], deck_type)
    if not valid:
        return jsonify({"error": message}), 400

    trunk_crud.update_trunk(data['username'], trunk)
    return jsonify({"message": f"Added {quantity} of card {card_id} to {deck_type}."}), 200

@main.route('/admin/remove_card', methods=['PATCH'])
@admin_required
def remove_card():
    """Route to remove a card from a user's trunk."""
    data = request.json
    if 'username' not in data or 'card_id' not in data or 'quantity' not in data or 'deck_type' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    trunk = trunk_crud.get_trunk_by_username(data['username'])
    if not trunk:
        return jsonify({"error": "Trunk not found"}), 404

    deck_type = data['deck_type']
    deck_type = normalize_deck_type(deck_type)
    card_id = data['card_id']
    card_id = str(card_id)
    quantity = data['quantity']
    quantity = int(quantity)

    if card_id in trunk[deck_type]:
        trunk[deck_type][card_id] =- int(quantity)
        if trunk[deck_type][card_id] <= 0:
            del trunk[deck_type][card_id]
        
        # validation for less than 40 cards in main deck
        #if deck_type == "main_deck" and sum(trunk[deck_type].values()) < 40:
        #    return jsonify({"error": "Main deck must contain at least 40 cards."}), 400

        trunk_crud.update_trunk(data['username'], trunk)
        return jsonify({"message": f"Removed {quantity} of card {card_id} from {deck_type}."}), 200
    else:
        return jsonify({"error": "Card not found in the specified deck."}), 404

@main.route('/admin/create_banlist', methods=['POST'])
@admin_required
def create_banlist():
    """Route to create a new banlist."""
    data = request.json
    if 'name' not in data or 'type' not in data or 'cards' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    name = data['name']
    type = data['type']
    cards = data['cards']
    maxQuantityPerDeck = data.get('maxQuantityPerDeck')

    if (find_banlist(name, type)):
        return jsonify({"error": "Banlist already exists"}), 400
    
    create_or_update_banlist(name, type, cards, maxQuantityPerDeck)
    created_banlist = find_banlist(name, type)
    created_banlist['_id'] = str(created_banlist['_id'])
    return jsonify(created_banlist), 201

@main.route('/admin/update_banlist', methods=['PATCH'])
@admin_required
def update_banlist():
    """Route to update a banlist."""
    data = request.json
    if 'name' not in data or 'type' not in data or 'cards' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    name = data['name']
    type = data['type']
    cards = data['cards']
    maxQuantityPerDeck = data.get('maxQuantityPerDeck')

    create_or_update_banlist(name, type, cards, maxQuantityPerDeck)
    updated_banlist = find_banlist(name, type)
    updated_banlist['_id'] = str(updated_banlist['_id'])
    return jsonify(updated_banlist), 200

@main.route('/admin/delete_banlist', methods=['DELETE'])
@admin_required
def delete_banlist_route():
    """Route to delete a banlist."""
    name = request.args.get('name')
    type = request.args.get('type')
    if not name or not type:
        return jsonify({"error": "Missing required parameters"}), 400

    delete_banlist(name, type)
    return jsonify({"message": f"Banlist {name} deleted."}), 200