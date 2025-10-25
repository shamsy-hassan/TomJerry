# ============================================================
# File: backend/api/auth.py
# Description:
#     Handles authentication for the Tom & Jerry backend.
#     Includes player registration, login, and token verification.
#     Uses JWT tokens for session management.
# ============================================================

from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from backend.database.db import get_db
from backend.models.player_model import Player
import jwt
import datetime
from backend.config import Config
SECRET_KEY = Config.SECRET_KEY


# ============================================================
# 1. BLUEPRINT SETUP
# ------------------------------------------------------------
# Blueprint allows this authentication module to be registered
# separately in the Flask app (modular organization).
# ============================================================
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# ============================================================
# 2. HELPER FUNCTION: GENERATE JWT TOKEN
# ------------------------------------------------------------
# A reusable function to create a signed token that contains:
#  - player ID
#  - expiration time (default: 24 hours)
# ============================================================
def generate_token(player_id):
    token = jwt.encode(
        {
            "player_id": player_id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm="HS256"
    )
    return token


# ============================================================
# 3. ROUTE: REGISTER NEW PLAYER
# ------------------------------------------------------------
# Endpoint: POST /api/auth/register
# Purpose : Register a new player with username & password.
# Example Payload:
# {
#   "username": "TomHero",
#   "password": "12345",
#   "avatar": "tom.png"
# }
# ============================================================
@auth_bp.route("/register", methods=["POST"])
def register():
    db = get_db()
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")
    avatar = data.get("avatar", "default.png")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Check if username exists
    existing_user = db.query(Player).filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "Username already taken"}), 409

    # Hash password before saving
    hashed_pw = generate_password_hash(password)

    new_player = Player(username=username, password=hashed_pw, avatar=avatar)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    token = generate_token(new_player.id)

    return jsonify({
        "message": "Registration successful",
        "player": new_player.to_dict(),
        "token": token
    }), 201


# ============================================================
# 4. ROUTE: LOGIN PLAYER
# ------------------------------------------------------------
# Endpoint: POST /api/auth/login
# Purpose : Authenticate player using username and password.
# Example Payload:
# {
#   "username": "TomHero",
#   "password": "12345"
# }
# ============================================================
@auth_bp.route("/login", methods=["POST"])
def login():
    db = get_db()
    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    player = db.query(Player).filter_by(username=username).first()

    if not player or not check_password_hash(player.password, password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_token(player.id)

    return jsonify({
        "message": "Login successful",
        "player": player.to_dict(),
        "token": token
    }), 200


# ============================================================
# 5. ROUTE: VERIFY TOKEN
# ------------------------------------------------------------
# Endpoint: GET /api/auth/verify
# Purpose : Check if the provided JWT token is still valid.
# Usage   : Sent from frontend for auto-login/session restore.
# ============================================================
@auth_bp.route("/verify", methods=["GET"])
def verify_token():
    token = request.headers.get("Authorization")

    if not token:
        return jsonify({"error": "Token missing"}), 401

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"valid": True, "player_id": decoded["player_id"]}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401


# ============================================================
# 6. ROUTE: LOGOUT PLAYER
# ------------------------------------------------------------
# Endpoint: POST /api/auth/logout
# Purpose : For frontend use only — client removes stored token.
# Note    : No server-side session is kept since we use JWT.
# ============================================================
@auth_bp.route("/logout", methods=["POST"])
def logout():
    return jsonify({"message": "Logout successful (token discarded client-side)"}), 200
