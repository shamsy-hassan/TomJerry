# ============================================================
# File: backend/app.py
# Description: Main entry point for the Tom & Jerry game backend.
# It initializes the Flask app, configures CORS, sets up routes,
# and integrates Socket.IO for real-time game communication.
# ============================================================

from flask import Flask, jsonify
from flask_cors import CORS
from backend.sockets.socket_manager import init_socket
from backend.config import Config

# ============================================================
# Function: create_app()
# Purpose: Factory function to create and configure the Flask app.
# Using a factory allows flexibility for testing and scaling later.
# ============================================================
def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # Load configuration from config.py
    app.config.from_object(Config)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app, supports_credentials=True)

    # ============================================================
    # SECTION: In-Memory Game State
    # ------------------------------------------------------------
    # This holds temporary data for the current game.
    # In production, this could be replaced with Redis or a database.
    # ============================================================
    GAME_STATE = {
        'players': {},   # Player list with their states
        'moves': []      # Recent moves or actions in the game
    }

    # ============================================================
    # SECTION: Register API Blueprints
    # ------------------------------------------------------------
    # This allows separating API routes for authentication,
    # players, leaderboard, etc., keeping code organized.
    # ============================================================
    from backend.api.auth import auth_bp
    from backend.api.player import player_bp
    from backend.api.leaderboard import leaderboard_bp
    from backend.api.game_routes import game_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(player_bp, url_prefix='/api/player')
    app.register_blueprint(leaderboard_bp, url_prefix='/api/leaderboard')
    app.register_blueprint(game_bp, url_prefix='/api/game')

    # ============================================================
    # SECTION: Basic Health Check Route
    # ------------------------------------------------------------
    # Used to verify the backend is running and reachable.
    # ============================================================
    @app.route('/')
    def index():
        return jsonify({'message': 'Tom & Jerry Backend (Flask) is running'}), 200

    # ============================================================
    # SECTION: Game State Route
    # ------------------------------------------------------------
    # Quick endpoint to retrieve current game state (for debugging
    # or client sync). In real use, Socket.IO manages live updates.
    # ============================================================
    @app.route('/api/game-state', methods=['GET'])
    def get_game_state():
        return jsonify(GAME_STATE)

    # ============================================================
    # SECTION: Initialize Socket.IO
    # ------------------------------------------------------------
    # WebSocket setup for real-time player movement, game events,
    # and communication between Tom and Jerry clients.
    # ============================================================
    socketio = init_socket(app, GAME_STATE)

    return app, socketio


# ============================================================
# SECTION: Application Entry Point
# ------------------------------------------------------------
# Runs the Flask app with Socket.IO support.
# The host '0.0.0.0' allows external access in LAN/dev mode.
# ============================================================
if __name__ == '__main__':
    app, socketio = create_app()
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
