# ================================================================
# File: backend/game_logic/rooms.py
# Description:
#   Handles the creation, management, and lifecycle of
#   multiplayer rooms in the Tom & Jerry game.
#
#   Each room can host multiple players (e.g., Tom vs Jerry),
#   and tracks its own state such as players, scores, and readiness.
# ================================================================

import uuid
import time

# ================================================================
# 1. ROOM CLASS
# ------------------------------------------------
# Represents a single active room instance.
# Tracks players, scores, and room status.
# ================================================================
class Room:
    def __init__(self, name, max_players=2):
        """
        Initialize a game room with a unique ID and optional name.
        :param name: Human-readable name (e.g. "House Arena")
        :param max_players: Maximum allowed players per room
        """
        self.id = str(uuid.uuid4())  # unique room ID
        self.name = name
        self.max_players = max_players
        self.players = {}
        self.created_at = time.time()
        self.started = False
        self.finished = False
        self.scoreboard = {}
        self.chat_history = []

    def add_player(self, player_id, nickname):
        """Add a player to this room if capacity allows."""
        if len(self.players) >= self.max_players:
            return False  # Room full

        self.players[player_id] = {
            'nickname': nickname,
            'ready': False,
            'score': 0,
            'joined_at': time.time()
        }
        print(f"[Room] 👤 Player '{nickname}' joined room '{self.name}'.")
        return True

    def remove_player(self, player_id):
        """Remove a player from the room."""
        if player_id in self.players:
            player_name = self.players[player_id]['nickname']
            del self.players[player_id]
            print(f"[Room] ❌ Player '{player_name}' left room '{self.name}'.")
            return True
        return False

    def all_ready(self):
        """Check if all players in the room are ready to start."""
        return all(p['ready'] for p in self.players.values())

    def start_game(self):
        """Mark the room's game session as started."""
        if not self.started and self.all_ready():
            self.started = True
            print(f"[Room] 🎮 Game started in room '{self.name}'.")
            return True
        return False

    def end_game(self):
        """Mark the room as finished and record final scores."""
        self.finished = True
        self.scoreboard = {
            pid: data['score'] for pid, data in self.players.items()
        }
        print(f"[Room] 🏁 Game in room '{self.name}' has ended.")
        return self.scoreboard

    def add_chat(self, player_id, message):
        """Append a chat message to the room history."""
        nickname = self.players.get(player_id, {}).get('nickname', 'Unknown')
        msg = {'player': nickname, 'text': message, 'timestamp': time.time()}
        self.chat_history.append(msg)
        return msg


# ================================================================
# 2. ROOM MANAGER CLASS
# ------------------------------------------------
# Oversees all active rooms, allows new room creation,
# joining, and cleanup when empty or finished.
# ================================================================
class RoomManager:
    def __init__(self):
        """Initialize the global room manager with a dict of active rooms."""
        self.rooms = {}

    # ------------------------------------------------------------
    # CREATE ROOM
    # ------------------------------------------------------------
    def create_room(self, name=None, max_players=2):
        """Create a new room and return its data."""
        room = Room(name or f"Room-{len(self.rooms)+1}", max_players)
        self.rooms[room.id] = room
        print(f"[RoomManager] 🏠 Created new room: {room.name} (ID: {room.id})")
        return room

    # ------------------------------------------------------------
    # GET ROOM BY ID
    # ------------------------------------------------------------
    def get_room(self, room_id):
        """Fetch a room by its unique ID."""
        return self.rooms.get(room_id)

    # ------------------------------------------------------------
    # JOIN ROOM
    # ------------------------------------------------------------
    def join_room(self, room_id, player_id, nickname):
        """Add a player to an existing room."""
        room = self.get_room(room_id)
        if not room:
            print(f"[RoomManager] ⚠️ Room with ID {room_id} not found.")
            return None

        if room.add_player(player_id, nickname):
            return room
        else:
            print(f"[RoomManager] 🚫 Failed to add {nickname} (room full).")
            return None

    # ------------------------------------------------------------
    # LEAVE ROOM
    # ------------------------------------------------------------
    def leave_room(self, room_id, player_id):
        """Remove a player from the specified room."""
        room = self.get_room(room_id)
        if not room:
            return False

        success = room.remove_player(player_id)
        # Cleanup room if empty
        if success and not room.players:
            print(f"[RoomManager] 🧹 Removing empty room '{room.name}'.")
            del self.rooms[room_id]
        return success

    # ------------------------------------------------------------
    # UPDATE ROOM STATES
    # ------------------------------------------------------------
    def update_rooms(self):
        """Periodic cleanup of finished or inactive rooms."""
        now = time.time()
        expired = [
            rid for rid, room in self.rooms.items()
            if room.finished and (now - room.created_at) > 300
        ]
        for rid in expired:
            print(f"[RoomManager] ⏳ Removing old finished room: {self.rooms[rid].name}")
            del self.rooms[rid]

    # ------------------------------------------------------------
    # GET ALL ROOMS (LISTING)
    # ------------------------------------------------------------
    def list_rooms(self):
        """Return summary info for all active rooms."""
        return [
            {
                'id': r.id,
                'name': r.name,
                'players': len(r.players),
                'max_players': r.max_players,
                'started': r.started
            }
            for r in self.rooms.values()
        ]
