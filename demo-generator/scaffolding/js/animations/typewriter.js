/**
 * Typewriter
 * Terminal-style character-by-character typing with blinking cursor.
 */

/**
 * Type text into an element character by character
 * @param {HTMLElement} element - Target element (should be inside a .terminal-body or similar)
 * @param {string} text - Text to type
 * @param {object} opts
 * @param {number} [opts.speed=50] - Ms per character
 * @param {boolean} [opts.cursor=true] - Show blinking cursor
 * @param {string} [opts.cursorChar='_'] - Cursor character
 * @param {boolean} [opts.sound=false] - Play keystroke sound
 * @param {function} [opts.onComplete] - Callback when done
 * @returns {{ play: Function, cancel: Function, promise: Promise }}
 */
export function typewrite(element, text, opts = {}) {
  const {
    speed = 50,
    cursor = true,
    cursorChar = '_',
    sound = false,
    onComplete,
  } = opts;

  let cancelled = false;
  let timeoutId = null;
  let cursorEl = null;
  let resolvePromise;

  const promise = new Promise(resolve => { resolvePromise = resolve; });

  // Audio context for keystroke sounds
  let audioCtx = null;
  if (sound && typeof AudioContext !== 'undefined') {
    audioCtx = new AudioContext();
  }

  function playKeystroke() {
    if (!audioCtx) return;
    const osc = audioCtx.createOscillator();
    const gain = audioCtx.createGain();
    osc.connect(gain);
    gain.connect(audioCtx.destination);
    osc.frequency.value = 800 + Math.random() * 400;
    gain.gain.value = 0.02;
    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);
    osc.start();
    osc.stop(audioCtx.currentTime + 0.05);
  }

  function run() {
    element.textContent = '';

    if (cursor) {
      cursorEl = document.createElement('span');
      cursorEl.textContent = cursorChar;
      cursorEl.style.animation = 'blink 0.7s step-end infinite';
      // Inject blink keyframes if not present
      if (!document.getElementById('typewriter-blink-style')) {
        const s = document.createElement('style');
        s.id = 'typewriter-blink-style';
        s.textContent = '@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0; } }';
        document.head.appendChild(s);
      }
    }

    let index = 0;

    function typeNext() {
      if (cancelled) return;
      if (index >= text.length) {
        if (cursorEl) cursorEl.remove();
        onComplete?.();
        resolvePromise();
        return;
      }

      element.textContent += text[index];
      if (cursorEl) element.appendChild(cursorEl);
      if (sound) playKeystroke();
      index++;

      // Vary speed slightly for naturalism
      const variance = speed * 0.4;
      const nextDelay = speed + (Math.random() - 0.5) * variance;
      timeoutId = setTimeout(typeNext, Math.max(10, nextDelay));
    }

    typeNext();
  }

  return {
    play() {
      cancelled = false;
      run();
    },
    cancel() {
      cancelled = true;
      if (timeoutId) clearTimeout(timeoutId);
      if (cursorEl) cursorEl.remove();
    },
    promise,
  };
}

/**
 * Type multiple lines sequentially
 * @param {HTMLElement} container - Parent container
 * @param {string[]} lines - Array of lines to type
 * @param {object} opts - Same as typewrite opts
 * @param {number} [lineDelay=300] - Delay between lines in ms
 * @returns {Promise}
 */
export function typewriteLines(container, lines, opts = {}, lineDelay = 300) {
  return new Promise(async (resolve) => {
    for (let i = 0; i < lines.length; i++) {
      const lineEl = document.createElement('div');
      container.appendChild(lineEl);
      const tw = typewrite(lineEl, lines[i], opts);
      tw.play();
      await tw.promise;
      if (i < lines.length - 1) {
        await new Promise(r => setTimeout(r, lineDelay));
      }
    }
    resolve();
  });
}
