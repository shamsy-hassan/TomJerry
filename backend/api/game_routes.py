from flask import Blueprint, request, jsonify

bp = Blueprint('game', __name__, url_prefix='/game')

@bp.route('/start', methods=['POST'])
def start_game():
	data = request.json or {}
	# Create a new game session, assign an id, and initialize sockets/room
	# TODO: implement game_model and room creation
	game_id = 'game-1234'
	return jsonify({'game_id': game_id}), 201

@bp.route('/restart', methods=['POST'])
def restart_game():
	data = request.json or {}
	# TODO: implement restart logic based on game_id
	return jsonify({'status': 'restarted'})
