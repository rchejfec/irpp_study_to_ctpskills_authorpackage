/**
 * export.mjs — Export figures to high-res PNG
 *
 * Usage:
 *   bun run export.mjs                    # Export all figures
 *   bun run export.mjs A_map              # Export a single figure by name
 *   bun run export.mjs A_map B_overview   # Export multiple specific figures
 *
 * Output: exports/<name>.png at 2× resolution (e.g., 1360×840 for standard figures)
 */

import puppeteer from 'puppeteer';
import { readdir } from 'fs/promises';
import { resolve, basename, extname } from 'path';

// ── Config ──
const FIGURES_DIR = resolve(import.meta.dirname, 'figures');
const EXPORTS_DIR = resolve(import.meta.dirname, 'exports');
const DEVICE_SCALE_FACTOR = 2; // 2× for print-quality (~192 dpi)

// ── Helpers ──
function log(msg) {
  console.log(`  ${msg}`);
}

async function getFigureFiles(specificNames) {
  const allFiles = await readdir(FIGURES_DIR);
  const htmlFiles = allFiles
    .filter(f => f.endsWith('.html') && !f.startsWith('_') && f !== 'index.html')
    .sort();

  if (specificNames && specificNames.length > 0) {
    return htmlFiles.filter(f => {
      const name = basename(f, '.html');
      return specificNames.includes(name) || specificNames.includes(f);
    });
  }

  return htmlFiles;
}

async function exportFigure(browser, filename) {
  const name = basename(filename, '.html');
  const filePath = resolve(FIGURES_DIR, filename);
  const outputPath = resolve(EXPORTS_DIR, `${name}.png`);

  const page = await browser.newPage();

  try {
    // Navigate to the file
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle0', timeout: 15000 });

    // Add export-mode class to strip dev wrapper styling
    await page.evaluate(() => document.body.classList.add('export-mode'));

    // Wait for fonts to load (Proxima Nova from Adobe Fonts / Typekit)
    await page.evaluate(() => document.fonts.ready);

    // Find the figure container
    const container = await page.$('.figure-container');
    if (!container) {
      log(`⚠  ${name}: No .figure-container found — skipping`);
      return false;
    }

    // Get the container's bounding box for the screenshot
    const box = await container.boundingBox();

    // Screenshot at 2× with transparent background outside the container
    await page.screenshot({
      path: outputPath,
      clip: {
        x: box.x,
        y: box.y,
        width: box.width,
        height: box.height,
      },
      omitBackground: false, // Keep white background
    });

    // Report dimensions
    const actualW = Math.round(box.width * DEVICE_SCALE_FACTOR);
    const actualH = Math.round(box.height * DEVICE_SCALE_FACTOR);
    log(`✓  ${name}.png  (${actualW}×${actualH}px @ ${DEVICE_SCALE_FACTOR}×)`);
    return true;

  } catch (err) {
    log(`✗  ${name}: ${err.message}`);
    return false;

  } finally {
    await page.close();
  }
}

// ── Main ──
async function main() {
  const args = process.argv.slice(2);
  const specificNames = args.filter(a => !a.startsWith('-'));

  console.log('\n📐 IRPP Figure Export\n');

  // Get files to export
  const files = await getFigureFiles(specificNames.length ? specificNames : null);
  if (files.length === 0) {
    log('No figures found to export.');
    process.exit(1);
  }

  log(`Found ${files.length} figure(s) to export\n`);

  // Launch browser
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--allow-file-access-from-files'],
    defaultViewport: {
      width: 1200,       // Wide enough for any figure variant
      height: 900,
      deviceScaleFactor: DEVICE_SCALE_FACTOR,
    },
  });

  let success = 0;
  let failed = 0;

  for (const file of files) {
    const ok = await exportFigure(browser, file);
    if (ok) success++;
    else failed++;
  }

  await browser.close();

  console.log(`\n  Done: ${success} exported${failed ? `, ${failed} failed` : ''}`);
  console.log(`  Output: ${EXPORTS_DIR}/\n`);
}

main().catch(err => {
  console.error('Export failed:', err);
  process.exit(1);
});
