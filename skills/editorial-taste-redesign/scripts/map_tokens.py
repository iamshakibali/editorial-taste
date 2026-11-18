#!/usr/bin/env python3
"""Editorial Taste token mapper: inventories an existing site's styles and maps
each value to the nearest Editorial Taste token, so a redesign can be done as
systematic replacements instead of guesswork.

Usage: python3 map_tokens.py <path> [<path> ...]   (files or directories)
Scans .css .scss .sass .less .html .jsx .tsx .js .ts .vue .svelte .astro files.
Prints a Markdown report: colors, font families, font sizes, spacing, radii,
shadows, and Tailwind utilities that need replacing.
"""
import os
import re
import sys
from collections import Counter

EXTS = {".css", ".scss", ".sass", ".less", ".html", ".htm", ".jsx", ".tsx", ".js", ".ts",
        ".vue", ".svelte", ".astro", ".mdx"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".next", ".nuxt", ".svelte-kit", "out",
             "coverage", ".vercel", ".turbo", "vendor"}

GRAYS = [  # (token, value)
    ("--neutral-white", 255), ("--neutral-50", 250), ("--neutral-100", 245), ("--bg-base", 237),
    ("--neutral-200", 229), ("--bg-lift", 217), ("--neutral-300", 212), ("--neutral-400", 163),
    ("--neutral-500 / --text-muted", 115), ("--neutral-600", 82), ("--neutral-700", 64),
    ("--neutral-800", 38), ("--neutral-850", 31), ("--neutral-900", 23), ("--tone-strong", 21),
    ("--neutral-950", 10), ("--neutral-black", 0),
]
ALPHA_STEPS = [100, 88, 64, 48, 32, 16, 8, 4]
TYPE_SCALE = [  # web desktop px -> class
    (72, ".h0"), (48, ".h1"), (40, ".h2"), (32, ".h3"), (24, ".h4"), (20, ".h5"),
    (17, ".body-lg"), (15, ".body-md"), (14, ".h6 / .btn (13)"), (13, ".body-sm / .btn"),
    (11, ".label-lg / .btn--sm"), (10, ".label-sm"),
]
SPACE_SCALE = [0, 5, 10, 15, 20, 25, 30, 35, 40, 50, 60, 75, 100]
RADII = [(0, "0"), (4, "--radius-4"), (8, "--radius-btn"), (10, "--radius-10"),
         (20, "--radius-20"), (9999, "--radius-pill")]
TW_CHROMA = r"(?:red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)"

NAMED = {"white": (255, 255, 255), "black": (0, 0, 0), "red": (255, 0, 0), "blue": (0, 0, 255),
         "green": (0, 128, 0), "gray": (128, 128, 128), "grey": (128, 128, 128)}


def files(paths):
    for p in paths:
        if os.path.isfile(p):
            yield p
        for root, dirs, fs in os.walk(p):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
            for f in fs:
                if os.path.splitext(f)[1].lower() in EXTS and not f.endswith(".min.css"):
                    yield os.path.join(root, f)


def to_px(v):
    m = re.match(r"(-?\d*\.?\d+)(px|rem|em)?$", v.strip())
    if not m:
        return None
    n = float(m.group(1))
    return n * 16 if m.group(2) in ("rem", "em") else n


def map_color(r, g, b, a=1.0):
    if max(r, g, b) - min(r, g, b) > 12:
        return "ACCENT → remove. Use --tone-strong for emphasis; let photography carry color"
    gray = (r + g + b) / 3
    if a < 0.98:
        step = min(ALPHA_STEPS, key=lambda s: abs(s - a * 100))
        return f"--{'dark' if gray < 128 else 'light'}-{step}"
    tok, val = min(GRAYS, key=lambda t: abs(t[1] - gray))
    return tok if abs(val - gray) <= 3 else f"{tok} (nearest)"


