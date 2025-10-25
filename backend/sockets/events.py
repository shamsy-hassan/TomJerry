# ============================================================
# File: backend/sockets/events.py
# Description:
#     This file defines all real-time WebSocket (Socket.IO)
#     event handlers for the Tom & Jerry game.
#     It manages player connections, movement broadcasting,
#     and shared game state synchronization.
# ============================================================


# ============================================================
# 1. REGISTER SOCKET EVENTS
# ------------------------------------------------------------
# This function is called from socket_manager.py to register
# all event listeners for the Flask-SocketIO server.
# ============================================================
def register_socket_events(socketio, game_state):
    """
    Registers all WebSocket event listeners for the game.

    Args:
        socketio (SocketIO): The Socket.IO instance.
        game_state (dict): Shared in-memory state tracking
                           players, positions, and moves.
    """

    # --------------------------------------------------------
    # EVENT: CONNECT
    # --------------------------------------------------------
    # Triggered whenever a new client establishes a WebSocket
    # connection with the server.
    # Useful for tracking active players or connections.
    # --------------------------------------------------------
    @socketio.on('connect')
    def handle_connect():
        print('⚡ Client connected to the game server')

    # --------------------------------------------------------
    # EVENT: DISCONNECT
    # --------------------------------------------------------
    # Triggered when a client disconnects (e.g., closes tab,
    # loses network, or logs out).
    # --------------------------------------------------------
    @socketio.on('disconnect')
    def handle_disconnect():
        print('🔌 Client disconnected from the game server')

    # --------------------------------------------------------
    # EVENT: JOIN
    # --------------------------------------------------------
    # Fired when a new player joins the game.
    # The client emits this event with player_id information.
    #
    # Example payload:
    #   { "player_id": "Jerry" }
    #
    # This adds the player to the shared game_state dictionary
    # and notifies all connected clients.
    # --------------------------------------------------------
    @socketio.on('join')
    def handle_join(data):
        player_id = data.get('player_id')

        if player_id:
            # Add player to the game state with default position
            game_state['players'][player_id] = {'x': 0, 'y': 0}

            print(f"🎮 Player joined: {player_id}")

            # Broadcast updated state to all players
            socketio.emit(
                'player_joined',
                {
                    'player_id': player_id,
                    'players': game_state['players']
                },
                broadcast=True
            )
        else:
            print("⚠️ Join event received without player_id")

    # --------------------------------------------------------
    # EVENT: MOVE
    # --------------------------------------------------------
    # Fired when a player moves their character (Tom or Jerry).
    # The client emits movement data (x, y coordinates) which
    # updates the shared game state and broadcasts to others.
    #
    # Example payload:
    #   { "player_id": "Tom", "x": 120, "y": 240 }
    #
    # The server stores movement history and syncs positions.
    # --------------------------------------------------------
    @socketio.on('move')
    def handle_move(data):
        player_id = data.get('player_id')
        x = data.get('x')
        y = data.get('y')

        if player_id and x is not None and y is not None:
            # Update player position in game state
            game_state['players'][player_id] = {'x': x, 'y': y}

            # Log move to move history
            game_state['moves'].append({
                'player_id': player_id,
                'x': x,
                'y': y
            })

            # Broadcast updated positions to all connected clients
            socketio.emit(
                'player_moved',
                {
                    'player_id': player_id,
                    'x': x,
                    'y': y,
                    'players': game_state['players']
                },
                broadcast=True
            )

            print(f"🏃 Player {player_id} moved to ({x}, {y})")

        else:
            print("⚠️ Invalid move data received:", data)
