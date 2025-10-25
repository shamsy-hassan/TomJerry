# ============================================================
# File: backend/models/__init__.py
# Description: Initializes all SQLAlchemy ORM models (Player, Game,
#              Score, etc.) and creates tables in the database.
#              This file ensures all models are imported and
#              synchronized with the database engine.
# ============================================================

from backend.database.db import engine
from sqlalchemy.orm import declarative_base

# ============================================================
# 1. BASE CLASS
# ------------------------------------------------------------
# SQLAlchemy’s Declarative Base class acts as the foundation
# for all models (tables). Each model will inherit from this base.
# ============================================================
Base = declarative_base()

# ============================================================
# 2. MODEL IMPORTS
# ------------------------------------------------------------
# Import all model classes here so they register automatically
# when Base.metadata.create_all(engine) is called.
# Each model file defines its own table and structure.
# ============================================================
from backend.models.player_model import Player
from backend.models.game_model import Game
from backend.models.score_model import Score

# ============================================================
# 3. DATABASE TABLE CREATION
# ------------------------------------------------------------
# This line creates all tables defined in the imported models
# if they don’t already exist in the database.
# It’s safe to call this multiple times — SQLAlchemy checks
# before creating duplicate tables.
# ============================================================
def init_db():
    Base.metadata.create_all(bind=engine)
    print("✅ All database tables initialized successfully.")

# ============================================================
# 4. INITIALIZATION CHECK
# ------------------------------------------------------------
# If this file is run directly, it will initialize the database
# tables manually. Useful for setup or testing.
# ============================================================
if __name__ == "__main__":
    init_db()
