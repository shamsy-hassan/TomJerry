# WebSocket events
def register_socket_events(socketio, game_state):
    @socketio.on('connect')
    def handle_connect():
        print('Client connected')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Client disconnected')

    @socketio.on('join')
    def handle_join(data):
        player_id = data.get('player_id')
        if player_id:
            game_state['players'][player_id] = {'x': 0, 'y': 0}
            socketio.emit('player_joined', {'player_id': player_id, 'players': game_state['players']}, broadcast=True)

    @socketio.on('move')
    def handle_move(data):
        player_id = data.get('player_id')
        x = data.get('x')
        y = data.get('y')
        if player_id and x is not None and y is not None:
            game_state['players'][player_id] = {'x': x, 'y': y}
            game_state['moves'].append({'player_id': player_id, 'x': x, 'y': y})
            socketio.emit('player_moved', {'player_id': player_id, 'x': x, 'y': y, 'players': game_state['players']}, broadcast=True)
