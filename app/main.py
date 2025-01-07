from pymongo import MongoClient
from flask import Flask, render_template
from models.card import Card
from config import Config

app = Flask(__name__)

# Connect to MongoDB
collection = Config.cards_collection

@app.route('/')
def index():
    # Fetch all cards from the database
    cards_data = collection.find()
    cards = [Card.from_dict(card) for card in cards_data]
    return render_template('index.html', cards=cards)

if __name__ == "__main__":
    app.run(debug=True)
