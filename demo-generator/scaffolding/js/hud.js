/**
 * HUD (Heads-Up Display) - Fine-tuning overlay
 * Provides transport controls, beat visualization, timing adjustments.
 * Press H to toggle visibility. Hidden during recording.
 */

const HUD_STYLES = `
  .hud {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: rgba(0, 0, 0, 0.85);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: 12px 20px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #ccc;
    z-index: 9999;
    transition: transform 0.3s ease;
    user-select: none;
  }
  .hud--hidden {
    transform: translateY(100%);
  }
  .hud-row {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  .hud-row + .hud-row {
    margin-top: 8px;
  }
  .hud-transport {
    display: flex;
    gap: 6px;
  }
  .hud-btn {
    padding: 4px 10px;
    border-radius: 4px;
    background: rgba(255, 255, 255, 0.1);
    color: #eee;
    font-size: 11px;
    font-family: inherit;
    cursor: pointer;
    transition: background 0.15s;
  }
  .hud-btn:hover {
    background: rgba(255, 255, 255, 0.2);
  }
  .hud-btn--active {
    background: rgba(59, 130, 246, 0.4);
  }
  .hud-time {
    font-variant-numeric: tabular-nums;
    min-width: 90px;
    color: #aaa;
  }
  .hud-label {
    color: #666;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
  .hud-beat-bar {
    flex: 1;
    height: 20px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 4px;
    position: relative;
    overflow: hidden;
  }
  .hud-beat-dot {
    position: absolute;
    top: 50%;
    width: 4px;
    height: 12px;
    background: rgba(59, 130, 246, 0.4);
    border-radius: 2px;
    transform: translateY(-50%);
  }
  .hud-beat-dot--downbeat {
    height: 16px;
    background: rgba(59, 130, 246, 0.7);
  }
  .hud-playhead {
    position: absolute;
    top: 0;
    bottom: 0;
    width: 2px;
    background: #fff;
    transition: none;
  }
  .hud-speed {
    display: flex;
    gap: 4px;
    align-items: center;
  }
  .hud-speed-btn {
    padding: 2px 6px;
    border-radius: 3px;
    background: rgba(255, 255, 255, 0.06);
    color: #888;
    font-size: 10px;
    font-family: inherit;
    cursor: pointer;
  }
  .hud-speed-btn--active {
    background: rgba(59, 130, 246, 0.3);
    color: #ccc;
  }
  .hud-hint {
    position: fixed;
    bottom: 8px;
    right: 12px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: rgba(255,255,255,0.2);
    z-index: 10000;
  }
`;

/**
 * Initialize the HUD overlay
 * @param {object} scene - Scene controller instance
 * @param {BeatTimeline|null} timeline - Optional beat timeline
 */
export function initHUD(scene, timeline = null) {
  // Inject styles
  const style = document.createElement('style');
  style.textContent = HUD_STYLES;
  document.head.appendChild(style);

  // Get or create HUD container
  let hud = document.getElementById('hud');
  if (!hud) {
    hud = document.createElement('div');
    hud.id = 'hud';
    document.body.appendChild(hud);
  }
  hud.className = 'hud';

  const totalDuration = timeline?.duration || scene.duration;
  const beatTimes = timeline?.beats?.beat_times || [];
  const downbeats = new Set(timeline?.beats?.downbeats || []);

  // Build beat dots for the timeline bar
  const beatDotsHTML = beatTimes.map(t => {
    const pct = (t / totalDuration) * 100;
    const cls = downbeats.has(t) ? 'hud-beat-dot hud-beat-dot--downbeat' : 'hud-beat-dot';
    return `<div class="${cls}" style="left:${pct}%"></div>`;
  }).join('');

  const speeds = [0.25, 0.5, 1, 1.5, 2];

  hud.innerHTML = `
    <div class="hud-row">
      <div class="hud-transport">
        <button class="hud-btn" data-action="play">Play</button>
        <button class="hud-btn" data-action="pause">Pause</button>
        <button class="hud-btn" data-action="restart">Restart</button>
      </div>
      <span class="hud-time" data-time>0.00s / ${totalDuration.toFixed(1)}s</span>
      <div class="hud-beat-bar" data-beatbar>
        <div class="hud-playhead" data-playhead></div>
        ${beatDotsHTML}
      </div>
      <div class="hud-speed">
        <span class="hud-label">Speed</span>
        ${speeds.map(s => `<button class="hud-speed-btn ${s === 1 ? 'hud-speed-btn--active' : ''}" data-speed="${s}">${s}x</button>`).join('')}
      </div>
    </div>
  `;

  // Hint for H key
  const hint = document.createElement('div');
  hint.className = 'hud-hint';
  hint.textContent = 'H to toggle HUD';
  document.body.appendChild(hint);

  // Element references
  const timeDisplay = hud.querySelector('[data-time]');
  const playhead = hud.querySelector('[data-playhead]');
  const beatbar = hud.querySelector('[data-beatbar]');

  // Transport controls
  hud.querySelector('[data-action="play"]').addEventListener('click', () => {
    scene.play();
    timeline?.play();
  });
  hud.querySelector('[data-action="pause"]').addEventListener('click', () => {
    scene.pause();
    timeline?.pause();
  });
  hud.querySelector('[data-action="restart"]').addEventListener('click', () => {
    scene.restart();
    timeline?.restart();
  });

  // Speed controls
  hud.querySelectorAll('[data-speed]').forEach(btn => {
    btn.addEventListener('click', () => {
      const speed = parseFloat(btn.dataset.speed);
      if (timeline) timeline.speed = speed;
      hud.querySelectorAll('[data-speed]').forEach(b => b.classList.remove('hud-speed-btn--active'));
      btn.classList.add('hud-speed-btn--active');
    });
  });

  // Update loop
  function updateHUD() {
    const t = timeline?.currentTime ?? scene.currentTime;
    timeDisplay.textContent = `${t.toFixed(2)}s / ${totalDuration.toFixed(1)}s`;
    const pct = Math.min((t / totalDuration) * 100, 100);
    playhead.style.left = `${pct}%`;
    requestAnimationFrame(updateHUD);
  }
  requestAnimationFrame(updateHUD);

  // Click on beat bar to seek (visual only - updates display)
  beatbar.addEventListener('click', (e) => {
    const rect = beatbar.getBoundingClientRect();
    const pct = (e.clientX - rect.left) / rect.width;
    const seekTo = pct * totalDuration;
    // For now, just show the time - full seeking requires more complex state management
    console.log(`Seek to: ${seekTo.toFixed(2)}s`);
  });

  // H key to toggle HUD visibility
  let hudVisible = true;
  document.addEventListener('keydown', (e) => {
    if (e.key === 'h' || e.key === 'H') {
      hudVisible = !hudVisible;
      hud.classList.toggle('hud--hidden', !hudVisible);
      hint.style.display = hudVisible ? '' : 'none';
    }
    if (e.key === ' ') {
      e.preventDefault();
      if (scene.state === 'playing') {
        scene.pause();
        timeline?.pause();
      } else {
        scene.play();
        timeline?.play();
      }
    }
    if (e.key === 'r' || e.key === 'R') {
      scene.restart();
      timeline?.restart();
    }
  });

  return hud;
}
