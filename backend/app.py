from flask import Flask, jsonify, request
from flask_cors import CORS
from backend.sockets.socket_manager import init_socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'change-me'
CORS(app, supports_credentials=True)

# Simple in-memory game state
GAME_STATE = {
    'players': {},
    'moves': []
}

# REST endpoint for game state
@app.route('/api/game-state', methods=['GET'])
def get_game_state():
    return jsonify(GAME_STATE)

# Initialize Socket.IO
socketio = init_socket(app, GAME_STATE)

@app.route('/')
def index():
    return {'message': 'Tom & Jerry Backend (Flask) is running'}

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)
