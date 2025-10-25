# ============================================================
# File: backend/api/leaderboard.py
# Description:
#     Provides endpoints to manage and retrieve leaderboard
#     data such as top player rankings, recent scores, and
#     game performance statistics.
# ============================================================

from flask import Blueprint, jsonify
from backend.database.db import get_db
from backend.models.score_model import Score
from backend.models.player_model import Player
from sqlalchemy import func, desc

# ============================================================
# 1. BLUEPRINT SETUP
# ------------------------------------------------------------
# The "leaderboard" blueprint groups all routes related to
# ranking, scores, and historical game stats.
# ============================================================
leaderboard_bp = Blueprint("leaderboard", __name__, url_prefix="/api/leaderboard")


# ============================================================
# 2. ROUTE: GET TOP PLAYERS
# ------------------------------------------------------------
# Endpoint: GET /api/leaderboard/top
# Purpose : Retrieves top 10 players ranked by total points.
# ------------------------------------------------------------
# Example Response:
# [
#   {"player_id": 1, "username": "TomHero", "total_points": 350},
#   {"player_id": 2, "username": "JerryKing", "total_points": 270},
#   ...
# ]
# ============================================================
@leaderboard_bp.route("/top", methods=["GET"])
def get_top_players():
    db = get_db()

    # Aggregate total points for each player and sort descending
    top_players = (
        db.query(
            Player.id.label("player_id"),
            Player.username,
            func.sum(Score.points).label("total_points")
        )
        .join(Score, Player.id == Score.player_id)
        .group_by(Player.id)
        .order_by(desc("total_points"))
        .limit(10)
        .all()
    )

    # Convert query result into dictionary format for JSON
    result = [
        {
            "player_id": p.player_id,
            "username": p.username,
            "total_points": int(p.total_points or 0)
        }
        for p in top_players
    ]

    return jsonify(result), 200


# ============================================================
# 3. ROUTE: GET PLAYER HISTORY
# ------------------------------------------------------------
# Endpoint: GET /api/leaderboard/player/<int:player_id>
# Purpose : Retrieves recent scores and ranking for one player.
# ------------------------------------------------------------
# Example Response:
# {
#   "player_id": 1,
#   "username": "TomHero",
#   "total_points": 350,
#   "recent_scores": [
#       {"game_id": 1, "points": 100, "date": "2025-10-23"},
#       {"game_id": 2, "points": 250, "date": "2025-10-24"}
#   ]
# }
# ============================================================
@leaderboard_bp.route("/player/<int:player_id>", methods=["GET"])
def get_player_history(player_id):
    db = get_db()

    player = db.query(Player).filter_by(id=player_id).first()
    if not player:
        return jsonify({"error": "Player not found"}), 404

    # Fetch all scores for this player
    scores = (
        db.query(Score)
        .filter_by(player_id=player_id)
        .order_by(desc(Score.created_at))
        .limit(10)
        .all()
    )

    total_points = db.query(func.sum(Score.points)).filter_by(player_id=player_id).scalar() or 0

    player_data = {
        "player_id": player.id,
        "username": player.username,
        "total_points": int(total_points),
        "recent_scores": [
            {
                "game_id": s.game_id,
                "points": s.points,
                "date": s.created_at.strftime("%Y-%m-%d %H:%M:%S")
            }
            for s in scores
        ]
    }

    return jsonify(player_data), 200


# ============================================================
# 4. ROUTE: GLOBAL LEADERBOARD SUMMARY
# ------------------------------------------------------------
# Endpoint: GET /api/leaderboard/summary
# Purpose : Provides quick stats for dashboard or homepage view.
# ------------------------------------------------------------
# Example Response:
# {
#   "total_players": 50,
#   "total_games": 200,
#   "highest_score": 500
# }
# ============================================================
@leaderboard_bp.route("/summary", methods=["GET"])
def leaderboard_summary():
    db = get_db()

    total_players = db.query(func.count(Player.id)).scalar()
    total_games = db.query(func.count(Score.game_id.distinct())).scalar()
    highest_score = db.query(func.max(Score.points)).scalar() or 0

    summary = {
        "total_players": total_players,
        "total_games": total_games,
        "highest_score": int(highest_score)
    }

    return jsonify(summary), 200
