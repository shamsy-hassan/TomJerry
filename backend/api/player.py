# ============================================================
# File: backend/api/player.py
# Description: Player API routes for the Tom & Jerry backend.
#              Handles player registration, profile retrieval,
#              and updates via RESTful endpoints.
# ============================================================

from flask import Blueprint, jsonify, request
from backend.database.db import get_db
from backend.models.player_model import Player

# ============================================================
# 1. BLUEPRINT SETUP
# ------------------------------------------------------------
# Blueprints in Flask allow modular route organization.
# Here, we create a dedicated "player" blueprint to handle
# all player-related API routes cleanly.
# ============================================================
player_bp = Blueprint("player", __name__, url_prefix="/api/players")

# ============================================================
# 2. ROUTE: REGISTER PLAYER
# ------------------------------------------------------------
# Endpoint: POST /api/players/register
# Purpose : Create a new player entry in the database.
# Example Payload:
# {
#   "username": "Tom",
#   "avatar": "tom-icon.png"
# }
# ============================================================
@player_bp.route("/register", methods=["POST"])
def register_player():
    db = get_db()
    data = request.get_json()

    username = data.get("username")
    avatar = data.get("avatar", "default.png")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    # Check if username already exists
    existing_player = db.query(Player).filter_by(username=username).first()
    if existing_player:
        return jsonify({"error": "Username already taken"}), 409

    # Create new player instance
    new_player = Player(username=username, avatar=avatar)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    return jsonify({
        "message": "Player registered successfully",
        "player": new_player.to_dict()
    }), 201


# ============================================================
# 3. ROUTE: GET ALL PLAYERS
# ------------------------------------------------------------
# Endpoint: GET /api/players
# Purpose : Retrieve all players currently in the database.
# ============================================================
@player_bp.route("/", methods=["GET"])
def get_players():
    db = get_db()
    players = db.query(Player).all()
    return jsonify([p.to_dict() for p in players])


# ============================================================
# 4. ROUTE: GET SINGLE PLAYER BY ID
# ------------------------------------------------------------
# Endpoint: GET /api/players/<int:player_id>
# Purpose : Retrieve details for a specific player by ID.
# ============================================================
@player_bp.route("/<int:player_id>", methods=["GET"])
def get_player(player_id):
    db = get_db()
    player = db.query(Player).filter_by(id=player_id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404
    return jsonify(player.to_dict())


# ============================================================
# 5. ROUTE: UPDATE PLAYER
# ------------------------------------------------------------
# Endpoint: PUT /api/players/<int:player_id>
# Purpose : Update an existing player's details such as avatar.
# Example Payload:
# {
#   "avatar": "new-avatar.png"
# }
# ============================================================
@player_bp.route("/<int:player_id>", methods=["PUT"])
def update_player(player_id):
    db = get_db()
    player = db.query(Player).filter_by(id=player_id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    data = request.get_json()
    avatar = data.get("avatar")

    if avatar:
        player.avatar = avatar

    db.commit()
    db.refresh(player)
    return jsonify({
        "message": "Player updated successfully",
        "player": player.to_dict()
    }), 200


# ============================================================
# 6. ROUTE: DELETE PLAYER
# ------------------------------------------------------------
# Endpoint: DELETE /api/players/<int:player_id>
# Purpose : Remove a player from the database (optional use).
# ============================================================
@player_bp.route("/<int:player_id>", methods=["DELETE"])
def delete_player(player_id):
    db = get_db()
    player = db.query(Player).filter_by(id=player_id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    db.delete(player)
    db.commit()

    return jsonify({"message": f"Player {player_id} deleted successfully"}), 200
