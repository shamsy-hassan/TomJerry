# ============================================================
# File: backend/config.py
# Description:
# Central configuration file for Flask backend
# ============================================================

import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Path to the database file
DATABASE_PATH = os.path.join(BASE_DIR, "database", "tomjerry.db")


class Config:
    """General Flask application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "supersecretkey")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_PATH}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True

SECRET_KEY = Config.SECRET_KEY
