# ================================================================
# File: backend/game_logic/ai_controller.py
# Description:
#   This module defines simple AI behavior for non-player characters
#   (Tom or Jerry) in the Tom & Jerry game.
#   The AI can:
#     - Chase the target (Tom chasing Jerry)
#     - Escape from the target (Jerry avoiding Tom)
#   Uses basic distance calculations and movement predictions.
# ================================================================

import math
import random

# ================================================================
# 1. AI CONTROLLER CLASS
# ------------------------------------------------
# Responsible for generating AI-controlled moves
# based on player positions and basic strategies.
# ================================================================
class AIController:
    def __init__(self, game_state, role="tom"):
        """
        Initialize the AI controller.
        :param game_state: Shared dictionary tracking all player positions.
        :param role: Either 'tom' (chaser) or 'jerry' (escaper).
        """
        self.game_state = game_state
        self.role = role.lower()
        self.speed = 5  # Movement speed of AI

    # ============================================================
    # 2. CALCULATE DISTANCE
    # ------------------------------------------------------------
    # Helper method to calculate distance between two points.
    # Used to decide movement direction for AI.
    # ============================================================
    def distance(self, pos1, pos2):
        return math.sqrt((pos1['x'] - pos2['x'])**2 + (pos1['y'] - pos2['y'])**2)

    # ============================================================
    # 3. DECIDE NEXT MOVE
    # ------------------------------------------------------------
    # Based on role (Tom or Jerry), decide where to move next.
    # - Tom moves toward Jerry.
    # - Jerry moves away from Tom.
    # ============================================================
    def decide_next_move(self, ai_id, target_id):
        if ai_id not in self.game_state['players'] or target_id not in self.game_state['players']:
            return None

        ai_pos = self.game_state['players'][ai_id]
        target_pos = self.game_state['players'][target_id]

        dx = target_pos['x'] - ai_pos['x']
        dy = target_pos['y'] - ai_pos['y']
        distance = max(self.distance(ai_pos, target_pos), 1)  # avoid division by zero

        # Normalize direction
        direction_x = dx / distance
        direction_y = dy / distance

        if self.role == "tom":
            # Move toward target
            new_x = ai_pos['x'] + direction_x * self.speed
            new_y = ai_pos['y'] + direction_y * self.speed
        else:
            # Move away from target (Jerry escaping)
            new_x = ai_pos['x'] - direction_x * self.speed
            new_y = ai_pos['y'] - direction_y * self.speed

        # Add slight randomness to movement for realism
        new_x += random.uniform(-1, 1)
        new_y += random.uniform(-1, 1)

        # Update game state
        self.game_state['players'][ai_id] = {'x': new_x, 'y': new_y}

        # Return for broadcasting
        return {'player_id': ai_id, 'x': new_x, 'y': new_y}

    # ============================================================
    # 4. UPDATE LOOP
    # ------------------------------------------------------------
    # This would be called periodically (e.g., via Socket.IO)
    # to update AI movement in real-time during the game.
    # ============================================================
    def update(self, ai_id, target_id):
        move = self.decide_next_move(ai_id, target_id)
        if move:
            # Append move to global move history
            self.game_state['moves'].append(move)
            return move
        return None
