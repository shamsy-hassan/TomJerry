import React, { createContext, useState, useEffect, useCallback } from 'react';

export const SoundContext = createContext();

export const SoundProvider = ({ children }) => {
  const [isMuted, setIsMuted] = useState(() => localStorage.getItem('isMuted') === 'true');
  const [musicVolume, setMusicVolume] = useState(() => Number(localStorage.getItem('musicVolume') || 0.3));
  const [effectsVolume, setEffectsVolume] = useState(() => Number(localStorage.getItem('effectsVolume') || 0.5));

  useEffect(() => {
    localStorage.setItem('isMuted', isMuted);
    localStorage.setItem('musicVolume', musicVolume);
    localStorage.setItem('effectsVolume', effectsVolume);
  }, [isMuted, musicVolume, effectsVolume]);

  const playOneShot = useCallback((src) => {
    if (isMuted) return;
    const audio = new window.Audio(src);
    audio.volume = effectsVolume;
    audio.play();
  }, [isMuted, effectsVolume]);

  const toggleMute = useCallback(() => setIsMuted(m => !m), []);

  return (
    <SoundContext.Provider value={{
      isMuted,
      toggleMute,
      musicVolume,
      setMusicVolume,
      effectsVolume,
      setEffectsVolume,
      playOneShot
    }}>
      {children}
    </SoundContext.Provider>
  );
};
