# ============================================================
# File: backend/database/db.py
# Description: Database setup file that initializes SQLAlchemy engine
#              and session for handling all database operations
# ============================================================

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from backend.config import DATABASE_PATH

# ============================================================
# 1. DATABASE CONNECTION STRING
# ------------------------------------------------------------
# Here, we use SQLite as the default database. The path is imported
# from backend/config.py, where it points to:
#    /database/tomjerry.db
# The 'check_same_thread=False' is required for Flask's threaded mode.
# ============================================================
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# ============================================================
# 2. ENGINE CREATION
# ------------------------------------------------------------
# The engine acts as the core interface to the database.
# It manages connections, executes SQL commands, and handles
# communication between SQLAlchemy and the actual DB file.
# ============================================================
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
    echo=False  # Set to True for debugging SQL queries
)

# ============================================================
# 3. SESSION FACTORY
# ------------------------------------------------------------
# Session objects handle transactions and ORM operations.
# We use scoped_session so each Flask request gets its own
# isolated session (thread-safe).
# ============================================================
SessionLocal = scoped_session(
    sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
)

# ============================================================
# 4. HELPER FUNCTION
# ------------------------------------------------------------
# This function returns a database session. Use it inside your
# API routes or game logic to query or modify data.
# Always close the session after using it!
# Example usage:
#   db = get_db()
#   players = db.query(PlayerModel).all()
#   db.close()
# ============================================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================
# 5. INITIALIZATION CHECK
# ------------------------------------------------------------
# When this file runs, it prints a confirmation message.
# Useful during debugging or server startup.
# ============================================================
if __name__ == "__main__":
    print("✅ Database engine initialized successfully at:", DATABASE_URL)
