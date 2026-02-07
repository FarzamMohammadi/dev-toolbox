/**
 * Counter
 * Animates a number counting up or down.
 * Great for stats, metrics, percentages.
 */

/**
 * Animate a number from start to end
 * @param {HTMLElement} element - Target element
 * @param {number} from - Start value
 * @param {number} to - End value
 * @param {object} opts
 * @param {number} [opts.duration=1500] - Duration in ms
 * @param {string} [opts.prefix=''] - Text before number (e.g. '$')
 * @param {string} [opts.suffix=''] - Text after number (e.g. '%')
 * @param {number} [opts.decimals=0] - Decimal places
 * @param {'easeOut'|'easeInOut'|'linear'} [opts.easing='easeOut'] - Easing function
 * @param {function} [opts.onComplete] - Callback when done
 * @returns {{ play: Function, cancel: Function, promise: Promise }}
 */
export function countUp(element, from, to, opts = {}) {
  const {
    duration = 1500,
    prefix = '',
    suffix = '',
    decimals = 0,
    easing = 'easeOut',
    onComplete,
  } = opts;

  let cancelled = false;
  let rafId = null;
  let resolvePromise;

  const promise = new Promise(resolve => { resolvePromise = resolve; });

  const easingFns = {
    linear: t => t,
    easeOut: t => 1 - Math.pow(1 - t, 3),
    easeInOut: t => t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2,
  };

  const ease = easingFns[easing] || easingFns.easeOut;

  function format(val) {
    return `${prefix}${val.toFixed(decimals)}${suffix}`;
  }

  function run() {
    const startTime = performance.now();
    element.textContent = format(from);

    function tick() {
      if (cancelled) return;
      const elapsed = performance.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easedProgress = ease(progress);
      const current = from + (to - from) * easedProgress;

      element.textContent = format(current);

      if (progress < 1) {
        rafId = requestAnimationFrame(tick);
      } else {
        element.textContent = format(to);
        onComplete?.();
        resolvePromise();
      }
    }

    rafId = requestAnimationFrame(tick);
  }

  return {
    play() {
      cancelled = false;
      run();
    },
    cancel() {
      cancelled = true;
      if (rafId) cancelAnimationFrame(rafId);
    },
    promise,
  };
}
