#!/usr/bin/env python3
"""Editorial Taste isometric hairline illustrations.

Generates a crisp, responsive SVG in true isometric projection: a faded hairline
ground grid, white blocks with 1px hairline edges, black vertex dots, Geist Mono
labels lying on the block faces, status LEDs, dashed connectors, and one optional
signal dot with a pulsing ring.

Usage:
  python3 iso.py --preset modules > modules.svg
  python3 iso.py spec.json > illustration.svg
  python3 iso.py --list                       # list presets
  python3 iso.py --preset stack --spec        # print a preset's JSON to start from

Spec (units are grid cells; x runs down-right, y runs down-left, z runs up):
{
  "id": "iso-modules",                 # unique per page (prefixes internal ids)
  "title": "Four modules, one active", # accessible name
  "unit": 40,                          # px per grid cell (default 40)
  "aspect": 1.5,                       # optional minimum width/height ratio
  "blocks": [
    {"x": 0, "y": 0, "z": 0, "w": 4, "d": 4, "h": 1,
     "label": "Module #1", "leds": 5, "active": true, "signal": true}
  ],
  "paths": [ {"points": [[4, 2, 0], [5, 2, 0]], "dashed": true} ]
}
Keep blocks either side by side on the ground (no overlapping footprints) or
stacked exactly on top of each other; drawing order is back-to-front by x + y, then z.
"""
import json
import math
import sys
from html import escape

C30 = math.cos(math.pi / 6)
S30 = 0.5

PRESETS = {
    "modules": {
        "id": "iso-modules", "title": "Four modules on a grid, one active",
        "blocks": [
            {"x": 0, "y": 0, "w": 4, "d": 4, "h": 1.1, "label": "Module #1", "active": True, "signal": True},
            {"x": 4.6, "y": 0, "w": 4, "d": 4, "h": 1.1, "label": "Module #2", "leds": 5},
            {"x": 0, "y": 4.6, "w": 4, "d": 4, "h": 1.1, "label": "Module #3", "leds": 5},
            {"x": 4.6, "y": 4.6, "w": 4, "d": 4, "h": 1.1, "label": "Module #4", "leds": 5},
        ],
    },
    "stack": {
        "id": "iso-stack", "title": "Three platform layers stacked",
        "blocks": [
            {"x": 0, "y": 0, "z": 0, "w": 6, "d": 6, "h": 0.7, "label": "Layer 01 · Hardware", "leds": 6},
            {"x": 0, "y": 0, "z": 1.6, "w": 6, "d": 6, "h": 0.7, "label": "Layer 02 · Control", "leds": 4},
            {"x": 0, "y": 0, "z": 3.2, "w": 6, "d": 6, "h": 0.7, "label": "Layer 03 · Software", "active": True, "signal": True},
        ],
        "paths": [
            {"points": [[0, 6, 0.7], [0, 6, 1.6]], "dashed": True},
            {"points": [[6, 6, 0.7], [6, 6, 1.6]], "dashed": True},
            {"points": [[6, 0, 0.7], [6, 0, 1.6]], "dashed": True},
            {"points": [[0, 6, 2.3], [0, 6, 3.2]], "dashed": True},
            {"points": [[6, 6, 2.3], [6, 6, 3.2]], "dashed": True},
            {"points": [[6, 0, 2.3], [6, 0, 3.2]], "dashed": True},
        ],
    },
    "flow": {
        "id": "iso-flow", "title": "Three steps connected in sequence",
        "blocks": [
            {"x": 0, "y": 0, "w": 3, "d": 3, "h": 1, "label": "Step 01", "leds": 3},
            {"x": 5, "y": 0, "w": 3, "d": 3, "h": 1, "label": "Step 02", "leds": 3},
            {"x": 10, "y": 0, "w": 3, "d": 3, "h": 1.6, "label": "Step 03", "active": True, "signal": True},
        ],
        "paths": [
            {"points": [[3, 1.5, 0], [5, 1.5, 0]], "dashed": True},
            {"points": [[8, 1.5, 0], [10, 1.5, 0]], "dashed": True},
        ],
    },
    "single": {
        "id": "iso-single", "title": "One unit with its status",
        "blocks": [{"x": 0, "y": 0, "w": 5, "d": 5, "h": 1.6, "label": "Unit 01", "leds": 6, "active": True, "signal": True}],
    },
}

