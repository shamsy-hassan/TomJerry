# ============================================================
# File: backend/api/game_routes.py
# Description:
#     Defines REST API routes for managing game sessions,
#     handling player moves, and updating in-game state.
#     Works in coordination with socket events for real-time
#     updates.
# ============================================================

from flask import Blueprint, jsonify, request
from backend.database.db import get_db
from backend.models.game_model import Game
from backend.models.player_model import Player
from backend.models.score_model import Score
from datetime import datetime

# ============================================================
# 1. BLUEPRINT SETUP
# ------------------------------------------------------------
# The "game" blueprint isolates all routes that deal with
# creating, updating, or ending game sessions.
# ============================================================
game_bp = Blueprint("game", __name__, url_prefix="/api/game")


# ============================================================
# 2. ROUTE: START NEW GAME
# ------------------------------------------------------------
# Endpoint: POST /api/game/start
# Purpose : Creates a new game session between players.
# Example Payload:
# {
#   "player1_id": 1,
#   "player2_id": 2,
#   "map": "house"
# }
# ============================================================
@game_bp.route("/start", methods=["POST"])
def start_game():
    db = get_db()
    data = request.get_json()

    player1_id = data.get("player1_id")
    player2_id = data.get("player2_id")
    map_name = data.get("map", "default")

    if not player1_id or not player2_id:
        return jsonify({"error": "Both player1_id and player2_id are required"}), 400

    # Ensure both players exist
    player1 = db.query(Player).filter_by(id=player1_id).first()
    player2 = db.query(Player).filter_by(id=player2_id).first()
    if not player1 or not player2:
        return jsonify({"error": "One or both players not found"}), 404

    # Create new game record
    new_game = Game(
        player1_id=player1_id,
        player2_id=player2_id,
        map_name=map_name,
        start_time=datetime.utcnow(),
        status="active"
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)

    return jsonify({
        "message": "New game started",
        "game": new_game.to_dict()
    }), 201


# ============================================================
# 3. ROUTE: SUBMIT PLAYER MOVE
# ------------------------------------------------------------
# Endpoint: POST /api/game/move
# Purpose : Receives and stores a player move during gameplay.
# Example Payload:
# {
#   "game_id": 1,
#   "player_id": 2,
#   "move": "jump"
# }
# ============================================================
@game_bp.route("/move", methods=["POST"])
def player_move():
    db = get_db()
    data = request.get_json()

    game_id = data.get("game_id")
    player_id = data.get("player_id")
    move = data.get("move")

    if not game_id or not player_id or not move:
        return jsonify({"error": "game_id, player_id, and move are required"}), 400

    game = db.query(Game).filter_by(id=game_id).first()
    if not game or game.status != "active":
        return jsonify({"error": "Game not found or not active"}), 404

    # Store or process move (for simplicity we just log it)
    if not hasattr(game, "moves"):
        game.moves = []
    game.moves.append({"player_id": player_id, "move": move})

    db.commit()
    return jsonify({"message": "Move recorded"}), 200


# ============================================================
# 4. ROUTE: END GAME
# ------------------------------------------------------------
# Endpoint: POST /api/game/end
# Purpose : Ends a game session and records scores.
# Example Payload:
# {
#   "game_id": 1,
#   "winner_id": 2,
#   "points": 100
# }
# ============================================================
@game_bp.route("/end", methods=["POST"])
def end_game():
    db = get_db()
    data = request.get_json()

    game_id = data.get("game_id")
    winner_id = data.get("winner_id")
    points = data.get("points", 0)

    game = db.query(Game).filter_by(id=game_id).first()
    if not game:
        return jsonify({"error": "Game not found"}), 404

    # Mark game as finished
    game.status = "finished"
    game.end_time = datetime.utcnow()

    # Record winner’s score
    score = Score(
        player_id=winner_id,
        game_id=game_id,
        points=points
    )
    db.add(score)
    db.commit()
    db.refresh(score)

    return jsonify({
        "message": "Game ended successfully",
        "winner_id": winner_id,
        "score": score.to_dict()
    }), 200


# ============================================================
# 5. ROUTE: FETCH ALL ACTIVE GAMES
# ------------------------------------------------------------
# Endpoint: GET /api/game/active
# Purpose : Retrieves all ongoing game sessions.
# ============================================================
@game_bp.route("/active", methods=["GET"])
def get_active_games():
    db = get_db()
    active_games = db.query(Game).filter_by(status="active").all()
    return jsonify([g.to_dict() for g in active_games])


# ============================================================
# 6. ROUTE: FETCH GAME BY ID
# ------------------------------------------------------------
# Endpoint: GET /api/game/<int:game_id>
# Purpose : Retrieves detailed info for one specific game.
# ============================================================
@game_bp.route("/<int:game_id>", methods=["GET"])
def get_game(game_id):
    db = get_db()
    game = db.query(Game).filter_by(id=game_id).first()
    if not game:
        return jsonify({"error": "Game not found"}), 404
    return jsonify(game.to_dict())
