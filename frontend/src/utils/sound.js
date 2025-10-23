// Audio manager using Howler or WebAudio
export function preload(list) {
  list.forEach(src => {
    const audio = new window.Audio(src);
    audio.load();
  });
}

export function play(id, { volume = 0.5 } = {}) {
  const audio = new window.Audio(id);
  audio.volume = volume;
  audio.play();
}

export function stop(id) {
  // Not implemented for basic Audio API
}

export function setVolume(channel, value) {
  // Not implemented for basic Audio API
}
