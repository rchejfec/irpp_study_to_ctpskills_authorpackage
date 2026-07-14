/**
 * compact.js — shared compact-mode runtime (mobile workstream, 2026-07-08)
 *
 * Contract (agreed 2026-07-08, see HANDOFF/TARGET_SPEC §3):
 *  - Compact fires below 440px of the iframe's OWN width, evaluated live.
 *    WordPress keeps one embed per figure; the figure decides its mode.
 *  - Sets `compact` class on <html>; every compact style is scoped under
 *    `html.compact` so desktop rendering is byte-identical without it.
 *  - Dispatches `compactmodechange` on window for JS-rendered figures.
 *  - Re-posts the figure-sized message after a mode switch so iframe
 *    hosts resize.
 *  - Touch devices (any mode, any width): tippy tooltips become
 *    tap-to-toggle. Keyed to input capability, NOT to the breakpoint.
 *
 * Load AFTER the tippy <script> tags and BEFORE the figure's own script.
 */
(function () {
  var BREAKPOINT = 440; /* was 640 — lowered for 550px desktop width (print-sizing) */
  var root = document.documentElement;
  var compact = null;

  function apply() {
    var next = root.clientWidth < BREAKPOINT;
    if (next === compact) return;
    var isSwitch = compact !== null;
    compact = next;
    root.classList.toggle('compact', compact);
    if (isSwitch) {
      window.dispatchEvent(new CustomEvent('compactmodechange', { detail: { compact: compact } }));
      // Let the re-render/reflow settle, then tell the host our new size.
      requestAnimationFrame(function () { requestAnimationFrame(reportSizeGeneric); });
    }
  }

  function reportSizeGeneric() {
    if (window.self === window.top) return;
    var c = document.querySelector('.figure-container') || document.querySelector('.appendix');
    if (!c) return;
    var fig = location.pathname.split('/').pop().replace('.html', '');
    parent.postMessage({ type: 'figure-sized', fig: fig, width: c.scrollWidth, height: c.scrollHeight }, '*');
  }

  window.isCompact = function () { return !!compact; };

  // Tap-to-toggle tooltips on hover-less devices. `hideOnClick: true`
  // dismisses on tap-outside, so only one stays open at a time.
  var coarse = window.matchMedia('(hover: none)').matches;
  if (coarse && typeof tippy !== 'undefined' && tippy.setDefaultProps) {
    tippy.setDefaultProps({ trigger: 'click', hideOnClick: true, touch: true });
  }

  window.addEventListener('resize', apply);
  apply();
})();
