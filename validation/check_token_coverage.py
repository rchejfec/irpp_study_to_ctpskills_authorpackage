#!/usr/bin/env python3
"""Theme v2 final-acceptance check (REGISTRY.md § Verification protocol).

Verifies, mechanically:
  1. registry.json parses; status counts reported.
  2. tokens.css :root and html.canary blocks are in lockstep (same token set).
  3. Every tokens.css token has a live (non-merged) registry row, and every
     registry row with recorded usage exists in tokens.css.
  4. No live figure retains a legacy var (--clr-*/--irpp-*) or a raw colour
     literal (hex) outside comments — i.e. every colour resolves to a token.

Exit 0 = PASS. Canary-value duplicates are reported as warnings only
(RC may bless deliberate aliases). theme.css is exempt until fold-in.

Run from the repo root:  python3 validation/check_token_coverage.py
"""
import json, re, os, sys, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'figure_data/theme/registry.json')
CSS = os.path.join(ROOT, 'figure_data/dist/tokens.css')
FIGS = os.path.join(ROOT, 'figure_data/dist/figures')

fail = []

reg = json.load(open(REG))
toks = reg['tokens']
statuses = collections.Counter(t['status'] for t in toks)
print(f"registry rows: {len(toks)} {dict(statuses)}")
live = {t['token'] for t in toks if t['status'] not in ('merged', 'dropped')}

css = open(CSS).read()
root_block = css.split(':root {')[1].split('}')[0]
canary_block = css.split('html.canary {')[1].split('}')[0]
root_toks = set(re.findall(r'(--color-[a-z0-9-]+):', root_block))
canary_toks = set(re.findall(r'(--color-[a-z0-9-]+):', canary_block))
print(f"tokens.css: {len(root_toks)} in :root, {len(canary_toks)} in canary")

if root_toks != canary_toks:
    fail.append(f"lockstep broken: :root-only={sorted(root_toks-canary_toks)} canary-only={sorted(canary_toks-root_toks)}")
orphans = root_toks - live
if orphans:
    fail.append(f"tokens.css tokens without a live registry row: {sorted(orphans)}")
used_reg = {t['token'] for t in toks if t.get('usage')}
missing = used_reg - root_toks
if missing:
    fail.append(f"registry rows with usage but absent from tokens.css: {sorted(missing)}")

bench = sorted(t['token'] for t in toks if t['status'] not in ('merged', 'dropped') and not t.get('usage'))
if bench:
    print(f"note — live rows with no usage (bench): {bench}")

canary_vals = re.findall(r'(--color-[a-z0-9-]+):\s*([^;]+);', canary_block)
by_val = collections.defaultdict(list)
for k, v in canary_vals:
    by_val[v.strip().lower()].append(k)
dups = {v: ks for v, ks in by_val.items() if len(ks) > 1}
if dups:
    print(f"warning — {len(dups)} duplicated canary values (wrong-token detection blind within each set):")
    for v, ks in sorted(dups.items()):
        print(f"   {v}: {ks}")

hexre = re.compile(r'#[0-9a-fA-F]{3,8}\b')
legacy = re.compile(r'var\(--(clr|irpp)-')
for f in sorted(os.listdir(FIGS)):
    if not f.endswith('.html'):
        continue
    txt = open(os.path.join(FIGS, f)).read()
    t2 = re.sub(r'/\*.*?\*/', '', txt, flags=re.S)
    t2 = re.sub(r'<!--.*?-->', '', t2, flags=re.S)
    t2 = re.sub(r'^\s*//.*$', '', t2, flags=re.M)
    lv = legacy.findall(t2)
    hx = hexre.findall(t2)
    if lv or hx:
        fail.append(f"{f}: legacy-vars={len(lv)} hex-literals={sorted(set(hx))}")
    else:
        print(f"  {f}: clean (0 legacy vars, 0 hex literals)")

print()
if fail:
    print("FAIL:")
    for m in fail:
        print(" -", m)
    sys.exit(1)
print(f"PASS: all {sum(1 for f in os.listdir(FIGS) if f.endswith('.html'))} live figures fully token-resolved; "
      f"{len(root_toks)} tokens, lockstep intact.")
