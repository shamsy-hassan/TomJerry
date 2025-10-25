# ================================================================
# File: backend/game_logic/powerups.py
# Description:
#   This module handles the logic for collectible power-ups
#   in the Tom & Jerry game. Power-ups are temporary effects
#   that modify player abilities like speed, visibility, or traps.
# ================================================================

import random
import time

# ================================================================
# 1. POWERUP CLASS
# ------------------------------------------------
# Represents a single power-up in the game world.
# Each has a type (e.g., speed boost) and a duration.
# ================================================================
class PowerUp:
    def __init__(self, powerup_type, x, y, duration=5):
        """
        Initialize a power-up item.
        :param powerup_type: String type ('speed', 'invisibility', 'trap')
        :param x: X position on the map
        :param y: Y position on the map
        :param duration: Duration of power-up effect in seconds
        """
        self.type = powerup_type
        self.x = x
        self.y = y
        self.duration = duration
        self.active = True
        self.spawn_time = time.time()

    def is_expired(self):
        """Check if the power-up effect time has passed."""
        return time.time() - self.spawn_time > self.duration


# ================================================================
# 2. POWERUP MANAGER CLASS
# ------------------------------------------------
# Manages spawning, activation, and expiration of all power-ups.
# Keeps track of active and collected power-ups for all players.
# ================================================================
class PowerUpManager:
    def __init__(self, game_state):
        """
        Initialize PowerUpManager with shared game state.
        :param game_state: Dictionary tracking players and moves.
        """
        self.game_state = game_state
        self.active_powerups = []
        self.collected_powerups = {}

    # ============================================================
    # SPAWN POWERUPS
    # ------------------------------------------------------------
    # Randomly spawn power-ups at different coordinates.
    # Typically triggered periodically during gameplay.
    # ============================================================
    def spawn_powerup(self):
        powerup_types = ['speed', 'invisibility', 'trap']
        p_type = random.choice(powerup_types)
        x, y = random.randint(0, 500), random.randint(0, 500)

        powerup = PowerUp(p_type, x, y)
        self.active_powerups.append(powerup)

        print(f"[PowerUpManager] 🧩 Spawned {p_type} power-up at ({x}, {y})")
        return {'type': p_type, 'x': x, 'y': y, 'duration': powerup.duration}

    # ============================================================
    # COLLECT POWERUP
    # ------------------------------------------------------------
    # Triggered when a player touches a power-up on the map.
    # The effect is applied temporarily and tracked per player.
    # ============================================================
    def collect_powerup(self, player_id, powerup_index):
        if powerup_index >= len(self.active_powerups):
            return None

        powerup = self.active_powerups.pop(powerup_index)
        powerup.active = False
        self.collected_powerups[player_id] = {
            'type': powerup.type,
            'expires_at': time.time() + powerup.duration
        }

        print(f"[PowerUpManager] ⚡ Player {player_id} collected {powerup.type} power-up.")
        return {'player_id': player_id, 'powerup': powerup.type}

    # ============================================================
    # UPDATE POWERUPS
    # ------------------------------------------------------------
    # Called periodically to remove expired effects
    # and respawn new ones for continued gameplay.
    # ============================================================
    def update(self):
        # Remove expired power-ups
        self.active_powerups = [p for p in self.active_powerups if not p.is_expired()]

        # Remove expired player effects
        now = time.time()
        expired_players = [
            pid for pid, data in self.collected_powerups.items()
            if data['expires_at'] <= now
        ]
        for pid in expired_players:
            expired_type = self.collected_powerups[pid]['type']
            del self.collected_powerups[pid]
            print(f"[PowerUpManager] ⏳ Player {pid}'s {expired_type} effect expired.")

        # Random chance to spawn a new power-up
        if random.random() < 0.1:  # 10% chance every update cycle
            self.spawn_powerup()

    # ============================================================
    # APPLY EFFECT
    # ------------------------------------------------------------
    # Helper to apply the active effect of a power-up to player stats.
    # For example, speed boost or invisibility logic.
    # ============================================================
    def apply_effect(self, player_id, player_state):
        if player_id not in self.collected_powerups:
            return player_state

        effect = self.collected_powerups[player_id]['type']

        if effect == 'speed':
            player_state['speed'] = player_state.get('speed', 5) * 1.5
        elif effect == 'invisibility':
            player_state['visible'] = False
        elif effect == 'trap':
            player_state['trapped'] = True

        return player_state
