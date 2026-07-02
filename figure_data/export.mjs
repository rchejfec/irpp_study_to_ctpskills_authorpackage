/**
 * export.mjs — Export the wired dist/ figures to high-res PNG.
 *
 * Unlike the consolidated project's exporter, our figures fetch('../data/*.json')
 * at runtime, so they must be served over HTTP (browsers block fetch over file://).
 * This script spins up a tiny static server over dist/, renders each figure, and
 * screenshots the .figure-container at 2×.
 *
 * Per-metric figures (E, B, D, F2) are exported once per metric →
 *   <name>.cosine.png / <name>.euclidean.png
 * Shared/static figures export a single <name>.png.
 *
 * Usage:
 *   node figure_data/export.mjs                 # all figures, both metrics
 *   node figure_data/export.mjs E_viable_table  # one figure by name
 *   node figure_data/export.mjs --metric=cosine # restrict metric variants
 *
 * Puppeteer is resolved from the sibling study_TO26_consolidatingfigures package
 * (no node_modules in this package). Override with PUPPETEER_PATH if needed.
 */

import http from 'http';
import { readFile, readdir, mkdir } from 'fs/promises';
import { resolve, join, extname, basename, dirname } from 'path';
import { fileURLToPath, pathToFileURL } from 'url';
import { createRequire } from 'module';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Config ──
const DIST_DIR = resolve(__dirname, 'dist');
const FIGURES_DIR = join(DIST_DIR, 'figures');
const EXPORTS_DIR = resolve(__dirname, 'exports');
const DEVICE_SCALE_FACTOR = 2; // ~192 dpi

// Figures whose data is per-metric (fetch `<name>.<metric>.json`).
const METRIC_FIGURES = new Set([
  'E_viable_table', 'B_suitable_heatmap', 'D_walkthrough', 'F2_filtering',
]);
const METRICS = ['cosine', 'euclidean'];

const MIME = {
  '.html': 'text/html', '.css': 'text/css', '.json': 'application/json',
  '.svg': 'image/svg+xml', '.js': 'text/javascript', '.png': 'image/png',
};

// ── Resolve puppeteer from the sibling package ──
async function loadPuppeteer() {
  const candidates = [
    process.env.PUPPETEER_PATH,
    resolve(__dirname, '../../study_TO26_consolidatingfigures/node_modules/puppeteer'),
  ].filter(Boolean);
  for (const p of candidates) {
    try {
      const require = createRequire(join(p, 'package.json'));
      return require(p);
    } catch { /* try next */ }
  }
  // Last resort: bare import (works if run from a dir that resolves puppeteer)
  return (await import('puppeteer')).default;
}

// ── Tiny static server over dist/ ──
function startServer() {
  const server = http.createServer(async (req, res) => {
    const urlPath = decodeURIComponent(req.url.split('?')[0]);
    const fp = join(DIST_DIR, urlPath);
    if (!fp.startsWith(DIST_DIR)) { res.writeHead(403); return res.end(); }
    try {
      const data = await readFile(fp);
      res.writeHead(200, { 'Content-Type': MIME[extname(fp)] || 'application/octet-stream' });
      res.end(data);
    } catch {
      res.writeHead(404); res.end('not found');
    }
  });
  return new Promise(r => server.listen(0, () => r({ server, port: server.address().port })));
}

function log(msg) { console.log(`  ${msg}`); }

async function getFigureNames(specific) {
  const files = (await readdir(FIGURES_DIR))
    .filter(f => f.endsWith('.html') && !f.startsWith('_') && f !== 'index.html')
    .map(f => basename(f, '.html'))
    .sort();
  if (specific?.length) return files.filter(n => specific.includes(n));
  return files;
}

async function exportOne(browser, base, name, metric) {
  const suffix = metric ? `.${metric}` : '';
  const query = metric ? `?metric=${metric}` : '';
  const outputPath = join(EXPORTS_DIR, `${name}${suffix}.png`);
  const page = await browser.newPage();
  try {
    await page.goto(`${base}/figures/${name}.html${query}`, { waitUntil: 'networkidle0', timeout: 20000 });
    await page.evaluate(() => document.body.classList.add('export-mode'));
    await page.evaluate(() => document.fonts.ready);
    // Give async fetch renders a beat to paint.
    await new Promise(r => setTimeout(r, 300));
    const container = await page.$('.figure-container');
    if (!container) { log(`⚠  ${name}${suffix}: no .figure-container — skipping`); return false; }
    const box = await container.boundingBox();
    await page.screenshot({
      path: outputPath,
      clip: { x: box.x, y: box.y, width: box.width, height: box.height },
      omitBackground: false,
    });
    const w = Math.round(box.width * DEVICE_SCALE_FACTOR);
    const h = Math.round(box.height * DEVICE_SCALE_FACTOR);
    log(`✓  ${name}${suffix}.png  (${w}×${h}px @ ${DEVICE_SCALE_FACTOR}×)`);
    return true;
  } catch (err) {
    log(`✗  ${name}${suffix}: ${err.message}`);
    return false;
  } finally {
    await page.close();
  }
}

async function main() {
  const args = process.argv.slice(2);
  const metricFlag = args.find(a => a.startsWith('--metric='))?.split('=')[1];
  const names = args.filter(a => !a.startsWith('-'));

  console.log('\n📐 IRPP Figure Export (author package)\n');
  await mkdir(EXPORTS_DIR, { recursive: true });

  const figures = await getFigureNames(names.length ? names : null);
  if (!figures.length) { log('No figures found to export.'); process.exit(1); }

  const metrics = metricFlag ? [metricFlag] : METRICS;
  const jobs = figures.flatMap(name =>
    METRIC_FIGURES.has(name) ? metrics.map(m => [name, m]) : [[name, null]]
  );
  log(`Found ${figures.length} figure(s) → ${jobs.length} render(s)\n`);

  const puppeteer = await loadPuppeteer();
  const { server, port } = await startServer();
  const base = `http://localhost:${port}`;
  const browser = await puppeteer.launch({
    headless: true,
    defaultViewport: { width: 1200, height: 900, deviceScaleFactor: DEVICE_SCALE_FACTOR },
  });

  let success = 0, failed = 0;
  for (const [name, metric] of jobs) {
    (await exportOne(browser, base, name, metric)) ? success++ : failed++;
  }

  await browser.close();
  server.close();
  console.log(`\n  Done: ${success} exported${failed ? `, ${failed} failed` : ''}`);
  console.log(`  Output: ${EXPORTS_DIR}/\n`);
  process.exit(failed ? 1 : 0);
}

main().catch(err => { console.error('Export failed:', err); process.exit(1); });
