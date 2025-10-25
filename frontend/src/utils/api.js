// frontend/src/utils/api.js
// HTTP client wrapper for game API
const BASE_URL = '/api';

async function request(path, opts = {}) {
  for (let i = 0; i < 3; i++) {
    try {
      const res = await fetch(BASE_URL + path, opts);
      if (!res.ok) throw new Error('API error');
      return await res.json();
    } catch (e) {
      if (i === 2) throw e;
    }
  }
}

export default {
  startGame: opts => request('/start', { method: 'POST', body: JSON.stringify(opts) }),
  restartGame: matchId => request(`/restart/${matchId}`, { method: 'POST' }),
  saveScore: stats => request('/score', { method: 'POST', body: JSON.stringify(stats) }),
  getLeaderboard: ({ limit = 20, offset = 0 } = {}) => request(`/leaderboard?limit=${limit}&offset=${offset}`)
};