STYLE = """
.iso-grid line { stroke: #D4D4D4; stroke-width: .75; }
.iso-face { stroke: #A3A3A3; stroke-width: 1; stroke-linejoin: round; vector-effect: non-scaling-stroke; }
.iso-top { fill: #FFFFFF; } .iso-left { fill: #F5F5F5; } .iso-right { fill: #E5E5E5; }
.is-active .iso-face { stroke: #151515; } .is-active .iso-top { fill: #F5F5F5; }
.iso-vertex { fill: #151515; }
.iso-label { font: 400 11px "Geist Mono", ui-monospace, SFMono-Regular, monospace; letter-spacing: 1.6px; fill: #404040; }
.iso-led { fill: #D4D4D4; } .is-active .iso-led { fill: #737373; }
.iso-path { fill: none; stroke: #737373; stroke-width: 1; vector-effect: non-scaling-stroke; }
.iso-path.is-dashed { stroke-dasharray: 3 4; }
.iso-signal { fill: #FF4D2E; }
.iso-ring { fill: none; stroke: #FF4D2E; stroke-opacity: .5; stroke-width: 1; stroke-dasharray: 2 3; vector-effect: non-scaling-stroke; }
.iso-pulse { fill: none; stroke: #FF4D2E; stroke-width: 1; vector-effect: non-scaling-stroke; transform-box: fill-box; transform-origin: center; opacity: 0; }
@media (prefers-reduced-motion: no-preference) {
  .iso-pulse { animation: isoPulse 2.4s cubic-bezier(.16, 1, .3, 1) infinite; }
}
@keyframes isoPulse { 0% { opacity: .6; transform: scale(.5); } 100% { opacity: 0; transform: scale(1.6); } }
"""


def proj(x, y, z, u):
    return ((x - y) * C30 * u, (x + y) * S30 * u - z * u)


