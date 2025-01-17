from app.db_config import Config
from functools import wraps
from flask import request, jsonify
import base64

users_collection = Config.users_collection

def decode_auth():
    auth = request.headers.get('Authorization')
    if not auth:
        return False, None, None
    auth = auth.split(" ")[1]
    auth = auth.encode('utf-8')
    auth = base64.b64decode(auth).decode('utf-8')
    username, password = auth.split(":")
    return True, username, password

def authenticate_user():
    """Authenticate a user by Authorization header."""
    valid, username, password = decode_auth()
    if not valid:
        return False
    user = users_collection.find_one({"username": username})
    return user["password"] == password

def login_user():
    """Authenticate a user by username and password. Return Authorization token if valid."""
    username = request.json.get("username")
    password = request.json.get("password")
    user = users_collection.find_one({"username": username})
    # if user is valid, return the basic token. If not valid return None
    if user and user["password"] == password:
        return "Basic " + base64.b64encode(f"{username}:{password}".encode('utf-8')).decode('utf-8')
    return None

def authenticate_adm():
    """Authenticate a user by Authorization header, but retruns true only if the user is an admin."""
    valid, username, password = decode_auth()
    if not valid:
        return False
    user = users_collection.find_one({"username": username})
    if user and user["password"] == password:
        return user["privelage"] == "ADM"
    return False

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not authenticate_user():
            return jsonify({"error": "Invalid username or password"}), 403
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not authenticate_adm():
            return jsonify({"error": "Invalid username or password"}), 403
        return f(*args, **kwargs)
    return decorated_function
