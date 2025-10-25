# ============================================================
# File: backend/game_logic/physics.py
# Description:
#     Handles the physics and movement logic for the Tom & Jerry
#     multiplayer game. Responsible for player motion updates,
#     collision checks, and enforcing map boundaries.
# ============================================================

import math

# ============================================================
# 1. CONSTANTS (Game Physics Settings)
# ------------------------------------------------------------
# These values define how fast characters move, gravity force,
# and the boundaries of the playable area.
# Modify them to tweak game difficulty or speed.
# ============================================================
GRAVITY = 0.4           # Downward force on jumps
MOVE_SPEED = 5.0        # Horizontal movement speed
JUMP_FORCE = 10.0       # Jumping vertical boost
MAX_FALL_SPEED = 12.0   # Limit to how fast a character can fall
WORLD_BOUNDS = {'x_min': 0, 'x_max': 800, 'y_min': 0, 'y_max': 600}


# ============================================================
# 2. APPLY GRAVITY
# ------------------------------------------------------------
# Updates the player’s vertical velocity based on gravity
# (simulating realistic falling and jumping).
# ============================================================
def apply_gravity(player_state):
    """Applies gravity to the player’s vertical position."""
    if player_state['y_velocity'] < MAX_FALL_SPEED:
        player_state['y_velocity'] += GRAVITY
    player_state['y'] += player_state['y_velocity']


# ============================================================
# 3. MOVE PLAYER
# ------------------------------------------------------------
# Moves player based on direction input and enforces game world
# boundaries to prevent moving off-screen.
# ============================================================
def move_player(player_state, direction):
    """
    Updates player position based on input direction.

    Args:
        player_state (dict): Player data (x, y, velocities)
        direction (str): 'left', 'right', or 'jump'
    """
    if direction == 'left':
        player_state['x'] -= MOVE_SPEED
    elif direction == 'right':
        player_state['x'] += MOVE_SPEED
    elif direction == 'jump' and player_state['on_ground']:
        player_state['y_velocity'] = -JUMP_FORCE
        player_state['on_ground'] = False

    # Enforce world boundaries
    player_state['x'] = max(WORLD_BOUNDS['x_min'], min(player_state['x'], WORLD_BOUNDS['x_max']))
    player_state['y'] = max(WORLD_BOUNDS['y_min'], min(player_state['y'], WORLD_BOUNDS['y_max']))


# ============================================================
# 4. DETECT COLLISION BETWEEN TWO PLAYERS
# ------------------------------------------------------------
# Basic rectangle-based collision detection to check if Tom
# has caught Jerry (or vice versa).
# ============================================================
def check_collision(player_a, player_b, collision_radius=25):
    """
    Detects collision between two players using circle distance.

    Args:
        player_a (dict): First player's (x, y)
        player_b (dict): Second player's (x, y)
        collision_radius (int): Minimum distance to count as collision

    Returns:
        bool: True if players collide, else False
    """
    dx = player_a['x'] - player_b['x']
    dy = player_a['y'] - player_b['y']
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance < collision_radius


# ============================================================
# 5. UPDATE GAME STATE
# ------------------------------------------------------------
# Main function used by socket events or game loop to continuously
# update player positions and apply gravity.
# ============================================================
def update_game_state(game_state):
    """
    Iterates through all players and applies physics updates.

    Args:
        game_state (dict): Shared global game state with player data.
    """
    for player_id, state in game_state['players'].items():
        apply_gravity(state)
        move_player(state, state.get('direction', None))
