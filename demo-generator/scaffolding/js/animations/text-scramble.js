/**
 * Text Scramble
 * Decodes text character by character from random glyphs to the target string.
 * Free replacement for paid ScrambleText plugins.
 */

const DEFAULT_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{}|;:,.<>?';

/**
 * Scramble text effect - progressively reveals target text
 * @param {HTMLElement} element - Target element
 * @param {object} opts
 * @param {string} [opts.text] - Target text (defaults to element's textContent)
 * @param {number} [opts.duration=1500] - Total duration in ms
 * @param {string} [opts.characters] - Character set for scramble
 * @param {number} [opts.scrambleSpeed=30] - Ms between scramble frames
 * @param {function} [opts.onComplete] - Callback when done
 * @returns {{ play: Function, cancel: Function, promise: Promise }}
 */
export function scrambleText(element, opts = {}) {
  const {
    text = element.textContent,
    duration = 1500,
    characters = DEFAULT_CHARS,
    scrambleSpeed = 30,
    onComplete,
  } = opts;

  let cancelled = false;
  let intervalId = null;
  let resolvePromise;

  const promise = new Promise(resolve => { resolvePromise = resolve; });

  function randomChar() {
    return characters[Math.floor(Math.random() * characters.length)];
  }

  function run() {
    const len = text.length;
    const revealDuration = duration;
    const startTime = performance.now();
    element.textContent = Array.from({ length: len }, () => randomChar()).join('');

    intervalId = setInterval(() => {
      if (cancelled) {
        clearInterval(intervalId);
        return;
      }

      const elapsed = performance.now() - startTime;
      const progress = Math.min(elapsed / revealDuration, 1);
      const revealedCount = Math.floor(progress * len);

      const result = [];
      for (let i = 0; i < len; i++) {
        if (text[i] === ' ') {
          result.push(' ');
        } else if (i < revealedCount) {
          result.push(text[i]);
        } else {
          result.push(randomChar());
        }
      }
      element.textContent = result.join('');

      if (progress >= 1) {
        clearInterval(intervalId);
        element.textContent = text;
        onComplete?.();
        resolvePromise();
      }
    }, scrambleSpeed);
  }

  return {
    play() {
      cancelled = false;
      run();
    },
    cancel() {
      cancelled = true;
      if (intervalId) clearInterval(intervalId);
    },
    promise,
  };
}

/**
 * Scramble multiple elements in sequence with stagger
 * @param {NodeList|HTMLElement[]} elements
 * @param {object} opts - Same as scrambleText opts
 * @param {number} [staggerMs=200] - Delay between each element start
 * @returns {Promise} - Resolves when all complete
 */
export function scrambleStagger(elements, opts = {}, staggerMs = 200) {
  const els = Array.from(elements);
  return new Promise(resolve => {
    let completed = 0;
    els.forEach((el, i) => {
      setTimeout(() => {
        const s = scrambleText(el, {
          ...opts,
          onComplete: () => {
            completed++;
            if (completed === els.length) resolve();
          },
        });
        s.play();
      }, i * staggerMs);
    });
  });
}
