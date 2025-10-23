// Config (URLs, colors, etc.)
// Centralized app constants
export const PHYSICS_TICK_RATE = 60;
export const SERVER_URL = 'http://localhost:5000';
export const CONTROL_DEADZONE = 0.2;
export const SPRITE_SIZE = 64;
export const CATCH_RADIUS = 32;
export const AUDIO_KEYS = {
  CHASE: 'chase-theme',
  WIN: 'win-sound',
  LOSE: 'lose-sound'
};
export const EVENTS = {
  PLAYER_MOVE: 'player_move',
  POSITION_SNAPSHOT: 'position_snapshot',
  MATCH_END: 'match_end',
  TIME_LEFT: 'time_left',
  POWERUP_SPAWN: 'powerup_spawn'
};
