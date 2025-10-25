# ============================================================
# File: backend/models/player_model.py
# Description: Defines the Player model for the Tom & Jerry game.
#              Stores player identity, character type, score,
#              and connection status.
# ============================================================

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from backend.models import Base

# ============================================================
# 1. PLAYER MODEL
# ------------------------------------------------------------
# Represents a player in the game. Each record stores basic
# profile info, current character (Tom or Jerry), connection
# status, and accumulated score.
# ============================================================
class Player(Base):
    __tablename__ = "players"

    # ------------------------------------------------------------
    # Primary Key ID — unique identifier for each player
    # ------------------------------------------------------------
    id = Column(Integer, primary_key=True, index=True)

    # ------------------------------------------------------------
    # Username — unique name chosen by the player
    # ------------------------------------------------------------
    username = Column(String(50), unique=True, nullable=False)

    # ------------------------------------------------------------
    # Character — either "Tom" or "Jerry"
    # ------------------------------------------------------------
    character = Column(String(10), nullable=False)

    # ------------------------------------------------------------
    # Score — player's accumulated score from all matches
    # ------------------------------------------------------------
    score = Column(Integer, default=0)

    # ------------------------------------------------------------
    # Online Status — True if currently connected via Socket.IO
    # ------------------------------------------------------------
    online = Column(Boolean, default=False)

    # ------------------------------------------------------------
    # Created Timestamp — when the player was registered
    # ------------------------------------------------------------
    created_at = Column(DateTime, default=datetime.utcnow)

    # ============================================================
    # 2. REPR METHOD
    # ------------------------------------------------------------
    # Provides a readable string representation of the Player
    # object when printed (useful for debugging/logs).
    # ============================================================
    def __repr__(self):
        return f"<Player(username='{self.username}', character='{self.character}', score={self.score})>"
