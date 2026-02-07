/**
 * Fade Slide
 * Simple entrance/exit animations with fade + directional movement.
 * Wraps Motion.dev animate() with sensible defaults.
 */

const DIRECTIONS = {
  up:    { y: [30, 0] },
  down:  { y: [-30, 0] },
  left:  { x: [30, 0] },
  right: { x: [-30, 0] },
};

/**
 * Fade + slide an element in from a direction
 * @param {string|HTMLElement|NodeList} target - CSS selector, element, or node list
 * @param {object} opts
 * @param {'up'|'down'|'left'|'right'} [opts.direction='up'] - Slide direction
 * @param {number} [opts.duration=0.6] - Duration in seconds
 * @param {string} [opts.ease='easeOut'] - Easing
 * @param {number} [opts.stagger=0.1] - Stagger delay between multiple elements
 * @param {number} [opts.distance=30] - Slide distance in px
 * @param {function} animate - Motion.dev animate function
 * @returns {object} Motion.dev animation controls
 */
export function fadeSlide(target, opts = {}, animate) {
  const {
    direction = 'up',
    duration = 0.6,
    ease = 'easeOut',
    stagger: staggerDelay = 0.1,
    distance = 30,
  } = opts;

  // Build directional keyframes
  const axis = (direction === 'up' || direction === 'down') ? 'y' : 'x';
  const sign = (direction === 'down' || direction === 'right') ? -1 : 1;
  const keyframes = {
    opacity: [0, 1],
    [axis]: [distance * sign, 0],
  };

  if (animate) {
    // Check if target matches multiple elements (for stagger)
    if (typeof target === 'string') {
      const elements = document.querySelectorAll(target);
      if (elements.length > 1) {
        return animate(target, keyframes, {
          duration,
          ease,
          delay: staggerDelay > 0
            ? (i) => i * staggerDelay
            : 0,
        });
      }
    }

    return animate(target, keyframes, { duration, ease });
  }

  // CSS fallback
  const elements = typeof target === 'string'
    ? document.querySelectorAll(target)
    : target instanceof NodeList ? target : [target];

  Array.from(elements).forEach((el, i) => {
    el.style.opacity = '0';
    el.style.transform = `translate${axis.toUpperCase()}(${distance * sign}px)`;
    el.style.transition = `opacity ${duration}s ${ease} ${i * staggerDelay}s, transform ${duration}s ${ease} ${i * staggerDelay}s`;
    requestAnimationFrame(() => {
      el.style.opacity = '1';
      el.style.transform = 'none';
    });
  });
}

/**
 * Fade out + slide away
 */
export function fadeSlideOut(target, opts = {}, animate) {
  const {
    direction = 'up',
    duration = 0.4,
    ease = 'easeIn',
    distance = 30,
  } = opts;

  const axis = (direction === 'up' || direction === 'down') ? 'y' : 'x';
  const sign = (direction === 'up' || direction === 'left') ? -1 : 1;
  const keyframes = {
    opacity: [1, 0],
    [axis]: [0, distance * sign],
  };

  if (animate) {
    return animate(target, keyframes, { duration, ease });
  }
}
