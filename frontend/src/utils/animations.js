// GSAP animation presets

// Animation helpers for UI transitions and sprite tweens
export function tweenShake(target, intensity = 1, duration = 300) {
  return new Promise(resolve => {
    const orig = target.style.transform;
    target.style.transition = `transform ${duration}ms`;
    target.style.transform = `translateX(${intensity * 8}px)`;
    setTimeout(() => {
      target.style.transform = orig;
      resolve();
    }, duration);
  });
}

export function tweenPopIn(el, duration = 400) {
  return new Promise(resolve => {
    el.style.transition = `transform ${duration}ms`;
    el.style.transform = 'scale(1.2)';
    setTimeout(() => {
      el.style.transform = 'scale(1)';
      resolve();
    }, duration);
  });
}
