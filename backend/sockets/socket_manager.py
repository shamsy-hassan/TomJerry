from flask_socketio import SocketIO

socketio = None

def init_socket(app, game_state):
    global socketio
    socketio = SocketIO(app, cors_allowed_origins='*')
    # Register events
    try:
        from backend.sockets.events import register_socket_events
        register_socket_events(socketio, game_state)
    except Exception:
        pass
    return socketio
