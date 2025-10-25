# ============================================================
# File: backend/models/score_model.py
# Description: Defines the Score model for the Tom & Jerry game.
#              Stores historical scores of each player from
#              different matches for leaderboard and analytics.
# ============================================================

from sqlalchemy import Column, Integer, ForeignKey, DateTime
from datetime import datetime
from backend.models import Base

# ============================================================
# 1. SCORE MODEL
# ------------------------------------------------------------
# Represents an individual scoring record linked to a player
# and optionally a game session.
# This helps in tracking score history and leaderboard stats.
# ============================================================
class Score(Base):
    __tablename__ = "scores"

    # ------------------------------------------------------------
    # Primary Key ID — unique identifier for each score record
    # ------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)

    # ------------------------------------------------------------
    # Player Reference — links to the player who earned this score
    # ------------------------------------------------------------
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    # ------------------------------------------------------------
    # Game Reference — links to the game session this score came from
    # ------------------------------------------------------------
    game_id = Column(Integer, ForeignKey("games.id"), nullable=True)

    # ------------------------------------------------------------
    # Points — the score value gained during the game
    # ------------------------------------------------------------
    points = Column(Integer, nullable=False)

    # ------------------------------------------------------------
    # Timestamp — when this score record was added
    # ------------------------------------------------------------
    created_at = Column(DateTime, default=datetime.utcnow)

    # ============================================================
    # 2. REPR METHOD
    # ------------------------------------------------------------
    # Returns a readable string representation of this score record
    # for debugging and admin logging.
    # ============================================================
    def __repr__(self):
        return f"<Score(player_id={self.player_id}, points={self.points}, game_id={self.game_id})>"
