# ============================================================
# File: backend/models/game_model.py
# Description: Defines the Game model for the Tom & Jerry game.
#              Represents each match played between players,
#              including participants, scores, duration, and result.
# ============================================================

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from backend.models import Base

# ============================================================
# 1. GAME MODEL
# ------------------------------------------------------------
# Represents a single match or game session.
# Each record stores references to the participating players,
# their scores, duration, and the final winner.
# ============================================================
class Game(Base):
    __tablename__ = "games"

    # ------------------------------------------------------------
    # Primary Key ID — unique identifier for each game session
    # ------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)

    # ------------------------------------------------------------
    # Player References — foreign keys linking to the players table
    # ------------------------------------------------------------
    tom_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    jerry_id = Column(Integer, ForeignKey("players.id"), nullable=False)

    # ------------------------------------------------------------
    # Scores — Tom's and Jerry's individual scores for this game
    # ------------------------------------------------------------
    tom_score = Column(Integer, default=0)
    jerry_score = Column(Integer, default=0)

    # ------------------------------------------------------------
    # Winner — name of the winning player ("Tom" or "Jerry")
    # ------------------------------------------------------------
    winner = Column(String(10), nullable=True)

    # ------------------------------------------------------------
    # Duration — total time of the game in seconds
    # ------------------------------------------------------------
    duration = Column(Integer, nullable=True)

    # ------------------------------------------------------------
    # Created Timestamp — when this game session was recorded
    # ------------------------------------------------------------
    created_at = Column(DateTime, default=datetime.utcnow)

    # ============================================================
    # 2. REPR METHOD
    # ------------------------------------------------------------
    # Provides a clear, readable string representation of the game
    # instance for debugging, logging, or display purposes.
    # ============================================================
    def __repr__(self):
        return (
            f"<Game(id={self.id}, tom_id={self.tom_id}, "
            f"jerry_id={self.jerry_id}, winner='{self.winner}')>"
        )
