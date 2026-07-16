# WP Engine embed codes — TO26 interactive figures

2026-07-16. Four representative embeds (3 figures + 1 table) for the WP
Engine site. Base URL: `https://irpp-study-to-ctpskills-authorpackage.pages.dev/`
(Cloudflare Pages; auto-deploys from the repo's main branch, so embeds always
serve the latest published state).

**Use the extensionless URLs** — Pages 308-redirects `…/A3_map.html` to
`…/A3_map`; linking the canonical form avoids the extra hop inside an iframe.

## 1. Resize listener — once per page (site-wide footer or the post template)

Each figure reports its rendered size to the parent page after load via
`postMessage`. This listener sets each iframe's height to match, so figures
are never clipped and never scroll internally. It is origin-locked to the
figure host.

```html
<script>
(function () {
  var FIGURE_ORIGIN = 'https://irpp-study-to-ctpskills-authorpackage.pages.dev';
  window.addEventListener('message', function (e) {
    if (e.origin !== FIGURE_ORIGIN) return;
    if (!e.data || e.data.type !== 'figure-sized') return;
    var frames = document.querySelectorAll('iframe.ctp-figure');
    for (var i = 0; i < frames.length; i++) {
      if (frames[i].contentWindow === e.source) {
        frames[i].style.height = e.data.height + 'px';
      }
    }
  });
})();
</script>
```

## 2. The iframes

All figures are built at 550px width and centre themselves in narrower
columns; below **440px of iframe width** they switch automatically to the
compact (phone) layout. The inline `height` is only a pre-load placeholder —
the listener above corrects it.

### Figure 2 — Susceptible communities and occupations (interactive map)

```html
<iframe class="ctp-figure"
  src="https://irpp-study-to-ctpskills-authorpackage.pages.dev/figures/A3_map"
  title="Figure 2 — Susceptible communities and occupations (interactive map)"
  style="width:100%; max-width:550px; height:420px; border:0; display:block; margin:0 auto;"
  loading="lazy" scrolling="no"></iframe>
```

### Table 2 — Viable occupations by community

```html
<iframe class="ctp-figure"
  src="https://irpp-study-to-ctpskills-authorpackage.pages.dev/figures/E2_viable_table"
  title="Table 2 — Viable occupations by community"
  style="width:100%; max-width:550px; height:640px; border:0; display:block; margin:0 auto;"
  loading="lazy" scrolling="no"></iframe>
```

### Figure 5 — Major skills gaps (RCA bars)

```html
<iframe class="ctp-figure"
  src="https://irpp-study-to-ctpskills-authorpackage.pages.dev/figures/I_skills_gap_bars"
  title="Figure 5 — Major skills gaps between susceptible and viable occupations"
  style="width:100%; max-width:550px; height:480px; border:0; display:block; margin:0 auto;"
  loading="lazy" scrolling="no"></iframe>
```

### Figure 7 — Material handlers: an illustrative example (walkthrough)

```html
<iframe class="ctp-figure"
  src="https://irpp-study-to-ctpskills-authorpackage.pages.dev/figures/D2_walkthrough"
  title="Figure 7 — Material handlers in Oxford: an illustrative walkthrough"
  style="width:100%; max-width:550px; height:820px; border:0; display:block; margin:0 auto;"
  loading="lazy" scrolling="no"></iframe>
```

## Notes for the web team

- **Controls are inside the figures** (community/occupation dropdowns,
  tooltips) — no WP-side UI needed.
- **One standard sentence** belongs in each figure's notes block on the WP
  side (per the mobile ruling): *"Simplified view — the full interactive
  figure is best on a larger screen."* It lives in the page copy, never in
  the graphic.
- **Static fallbacks**: print-resolution PNGs of each figure's default state
  are served at `…pages.dev/exports/<name>.png` (e.g. `exports/A3_map.png`),
  1100px wide (2×).
- The size message fires on load (and when a figure internally re-renders);
  if live *window*-resizing must also re-flow heights, tell us — the helper
  can re-emit on resize.
- Remaining figures follow the same pattern:
  `figures/C2_summary`, `figures/G2_oasis_competencies` (Table 1),
  `figures/B2_suitable_heatmap` (Figure 3), `figures/F2_filtering`
  (Figure 4), `figures/J_skills_gap_table` (Figure 6).
- Colour work is still in progress (theme v2); embeds will restyle
  automatically on our next pushes — no embed-code changes needed.
