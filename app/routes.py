from flask import Flask, request, jsonify, Blueprint
from app.models.deck import Deck
from app.models.trunk import Trunk
from .trunk_utils import move_card_from_deck_to_trunk, move_card_from_trunk_to_deck, move_card_deck_to_deck
from app.crud.trunk_crud import TrunkCRUD
from app.auth import user_required, admin_required
from app.card_search import search_card_by_id, search_card_by_name
from app.models.card import Card

app = Flask(__name__)

# Initialize TrunkCRUD
trunk_crud = TrunkCRUD()

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return "Hello, Flask!"

### USER ROUTES ###

@main.route('/get_card', methods=['GET'])
@user_required
def get_card():
    """Route to return an card by id or name."""
    card_id = request.args.get('id')
    card_name = request.args.get('name')
    if not card_id and not card_name:
        return jsonify({"error": "Missing 'id' or 'name' parameter"}), 400
    
    if card_id:
        card = search_card_by_id(card_id)
        print("CARD", card)
        if not card:
            return jsonify({"error": "Card not found"}), 404
        card = Card.from_dict(card)
        card = card.to_dict()
        return jsonify(card), 200
    
    card = search_card_by_name(card_name)
    if not card:
        return jsonify({"error": "Card not found"}), 404
    card = Card.from_dict(card)
    card = card.to_dict()
    return jsonify(card), 200

@main.route('/get_trunk', methods=['GET'])
@user_required
def get_trunk():
    """Route to return a user's trunk."""
    username = request.args.get('username')
    if not username:
        return jsonify({"error": "Missing 'username' parameter"}), 400
    
    trunk = trunk_crud.get_trunk_by_username(username)
    if not trunk:
        return jsonify({"error": "Trunk not found"}), 404
    
    return jsonify(trunk.to_detailed_dict()), 200

@main.route('/move_card_to_trunk', methods=['POST'])
@user_required
def move_card_to_trunk():
    data = request.json
    if 'deck_type' not in data or 'card_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    deck_type = data['deck_type']
    card_id = data['card_id']
    quantity = data['quantity']
    username = username=data['username']

    trunk = trunk_crud.get_trunk_by_username(username)
    deck = trunk.deck

    move_card_from_deck_to_trunk(deck, deck_type, trunk, card_id, quantity)
    trunk_crud.update_trunk(trunk, username)

    return jsonify({"message": f"Moved {quantity} of card {card_id} from deck to trunk."}), 200

@main.route('/move_card_to_deck', methods=['POST'])
@user_required
def move_card_to_deck():
    data = request.json
    if 'deck_type' not in data or 'card_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    deck_type = data['deck_type']
    card_id = data['card_id']
    quantity = data['quantity']
    username = data['username']

    trunk = trunk_crud.get_trunk_by_username(username)
    deck = trunk.deck

    move_card_from_trunk_to_deck(deck, deck_type, trunk, card_id, quantity)
    trunk_crud.update_trunk(trunk, username)

    return jsonify({"message": f"Moved {quantity} of card {card_id} from trunk to deck."}), 200

@main.route('/move_card_deck_to_deck', methods=['POST'])
@user_required
def move_card_deck_to_deck():
    data = request.json
    if 'deck_type' not in data or 'card_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    deck_type = data['deck_type']
    card_id = data['card_id']
    quantity = data['quantity']
    username = data['username']

    trunk = trunk_crud.get_trunk_by_username(username)
    deck = trunk.deck

    move_card_deck_to_deck(deck, deck_type, card_id, quantity)
    trunk_crud.update_trunk(trunk, username)

    return jsonify({"message": f"Moved {quantity} of card {card_id} from deck to deck."}), 200


### ADMIN ROUTES ###

@main.route('/admin/create_trunk', methods=['POST'])
@admin_required
def create_trunk():
    """Route to create a new trunk."""
    print('user autenticated')
    print('request:', request.json)
    data = request.json
    if 'username' not in data:
        return jsonify({"error": "Missing 'username' parameter"}), 400
    
    print('user autenticated and username is:', data['username'])
    new_trunk = Trunk(username=data['username'])
    success, message = trunk_crud.create_trunk(new_trunk)
    if success:
        return jsonify({"message": message}), 201
    return jsonify({"error": message}), 400

@main.route('/admin/add_card', methods=['POST'])
@admin_required
def add_card():
    """Route to add a card to a user's trunk."""

    data = request.json
    if 'username' not in data or 'card_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing required parameters"}), 400
    
    trunk_crud.add_card_to_trunk(username=data['username'], card_id=data['card_id'], quantity=data['quantity'])
    return jsonify({"message": f"Added {data['quantity']} of card {data['card_id']} to {data['username']}'s trunk."}), 200

@main.route('/admin/remove_card', methods=['POST'])
@admin_required
def remove_card():
    """Route to remove a card from a user's trunk."""

    data = request.json
    if 'username' not in data or 'card_id' not in data or 'quantity' not in data:
        return jsonify({"error": "Missing required parameters"}), 400

    trunk_crud.remove_card_from_trunk(username=data['username'], card_id=data['card_id'], quantity=data['quantity'])
    return jsonify({"message": f"Removed {data['quantity']} of card {data['card_id']} from {data['username']}'s trunk."}), 200

@main.route('/admin/delete_trunk', methods=['POST'])
@admin_required
def delete_trunk():
    """Route to delete a user's trunk."""

    data = request.json
    if 'username' not in data:
        return jsonify({"error": "Missing 'username' parameter"}), 400

    trunk_crud.delete_trunk(username=data['username'])
    return jsonify({"message": f"Trunk for {data['username']} deleted."}), 200