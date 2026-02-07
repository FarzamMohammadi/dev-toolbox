/**
 * SVG Tracer
 * Wraps Motion.dev's pathLength animation to draw SVG paths
 * with optional glow effects.
 */

/**
 * Animate SVG path drawing using Motion.dev
 * @param {SVGElement} svgElement - The SVG element containing paths
 * @param {object} opts
 * @param {number} [opts.duration=2] - Duration in seconds
 * @param {string} [opts.ease='easeInOut'] - Easing function
 * @param {number} [opts.stagger=0] - Stagger delay between paths in seconds
 * @param {string} [opts.glowColor] - CSS color for glow effect (e.g. '#06b6d4')
 * @param {number} [opts.glowSize=8] - Glow radius in px
 * @param {boolean} [opts.fillAfter=false] - Fill paths after tracing
 * @param {function} animate - Motion.dev animate function (passed from scene)
 * @returns {object} Motion.dev animation controls
 */
export function traceSVG(svgElement, opts = {}, animate) {
  const {
    duration = 2,
    ease = 'easeInOut',
    stagger: staggerDelay = 0,
    glowColor,
    glowSize = 8,
    fillAfter = false,
  } = opts;

  // Find all drawable path elements
  const pathSelectors = 'path, line, polyline, polygon, circle, ellipse, rect';
  const paths = svgElement.querySelectorAll(pathSelectors);

  // Prepare paths: set initial state
  paths.forEach(path => {
    // For non-path elements that don't support pathLength natively,
    // we rely on Motion.dev handling them
    if (path.tagName === 'path' || path.tagName === 'line' ||
        path.tagName === 'polyline' || path.tagName === 'polygon') {
      const length = path.getTotalLength?.() || 0;
      if (length > 0) {
        path.style.strokeDasharray = length;
        path.style.strokeDashoffset = length;
      }
    }
    // Ensure stroke is visible
    if (!path.getAttribute('stroke') && !path.style.stroke) {
      path.style.stroke = 'currentColor';
    }
    if (path.style.fill === '' && !path.getAttribute('fill')) {
      path.style.fill = 'none';
    }
  });

  // Apply glow
  if (glowColor) {
    svgElement.style.filter = `drop-shadow(0 0 ${glowSize}px ${glowColor}) drop-shadow(0 0 ${glowSize * 2}px ${glowColor})`;
  }

  // Use Motion.dev's pathLength if available, otherwise fall back to strokeDashoffset
  if (animate) {
    // Build a sequence for staggered drawing
    if (staggerDelay > 0 && paths.length > 1) {
      const sequence = Array.from(paths).map((path, i) => [
        path,
        { strokeDashoffset: [path.getTotalLength?.() || 0, 0] },
        {
          duration,
          ease,
          at: i * staggerDelay,
        },
      ]);
      return animate(sequence);
    }

    // Animate all paths together
    return animate(paths, {
      strokeDashoffset: 0,
    }, {
      duration,
      ease,
    });
  }

  // Fallback: CSS animation without Motion.dev
  paths.forEach((path, i) => {
    path.style.transition = `stroke-dashoffset ${duration}s ${ease} ${i * staggerDelay}s`;
    requestAnimationFrame(() => {
      path.style.strokeDashoffset = '0';
    });
  });

  return { paths };
}
