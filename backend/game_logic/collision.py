# ============================================================
# File: backend/game_logic/collision.py
# Description:
#     Handles all collision-related logic in the Tom & Jerry game.
#     Includes detection between players, walls, and collectible items.
#     Works together with physics.py to create realistic gameplay.
# ============================================================

import math

# ============================================================
# 1. COLLISION BETWEEN TWO PLAYERS
# ------------------------------------------------------------
# Simple circular collision detection based on player positions.
# Used mainly for Tom catching Jerry.
# ============================================================
def players_collide(player_a, player_b, radius=25):
    """
    Checks if two players collide based on proximity.

    Args:
        player_a (dict): First player's state (x, y)
        player_b (dict): Second player's state (x, y)
        radius (int): Collision radius (default 25 pixels)

    Returns:
        bool: True if players overlap, False otherwise.
    """
    dx = player_a['x'] - player_b['x']
    dy = player_a['y'] - player_b['y']
    distance = math.sqrt(dx ** 2 + dy ** 2)
    return distance < radius


# ============================================================
# 2. COLLISION WITH WALLS / MAP BOUNDARIES
# ------------------------------------------------------------
# Prevents players from moving outside the screen or solid objects.
# ============================================================
def handle_wall_collision(player_state, world_bounds):
    """
    Keeps player inside playable area and prevents clipping through walls.

    Args:
        player_state (dict): Contains player's position (x, y)
        world_bounds (dict): Defines x_min, x_max, y_min, y_max
    """
    if player_state['x'] < world_bounds['x_min']:
        player_state['x'] = world_bounds['x_min']
    elif player_state['x'] > world_bounds['x_max']:
        player_state['x'] = world_bounds['x_max']

    if player_state['y'] > world_bounds['y_max']:
        player_state['y'] = world_bounds['y_max']
        player_state['y_velocity'] = 0
        player_state['on_ground'] = True


# ============================================================
# 3. COLLISION WITH ITEMS / COLLECTIBLES
# ------------------------------------------------------------
# Detects when a player touches an item (like cheese or traps).
# Returns item ID if collected.
# ============================================================
def check_item_collision(player_state, items):
    """
    Detects collision between player and collectible items.

    Args:
        player_state (dict): Player's position (x, y)
        items (list): List of item dicts {'id': str, 'x': int, 'y': int, 'radius': int}

    Returns:
        str | None: ID of collected item, or None if no collision.
    """
    for item in items:
        dx = player_state['x'] - item['x']
        dy = player_state['y'] - item['y']
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance < item.get('radius', 20):
            return item['id']
    return None


# ============================================================
# 4. COLLISION RESPONSE
# ------------------------------------------------------------
# Defines what happens when certain collisions occur:
# - Tom catches Jerry → Tom wins
# - Jerry collects cheese → Score increases
# - Player hits trap → Lose points or respawn
# ============================================================
def handle_collision_response(game_state):
    """
    Handles all interactions resulting from collisions.

    Args:
        game_state (dict): Current shared game state including players and items.
    """
    players = game_state.get('players', {})
    items = game_state.get('items', [])

    # Example: Tom catching Jerry
    if 'Tom' in players and 'Jerry' in players:
        if players_collide(players['Tom'], players['Jerry']):
            game_state['status'] = "Tom caught Jerry!"
            game_state['winner'] = "Tom"

    # Check if any player collected an item
    for player_id, state in players.items():
        collected_item = check_item_collision(state, items)
        if collected_item:
            game_state['scores'][player_id] = game_state['scores'].get(player_id, 0) + 10
            game_state['items'] = [item for item in items if item['id'] != collected_item]


# ============================================================
# 5. UPDATE COLLISIONS IN GAME LOOP
# ------------------------------------------------------------
# Utility function used in main game loop to apply all checks
# per frame.
# ============================================================
def update_collisions(game_state, world_bounds):
    """
    Performs full collision update cycle (walls, items, players).

    Args:
        game_state (dict): Global shared game state.
        world_bounds (dict): Boundary limits for the map.
    """
    for _, player in game_state['players'].items():
        handle_wall_collision(player, world_bounds)
    handle_collision_response(game_state)
