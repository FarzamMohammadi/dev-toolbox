/**
 * Scene Controller
 * Manages scene lifecycle: play, pause, restart, timing.
 * Each scene HTML file creates one scene instance.
 */

export function initScene(config = {}) {
  const {
    name = 'Untitled Scene',
    duration = 10,
  } = config;

  let state = 'idle'; // idle | playing | paused | complete
  let startTime = null;
  let elapsed = 0;
  let pausedAt = 0;
  let rafId = null;

  const callbacks = {
    play: [],
    pause: [],
    restart: [],
    tick: [],
    complete: [],
  };

  function currentTime() {
    if (state === 'playing') {
      return (performance.now() - startTime) / 1000;
    }
    return pausedAt;
  }

  function tick() {
    if (state !== 'playing') return;
    elapsed = currentTime();
    callbacks.tick.forEach(fn => fn(elapsed));
    if (elapsed >= duration) {
      state = 'complete';
      callbacks.complete.forEach(fn => fn());
      return;
    }
    rafId = requestAnimationFrame(tick);
  }

  const scene = {
    name,
    duration,

    get state() { return state; },
    get currentTime() { return currentTime(); },
    get elapsed() { return elapsed; },

    play() {
      if (state === 'playing') return;
      if (state === 'idle' || state === 'complete') {
        startTime = performance.now();
        pausedAt = 0;
      } else if (state === 'paused') {
        startTime = performance.now() - (pausedAt * 1000);
      }
      state = 'playing';
      callbacks.play.forEach(fn => fn());
      rafId = requestAnimationFrame(tick);
    },

    pause() {
      if (state !== 'playing') return;
      pausedAt = currentTime();
      state = 'paused';
      if (rafId) cancelAnimationFrame(rafId);
      callbacks.pause.forEach(fn => fn());
    },

    restart() {
      if (rafId) cancelAnimationFrame(rafId);
      startTime = null;
      elapsed = 0;
      pausedAt = 0;
      state = 'idle';
      callbacks.restart.forEach(fn => fn());
    },

    onPlay(fn) { callbacks.play.push(fn); },
    onPause(fn) { callbacks.pause.push(fn); },
    onRestart(fn) { callbacks.restart.push(fn); },
    onTick(fn) { callbacks.tick.push(fn); },
    onComplete(fn) { callbacks.complete.push(fn); },
  };

  return scene;
}