def fmt(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def poly(points, u, cls):
    pts = " ".join(f"{fmt(px)},{fmt(py)}" for px, py in (proj(*p, u) for p in points))
    return f'<polygon class="iso-face {cls}" points="{pts}"/>'


def block_svg(b, u, index):
    x, y, z = b.get("x", 0), b.get("y", 0), b.get("z", 0)
    w, d, h = b.get("w", 4), b.get("d", 4), b.get("h", 1)
    top = z + h
    cls = "iso-block is-active" if b.get("active") else "iso-block"
    out = [f'<g class="{cls}" style="--d: {index * 120}ms">']
    out.append(poly([(x, y + d, top), (x + w, y + d, top), (x + w, y + d, z), (x, y + d, z)], u, "iso-left"))
    out.append(poly([(x + w, y, top), (x + w, y + d, top), (x + w, y + d, z), (x + w, y, z)], u, "iso-right"))
    out.append(poly([(x, y, top), (x + w, y, top), (x + w, y + d, top), (x, y + d, top)], u, "iso-top"))

    # vertex dots, inset from the top-face corners
    i = min(0.3, w / 6, d / 6)
    for cx, cy in ((x + i, y + i), (x + w - i, y + i), (x + w - i, y + d - i), (x + i, y + d - i)):
        px, py = proj(cx, cy, top, u)
        out.append(f'<circle class="iso-vertex" cx="{fmt(px)}" cy="{fmt(py)}" r="2"/>')

    # label + LEDs lie on the left face: text x follows the block's x axis, text y points down
    face_h = h * u
    if b.get("label") and face_h >= 18:
        ox, oy = proj(x, y + d, top, u)
        out.append(f'<g transform="matrix({fmt(C30)} {fmt(S30)} 0 1 {fmt(ox)} {fmt(oy)})">')
        base = min(18, face_h * 0.5 + 4)
        out.append(f'<text class="iso-label" x="{fmt(0.35 * u)}" y="{fmt(base)}">{escape(b["label"].upper())}</text>')
        leds = int(b.get("leds", 0))
        if leds and face_h >= 34:
            for k in range(leds):
                out.append(f'<circle class="iso-led" cx="{fmt(0.35 * u + 3 + k * 9)}" cy="{fmt(base + 11)}" r="2.4"/>')
        out.append("</g>")

    if b.get("signal"):
        cx, cy = proj(x + w / 2, y + d / 2, top, u)
        k = math.sqrt(2)
        ring = min(w, d) * 0.18
        out.append(f'<ellipse class="iso-ring" cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(k * ring * C30 * u)}" ry="{fmt(k * ring * S30 * u)}"/>')
        out.append(f'<ellipse class="iso-pulse" cx="{fmt(cx)}" cy="{fmt(cy)}" rx="{fmt(k * ring * C30 * u)}" ry="{fmt(k * ring * S30 * u)}"/>')
        out.append(f'<ellipse class="iso-signal" cx="{fmt(cx)}" cy="{fmt(cy)}" rx="5.6" ry="3.4"/>')
    out.append("</g>")
    return "\n".join(out)


def path_svg(p, u):
    pts = " ".join(f"{fmt(px)},{fmt(py)}" for px, py in (proj(*pt, u) for pt in p["points"]))
    cls = "iso-path is-dashed" if p.get("dashed", True) else "iso-path"
    return f'<polyline class="{cls}" points="{pts}"/>'


def render(spec):
    u = spec.get("unit", 40)
    uid = spec.get("id", "iso")
    blocks = spec.get("blocks", [])
    paths = spec.get("paths", [])
    if not blocks:
        raise SystemExit("spec needs at least one block")

    pts = []
    for b in blocks:
        x, y, z = b.get("x", 0), b.get("y", 0), b.get("z", 0)
        w, d, h = b.get("w", 4), b.get("d", 4), b.get("h", 1)
        for cx in (x, x + w):
            for cy in (y, y + d):
                for cz in (z, z + h):
                    pts.append(proj(cx, cy, cz, u))
    for p in paths:
        pts += [proj(*pt, u) for pt in p["points"]]
    pad = spec.get("padding", 1.2 * u)
    minx = min(p[0] for p in pts) - pad
    maxx = max(p[0] for p in pts) + pad
    miny = min(p[1] for p in pts) - pad
    maxy = max(p[1] for p in pts) + pad
    vw, vh = maxx - minx, maxy - miny
    aspect = spec.get("aspect")
    if aspect and vw / vh < aspect:
        extra = vh * aspect - vw
        minx -= extra / 2
        vw += extra
    elif aspect and vw / vh > aspect:
        extra = vw / aspect - vh
        miny -= extra / 2
        vh += extra

    # ground grid covering the view, faded towards the edges
    span = int(max(vw, vh) / (u * S30)) + 4
    gx = sum(b.get("x", 0) + b.get("w", 4) / 2 for b in blocks) / len(blocks)
    gy = sum(b.get("y", 0) + b.get("d", 4) / 2 for b in blocks) / len(blocks)
    lines = []
    for i in range(-span, span + 1):
        a = proj(math.floor(gx) + i, gy - span, 0, u)
        b2 = proj(math.floor(gx) + i, gy + span, 0, u)
        lines.append(f'<line x1="{fmt(a[0])}" y1="{fmt(a[1])}" x2="{fmt(b2[0])}" y2="{fmt(b2[1])}"/>')
        a = proj(gx - span, math.floor(gy) + i, 0, u)
        b2 = proj(gx + span, math.floor(gy) + i, 0, u)
        lines.append(f'<line x1="{fmt(a[0])}" y1="{fmt(a[1])}" x2="{fmt(b2[0])}" y2="{fmt(b2[1])}"/>')

    ordered = sorted(blocks, key=lambda b: (b.get("x", 0) + b.get("y", 0), b.get("z", 0)))
    title = escape(spec.get("title", "Isometric illustration"))
    vb = f"{fmt(minx)} {fmt(miny)} {fmt(vw)} {fmt(vh)}"
    parts = [
        f'<svg class="iso" xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="{uid}-title">',
        f'<title id="{uid}-title">{title}</title>',
        f"<style>{STYLE.strip()}</style>",
        "<defs>",
        f'<radialGradient id="{uid}-fade" cx="50%" cy="50%" r="55%">'
        '<stop offset="0" stop-color="#FFFFFF"/><stop offset=".65" stop-color="#FFFFFF" stop-opacity=".9"/>'
        '<stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>',
        f'<mask id="{uid}-mask"><rect x="{fmt(minx)}" y="{fmt(miny)}" width="{fmt(vw)}" height="{fmt(vh)}" fill="url(#{uid}-fade)"/></mask>',
        "</defs>",
        f'<g class="iso-grid" mask="url(#{uid}-mask)">' + "".join(lines) + "</g>",
    ]
    parts += [path_svg(p, u) for p in paths if not p.get("above")]
    parts += [block_svg(b, u, i) for i, b in enumerate(ordered)]
    parts += [path_svg(p, u) for p in paths if p.get("above")]
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main(argv):
    if "--list" in argv:
        for name, s in PRESETS.items():
            print(f"{name:8} {s['title']}")
        return 0
    if "--preset" in argv:
        name = argv[argv.index("--preset") + 1]
        if name not in PRESETS:
            print(f"unknown preset '{name}'. Try --list", file=sys.stderr)
            return 2
        spec = PRESETS[name]
        if "--spec" in argv:
            print(json.dumps(spec, indent=2))
            return 0
    elif argv:
        with open(argv[0], encoding="utf-8") as f:
            spec = json.load(f)
    else:
        print(__doc__)
        return 2
    sys.stdout.write(render(spec))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
