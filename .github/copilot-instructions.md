# Copilot Instructions for Tom & Jerry Chase Game

## Big Picture Architecture
- **Frontend (`frontend/`)**: React + Vite app. Handles UI, game canvas, character selection, controls, sound, and local leaderboard. Communicates with backend via Socket.IO and REST APIs.
- **Backend (`backend/`)**: Python Flask app. Manages game state, player sessions, AI logic, real-time events, and persistent leaderboard. Organized into API routes, game logic, models, sockets, and utilities.
- **Real-Time Sync**: Multiplayer and solo modes use Socket.IO for instant updates. AI fills in for solo play.
- **Offline Support**: Service worker enables offline play and local leaderboard/history.

## Developer Workflows
- **Frontend**
  - Install: `npm install` in `frontend/`
  - Run dev server: `npm run dev` in `frontend/`
  - Build: `npm run build` in `frontend/`
  - Entry: `src/main.jsx`, main UI: `src/components/GameCanvas.jsx`, context: `src/context/`
- **Backend**
  - Install: `pip install -r backend/requirements.txt`
  - Run: `python3 backend/app.py`
  - Main entry: `backend/app.py`, routes: `backend/api/`, game logic: `backend/game_logic/`

## Project-Specific Patterns
- **Frontend**
  - Context API for global state: see `src/context/`
  - Custom hooks for socket, auth, controls: see `src/hooks/`
  - Game loop and rendering: `GameCanvas.jsx`, uses requestAnimationFrame
  - Sound: `SoundContext.jsx` manages music/effects, adapts to game state
  - Service worker: `public/sw.js` for offline and caching
- **Backend**
  - API routes: `backend/api/` (auth, game, leaderboard, player)
  - Game logic: `backend/game_logic/` (AI, physics, collision, powerups)
  - Models: `backend/models/` (game, player, score)
  - Sockets: `backend/sockets/` (events, socket manager)
  - Utilities: `backend/utils/` (JWT, cache, serialization)

## Integration Points
- **Socket.IO**: Used for real-time game events (moves, collisions, results)
- **REST APIs**: For leaderboard, player data, authentication
- **AI Controller**: `backend/game_logic/ai_controller.py` for solo mode
- **Service Worker**: `frontend/public/sw.js` for offline and asset caching

## Conventions & Patterns
- **No login required**: Game starts instantly, but local leaderboard/history is tracked
- **Component-based UI**: React components for each screen/feature
- **Separation of concerns**: API, game logic, models, sockets, and utilities are in distinct folders
- **Local-first**: Leaderboard and history stored locally, syncs with backend when online

## Examples
- To add a new powerup: update `backend/game_logic/powerups.py` and sync frontend visuals in `GameCanvas.jsx`
- To add a new leaderboard stat: update `backend/models/score_model.py` and API in `backend/api/leaderboard.py`, then update frontend display in `src/components/ScoreBoard.jsx`

## Key Files & Directories
- `frontend/src/components/GameCanvas.jsx`: Main game rendering
- `frontend/src/context/SoundContext.jsx`: Sound/music management
- `backend/app.py`: Flask app entry point
- `backend/game_logic/ai_controller.py`: AI logic for solo play
- `backend/api/game_routes.py`: Game event API
- `backend/sockets/socket_manager.py`: Real-time event handling

---
For unclear or missing conventions, ask the user for clarification or examples from recent code changes.