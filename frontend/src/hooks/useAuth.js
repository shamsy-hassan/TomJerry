export default function useLocalSession() {
  const deviceId = localStorage.getItem('deviceId') || (() => {
    const id = 'dev-' + Math.random().toString(36).slice(2, 10);
    localStorage.setItem('deviceId', id);
    return id;
  })();
  const lastCharacter = localStorage.getItem('lastCharacter');
  const preferences = JSON.parse(localStorage.getItem('preferences') || '{}');

  function setPreference(key, value) {
    const prefs = { ...preferences, [key]: value };
    localStorage.setItem('preferences', JSON.stringify(prefs));
  }

  function resetLocalSession() {
    localStorage.removeItem('deviceId');
    localStorage.removeItem('lastCharacter');
    localStorage.removeItem('preferences');
  }

  return { deviceId, lastCharacter, preferences, setPreference, resetLocalSession };
}
