# Serialization helpers
# ============================================================
# File: backend/utils/serializer.py
# Description:
#   This utility module provides reusable serialization helpers
#   for converting Python objects (especially SQLAlchemy models)
#   into JSON-friendly dictionaries.
#   It simplifies how database models are returned through APIs.
# ============================================================

from datetime import datetime
from typing import Any, Dict


# ============================================================
# SECTION 1: Generic Serializer Function
# ------------------------------------------------------------
# The `serialize_model` function takes in a SQLAlchemy model
# instance and converts it into a dictionary that can be safely
# returned as JSON.
# ============================================================

def serialize_model(model) -> Dict[str, Any]:
    """
    Convert a SQLAlchemy model instance into a JSON-serializable dictionary.

    :param model: SQLAlchemy model instance
    :return: Dictionary of column-value pairs
    """
    serialized_data = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        serialized_data[column.name] = format_value(value)
    return serialized_data


# ============================================================
# SECTION 2: Serializer for Lists of Models
# ------------------------------------------------------------
# This helper is used when you want to serialize a list or query
# result of multiple model instances into JSON-ready data.
# ============================================================

def serialize_list(models) -> list:
    """
    Serialize a list of SQLAlchemy model instances.

    :param models: Iterable (e.g., list or SQLAlchemy query result)
    :return: List of serialized dictionaries
    """
    return [serialize_model(m) for m in models]


# ============================================================
# SECTION 3: Value Formatting Helper
# ------------------------------------------------------------
# Since JSON doesn’t support complex types like datetime or
# decimals natively, this function ensures all values are cleanly
# formatted before sending them as API responses.
# ============================================================

def format_value(value: Any) -> Any:
    """
    Format values to make them JSON serializable.

    :param value: Raw value (e.g., datetime, decimal, str)
    :return: JSON-safe representation
    """
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.decode("utf-8")
    return value


# ============================================================
# SECTION 4: Example - Custom Game Serialization
# ------------------------------------------------------------
# (Optional) You can use this pattern to serialize custom logic
# like game states, scores, or joined query results.
# ============================================================

def serialize_game_state(game_state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Serialize custom in-memory game state for Socket or API responses.

    :param game_state: Dictionary containing player data and moves
    :return: Cleaned and JSON-serializable version
    """
    return {
        "players": game_state.get("players", {}),
        "moves": game_state.get("moves", []),
        "timestamp": datetime.utcnow().isoformat()
    }
