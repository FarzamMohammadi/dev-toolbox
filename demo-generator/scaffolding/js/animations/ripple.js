/**
 * Ripple
 * Creates expanding concentric circles from a point.
 * Great for logo drops, emphasis moments, beat hits.
 */

/**
 * Create an expanding ripple effect
 * @param {HTMLElement} container - Parent element (should be position: relative)
 * @param {object} opts
 * @param {number} [opts.count=3] - Number of ripple rings
 * @param {number} [opts.duration=1.5] - Duration per ring in seconds
 * @param {string} [opts.color='rgba(59, 130, 246, 0.4)'] - Ring color
 * @param {number} [opts.maxRadius=300] - Maximum radius in px
 * @param {number} [opts.strokeWidth=2] - Ring stroke width
 * @param {number} [opts.stagger=0.2] - Delay between rings in seconds
 * @param {{ x: number, y: number }} [opts.origin] - Center point (defaults to container center)
 * @param {function} [opts.onComplete] - Callback when all rings finish
 * @param {function} animate - Motion.dev animate function
 * @returns {{ element: SVGElement, play: Function }}
 */
export function ripple(container, opts = {}, animate) {
  const {
    count = 3,
    duration = 1.5,
    color = 'rgba(59, 130, 246, 0.4)',
    maxRadius = 300,
    strokeWidth = 2,
    stagger: staggerDelay = 0.2,
    origin,
    onComplete,
  } = opts;

  const rect = container.getBoundingClientRect();
  const cx = origin?.x ?? rect.width / 2;
  const cy = origin?.y ?? rect.height / 2;

  // Create SVG overlay
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', rect.width);
  svg.setAttribute('height', rect.height);
  svg.style.position = 'absolute';
  svg.style.top = '0';
  svg.style.left = '0';
  svg.style.pointerEvents = 'none';
  svg.style.overflow = 'visible';

  const circles = [];
  for (let i = 0; i < count; i++) {
    const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    circle.setAttribute('cx', cx);
    circle.setAttribute('cy', cy);
    circle.setAttribute('r', 0);
    circle.setAttribute('fill', 'none');
    circle.setAttribute('stroke', color);
    circle.setAttribute('stroke-width', strokeWidth);
    circle.style.opacity = '0';
    svg.appendChild(circle);
    circles.push(circle);
  }

  container.appendChild(svg);

  function play() {
    if (animate) {
      const sequence = circles.flatMap((circle, i) => [
        [circle, { r: [0, maxRadius], opacity: [0.8, 0] }, {
          duration,
          ease: 'easeOut',
          at: i * staggerDelay,
        }],
      ]);
      const controls = animate(sequence);
      if (onComplete) {
        controls.finished?.then(onComplete);
      }
      return controls;
    }

    // CSS fallback
    circles.forEach((circle, i) => {
      circle.style.transition = `r ${duration}s ease-out ${i * staggerDelay}s, opacity ${duration}s ease-out ${i * staggerDelay}s`;
      requestAnimationFrame(() => {
        circle.setAttribute('r', maxRadius);
        circle.style.opacity = '0';
      });
    });
  }

  return { element: svg, play, circles };
}