def parse_colors(text):
    out = []
    for m in re.finditer(r"#([0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b", text):
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h)
        r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
        a = int(h[6:8], 16) / 255 if len(h) == 8 else 1.0
        out.append(("#" + m.group(1).lower(), r, g, b, a))
    for m in re.finditer(r"rgba?\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)(?:\s*[,/]\s*([\d.]+%?))?\s*\)", text):
        a = m.group(4)
        a = (float(a[:-1]) / 100 if a and a.endswith("%") else float(a)) if a else 1.0
        out.append((m.group(0).replace(" ", ""), int(m.group(1)), int(m.group(2)), int(m.group(3)), a))
    for m in re.finditer(r"(?:color|background(?:-color)?|border(?:-color)?|fill|stroke)\s*:\s*(white|black|red|blue|green|gr[ae]y)\b", text, re.I):
        r, g, b = NAMED[m.group(1).lower()]
        out.append((m.group(1).lower(), r, g, b, 1.0))
    return out


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    colors, fams, sizes, spacing, radii, shadows, weights, tw = (Counter() for _ in range(8))
    color_map, scanned = {}, 0
    for path in files(argv):
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        scanned += 1
        for key, r, g, b, a in parse_colors(text):
            colors[key] += 1
            color_map[key] = map_color(r, g, b, a)
        for m in re.finditer(r"font-family\s*:\s*([^;}\n]+)", text, re.I):
            fams[m.group(1).strip().strip("'\"")] += 1
        for m in re.finditer(r"font-size\s*:\s*([\d.]+(?:px|rem|em))", text, re.I):
            sizes[m.group(1)] += 1
        for m in re.finditer(r"font-weight\s*:\s*(\w+)", text, re.I):
            weights[m.group(1)] += 1
        for m in re.finditer(r"(?:margin|padding|gap|row-gap|column-gap)(?:-[a-z]+)?\s*:\s*([^;}\n]+)", text, re.I):
            for v in re.findall(r"-?[\d.]+(?:px|rem)", m.group(1)):
                spacing[v] += 1
        for m in re.finditer(r"border(?:-[a-z]+)?-radius\s*:\s*([^;}\n]+)", text, re.I):
            for v in re.findall(r"[\d.]+(?:px|rem|%)", m.group(1)):
                radii[v] += 1
        for m in re.finditer(r"(box-shadow|text-shadow|drop-shadow)\s*[:(]\s*([^;}\n]+)", text, re.I):
            if not m.group(2).strip().startswith("none"):
                shadows[m.group(1)] += 1
        for pat, label in [
            (rf"\b(?:bg|text|border|ring|from|via|to|fill|stroke|outline|decoration|accent)-{TW_CHROMA}-\d{{2,3}}\b", "chromatic color utility → neutral / tone utilities"),
            (r"\bshadow(?:-(?:sm|md|lg|xl|2xl|inner))?\b(?![-:\w])", "shadow utility → remove; use backdrop-blur for glass"),
            (r"\bfont-(?:semibold|bold|extrabold|black)\b", "bold weight → font-medium (headings) / font-normal"),
            (r"\brounded-(?:sm|md|lg|xl|2xl|3xl)\b", "radius utility → rounded-[8px] buttons / [10px] cards / [20px] case / full"),
            (r"\bfont-(?:serif)\b", "serif → Geist (font-sans)"),
        ]:
            for m in re.finditer(pat, text):
                tw[(m.group(0), label)] += 1

    print(f"# Editorial Taste token map\n\nScanned {scanned} file(s).\n")

    print("## Colors\n| Value | Uses | Replace with |\n|---|---|---|")
    for k, n in colors.most_common(60):
        print(f"| `{k}` | {n} | {color_map[k]} |")

    print("\n## Font families\n| Value | Uses | Replace with |\n|---|---|---|")
    for k, n in fams.most_common():
        mono = re.search(r"mono|code|courier|consolas|menlo", k, re.I)
        ok = re.search(r"var\(--font-|Geist", k)
        rep = "OK" if ok else ("--font-ui (Geist Mono): UI/labels only" if mono else "--font-heading / --font-body (Geist)")
        print(f"| `{k[:60]}` | {n} | {rep} |")

    print("\n## Font weights\n| Value | Uses | Replace with |\n|---|---|---|")
    for k, n in weights.most_common():
        w = {"bold": 700, "bolder": 800, "normal": 400, "lighter": 300}.get(k.lower(), k)
        try:
            w = int(w)
            rep = "OK" if w in (400, 500) else ("500 (Medium)" if w > 500 else "400")
        except ValueError:
            rep = "check"
        print(f"| `{k}` | {n} | {rep} |")

    print("\n## Font sizes\n| Value | Uses | Nearest style |\n|---|---|---|")
    for k, n in sorted(sizes.items(), key=lambda kv: -(to_px(kv[0]) or 0)):
        px = to_px(k)
        size, cls = min(TYPE_SCALE, key=lambda t: abs(t[0] - px))
        print(f"| `{k}` ({px:g}px) | {n} | {cls} ({size}px) |")

    print("\n## Spacing\n| Value | Uses | Nearest token |\n|---|---|---|")
    for k, n in sorted(spacing.items(), key=lambda kv: abs(to_px(kv[0]) or 0)):
        px = abs(to_px(k) or 0)
        near = min(SPACE_SCALE, key=lambda s: abs(s - px))
        flag = "" if px in SPACE_SCALE or px in (8, 12, 32, 56, 96) else " ⚠"
        print(f"| `{k}` | {n} | --space-{near}{flag} |" if near else f"| `{k}` | {n} | 0 |")

    print("\n## Border radius\n| Value | Uses | Replace with |\n|---|---|---|")
    for k, n in radii.most_common():
        if k.endswith("%"):
            rep = "--radius-pill / 50% (circles only)"
        else:
            px = to_px(k)
            rep = "--radius-pill" if px >= 100 else min(RADII, key=lambda r: abs(r[0] - px))[1]
        print(f"| `{k}` | {n} | {rep} |")

    print("\n## Shadows\n")
    if shadows:
        for k, n in shadows.items():
            print(f"- `{k}` × {n} → remove. Use translucent fill + `backdrop-filter: var(--blur-glass)` or a hairline `--border-subtle`")
    else:
        print("None found.")

    if tw:
        print("\n## Tailwind utilities\n| Utility | Uses | Action |\n|---|---|---|")
        for (u, label), n in tw.most_common(60):
            print(f"| `{u}` | {n} | {label} |")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
