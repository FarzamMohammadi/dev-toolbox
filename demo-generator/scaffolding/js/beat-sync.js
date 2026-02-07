/**
 * Beat Sync
 * Loads beats.json from analyze-beats.py and provides a scheduling API
 * for syncing animations to musical beats.
 */

/**
 * Load and parse beats.json
 * @param {string} path - Path to beats.json
 * @returns {Promise<BeatData>}
 */
export async function loadBeats(path) {
  const res = await fetch(path);
  if (!res.ok) throw new Error(`Failed to load beats: ${res.status}`);
  return res.json();
}

/**
 * Create a fixed-timing BeatData object when no music is used.
 * @param {object} opts
 * @param {number} opts.bpm - Beats per minute (default 120)
 * @param {number} opts.duration - Total duration in seconds (default 30)
 * @returns {BeatData}
 */
export function createFixedBeats({ bpm = 120, duration = 30 } = {}) {
  const interval = 60 / bpm;
  const beatTimes = [];
  for (let t = 0; t < duration; t += interval) {
    beatTimes.push(Math.round(t * 1000) / 1000);
  }
  // Every 4th beat is a downbeat
  const downbeats = beatTimes.filter((_, i) => i % 4 === 0);
  return {
    bpm,
    duration,
    beat_times: beatTimes,
    onset_times: beatTimes,
    downbeats,
    sections: [{ start: 0, end: duration, label: 'full' }],
  };
}

/**
 * BeatTimeline - schedule callbacks at specific beats or times.
 * Uses requestAnimationFrame with a lookahead approach for precision.
 */
export class BeatTimeline {
  #beats;
  #scheduled = [];     // { time, callback, fired }
  #playing = false;
  #startTime = null;
  #pausedAt = 0;
  #rafId = null;
  #onBeatCallbacks = [];
  #lastBeatIndex = -1;
  #speedMultiplier = 1;
  #offsets = new Map(); // beatIndex -> offset in ms

  /**
   * @param {BeatData} beats - Beat data from loadBeats() or createFixedBeats()
   */
  constructor(beats) {
    this.#beats = beats;
  }

  get beats() { return this.#beats; }
  get isPlaying() { return this.#playing; }
  get bpm() { return this.#beats.bpm; }
  get duration() { return this.#beats.duration; }

  get currentTime() {
    if (!this.#playing || !this.#startTime) return this.#pausedAt;
    return ((performance.now() - this.#startTime) / 1000) * this.#speedMultiplier;
  }

  set speed(val) {
    if (this.#playing) {
      this.#pausedAt = this.currentTime;
      this.#startTime = performance.now();
    }
    this.#speedMultiplier = val;
  }

  get speed() { return this.#speedMultiplier; }

  /**
   * Schedule a callback at a specific beat index
   */
  at(beatIndex, callback) {
    const time = this.#beats.beat_times[beatIndex];
    if (time == null) {
      console.warn(`Beat index ${beatIndex} out of range (${this.#beats.beat_times.length} beats)`);
      return this;
    }
    const offset = (this.#offsets.get(beatIndex) || 0) / 1000;
    this.#scheduled.push({ time: time + offset, callback, fired: false, beatIndex });
    return this;
  }

  /**
   * Schedule a callback at an absolute time (seconds)
   */
  atTime(seconds, callback) {
    this.#scheduled.push({ time: seconds, callback, fired: false, beatIndex: null });
    return this;
  }

  /**
   * Schedule a callback at a specific downbeat index
   */
  atDownbeat(downbeatIndex, callback) {
    const time = this.#beats.downbeats?.[downbeatIndex];
    if (time == null) {
      console.warn(`Downbeat index ${downbeatIndex} out of range`);
      return this;
    }
    this.#scheduled.push({ time, callback, fired: false, beatIndex: null });
    return this;
  }

  /**
   * Register a callback that fires on every beat
   */
  onBeat(callback) {
    this.#onBeatCallbacks.push(callback);
    return this;
  }

  /**
   * Adjust the offset for a specific beat (used by HUD)
   * @param {number} beatIndex
   * @param {number} deltaMs - Offset in milliseconds
   */
  adjustOffset(beatIndex, deltaMs) {
    this.#offsets.set(beatIndex, deltaMs);
  }

  /**
   * Export current timing adjustments
   */
  exportTimings() {
    const offsets = {};
    this.#offsets.forEach((v, k) => { offsets[k] = v; });
    return { offsets, speed: this.#speedMultiplier };
  }

  play() {
    if (this.#playing) return;
    this.#playing = true;
    if (this.#pausedAt > 0) {
      this.#startTime = performance.now() - (this.#pausedAt * 1000 / this.#speedMultiplier);
    } else {
      this.#startTime = performance.now();
    }
    this.#tick();
  }

  pause() {
    this.#playing = false;
    this.#pausedAt = this.currentTime;
    if (this.#rafId) cancelAnimationFrame(this.#rafId);
  }

  restart() {
    this.#playing = false;
    if (this.#rafId) cancelAnimationFrame(this.#rafId);
    this.#startTime = null;
    this.#pausedAt = 0;
    this.#lastBeatIndex = -1;
    this.#scheduled.forEach(s => { s.fired = false; });
  }

  #tick() {
    if (!this.#playing) return;
    const now = this.currentTime;

    // Fire scheduled callbacks
    for (const entry of this.#scheduled) {
      if (!entry.fired && now >= entry.time) {
        entry.fired = true;
        try { entry.callback(now); } catch (e) { console.error('Beat callback error:', e); }
      }
    }

    // Fire onBeat callbacks
    const beatTimes = this.#beats.beat_times;
    for (let i = this.#lastBeatIndex + 1; i < beatTimes.length; i++) {
      if (now >= beatTimes[i]) {
        this.#lastBeatIndex = i;
        this.#onBeatCallbacks.forEach(fn => {
          try { fn(i, beatTimes[i]); } catch (e) { console.error('onBeat error:', e); }
        });
      } else {
        break;
      }
    }

    this.#rafId = requestAnimationFrame(() => this.#tick());
  }
}
