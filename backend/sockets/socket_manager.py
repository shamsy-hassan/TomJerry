# ============================================================
# File: backend/sockets/socket_manager.py
# Description:
#     This file initializes and manages the Socket.IO connection
#     for real-time communication in the Tom & Jerry game.
# ============================================================

from flask_socketio import SocketIO
import traceback

# ============================================================
# 1. GLOBAL SOCKET INSTANCE
# ------------------------------------------------------------
# This global variable will hold the SocketIO instance
# so it can be used across other backend modules.
# ============================================================
socketio = None


# ============================================================
# 2. INITIALIZATION FUNCTION
# ------------------------------------------------------------
# Called from app.py to initialize Socket.IO with the Flask app.
# Handles configuration, event registration, and basic connect/disconnect logs.
# ============================================================
def init_socket(app, game_state):
    """
    Initialize and configure Socket.IO for the Flask app.
    Automatically registers all socket event handlers.

    Args:
        app (Flask): The main Flask app instance.
        game_state (dict): Shared in-memory game state.
    """

    global socketio

    # --------------------------------------------------------
    # 2.1. Configure Socket.IO
    # --------------------------------------------------------
    socketio = SocketIO(
        app,
        cors_allowed_origins="*",  # Allow all origins (adjust for production)
        async_mode="threading",    # Good for local dev and simpler concurrency
        ping_timeout=30,           # How long before a ping is considered dead
        ping_interval=10,          # How often to send pings
        logger=True,               # Enables server-side Socket.IO logs
        engineio_logger=True       # Enables low-level connection logs
    )

    # --------------------------------------------------------
    # 2.2. Import and register socket event handlers
    # --------------------------------------------------------
    try:
        # Dynamically import to avoid circular imports
        from backend.sockets.events import register_socket_events

        # Register all the event listeners (join room, move, etc.)
        register_socket_events(socketio, game_state)
        print("[SocketManager] ✅ Socket events registered successfully.")
    except Exception as e:
        print("[SocketManager] ⚠️ Failed to register socket events:")
        traceback.print_exc()

    # --------------------------------------------------------
    # 2.3. Basic connection event logging
    # --------------------------------------------------------
    @socketio.on('connect')
    def handle_connect():
        print("⚡ Client connected to Socket.IO")

    @socketio.on('disconnect')
    def handle_disconnect():
        print("🔌 Client disconnected from Socket.IO")

    # --------------------------------------------------------
    # 2.4. Return instance to main app
    # --------------------------------------------------------
    return socketio
