#!/usr/bin/env python3
"""Fetch real, licensed photography for an Editorial Taste site.

Every image slot in the page gets a search query. The script finds a photo,
downloads it into the project (never hotlinked), crops it to the slot size,
records the credit, and writes credits.html for the attribution that open
licenses require.

Providers, tried in order:
  unsplash   if UNSPLASH_ACCESS_KEY is set   (Unsplash License)
  pexels     if PEXELS_API_KEY is set        (Pexels License)
  openverse  always, no key needed           (CC0, Public Domain, CC BY, CC BY-SA only)
  placeholder  last resort, offline           (neutral monochrome block, flagged for replacement)

Usage:
  images.py --spec > images.json          # print an example manifest
  images.py images.json --out site/       # fetch into site/images/, write site/credits.html
  images.py images.json --out site/ --provider openverse

Manifest: a list of slots
  {"name": "hero", "query": "wooden day boat misty lake morning", "w": 2400, "h": 1500,
   "alt": "Wooden day boat at a misty mooring", "offset": 0}
  name    file name without extension (images/<name>.jpg)
  query   3-6 concrete words: subject, material, place, light. No "people working on laptops".
  w, h    output size in px (crop to fill). Hero 2400x1500, cards 1200x900 or 1000x1250, splits 1600x1000.
  offset  optional: skip the first N results (use it to swap a photo you rejected)

Output: prints a JSON summary {name: {file, alt, credit, provider}}, writes images/credits.json,
credits.html, and review/contact-sheet.jpg (look at it, then rerun with a better query or an
offset for any photo that is off-subject; delete review/ before shipping).
Pillow is used for cropping when installed; without it the original file is saved as is.
"""
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

UA = "editorial-taste-images/1.0"
TIMEOUT = 25
OPENVERSE_LICENSES = {"cc0", "pdm", "by", "by-sa"}

EXAMPLE = [
    {"name": "hero", "query": "concrete stair light well architecture", "w": 2400, "h": 1500,
     "alt": "Concrete stair rising through a light well"},
    {"name": "product-1", "query": "timber house pine forest", "w": 1200, "h": 900,
     "alt": "Timber house set into a pine slope"},
    {"name": "cta", "query": "evening light living room minimal", "w": 2400, "h": 1200,
     "alt": "Evening light across a quiet living room"},
]


def get_json(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def download(url, headers=None):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        data = r.read()
    if len(data) < 5000:
        raise ValueError("file too small")
    return data


def orientation(w, h):
    r = w / h
    return "wide" if r > 1.15 else "tall" if r < 0.87 else "square"


# ---------- providers: each returns a list of candidate dicts ----------
def unsplash(q, w, h):
    key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not key:
        return None
    o = {"wide": "landscape", "tall": "portrait", "square": "squarish"}[orientation(w, h)]
    url = "https://api.unsplash.com/search/photos?" + urllib.parse.urlencode(
        {"query": q, "orientation": o, "per_page": 15, "content_filter": "high"})
    data = get_json(url, {"Authorization": f"Client-ID {key}", "Accept-Version": "v1"})
    out = []
    for p in data.get("results", []):
        out.append({
            "id": p["id"],
            "url": p["urls"]["raw"] + f"&w={w}&h={h}&fit=crop&q=82&fm=jpg",
            "creator": p["user"]["name"],
            "creator_url": p["user"]["links"]["html"] + "?utm_source=editorial_taste&utm_medium=referral",
            "source_url": p["links"]["html"],
            "license": "Unsplash License",
            "license_url": "https://unsplash.com/license",
            "provider": "Unsplash",
            "track": p["links"].get("download_location"),
            "headers": {"Authorization": f"Client-ID {key}"},
        })
    return out


def pexels(q, w, h):
    key = os.environ.get("PEXELS_API_KEY")
    if not key:
        return None
    o = {"wide": "landscape", "tall": "portrait", "square": "square"}[orientation(w, h)]
    url = "https://api.pexels.com/v1/search?" + urllib.parse.urlencode(
        {"query": q, "orientation": o, "per_page": 15, "size": "large"})
    data = get_json(url, {"Authorization": key})
    return [{
        "id": str(p["id"]),
        "url": p["src"]["original"] + f"?auto=compress&cs=tinysrgb&fit=crop&w={w}&h={h}",
        "creator": p["photographer"],
        "creator_url": p["photographer_url"],
        "source_url": p["url"],
        "license": "Pexels License",
        "license_url": "https://www.pexels.com/license/",
        "provider": "Pexels",
    } for p in data.get("photos", [])]


def openverse(q, w, h):
    # Widen the search step by step: exact orientation, any orientation, then a shorter query.
    words = q.split()
    tries = [(q, orientation(w, h)), (q, None)] + ([(" ".join(words[:2]), None)] if len(words) > 2 else [])
    out = []
    for query, aspect in tries:
        params = {"q": query, "license_type": "commercial,modification", "category": "photograph",
                  "page_size": 20, "mature": "false"}
        if aspect:
            params["aspect_ratio"] = aspect
        data = get_json("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(params))
        out = _openverse_results(data, w, h)
        if out:
            break
    return out


def _openverse_results(data, w, h):
    out = []
    for p in data.get("results", []):
        if p.get("license") not in OPENVERSE_LICENSES:
            continue
        pw, ph = p.get("width") or 0, p.get("height") or 0
        if pw and ph and max(pw, ph) < min(1000, max(w, h) * 0.5):
            continue  # too small to look sharp
        lic = "CC0" if p["license"] == "cc0" else "Public Domain" if p["license"] == "pdm" \
            else f"CC {p['license'].upper()} {p.get('license_version') or ''}".strip()
        out.append({
            "id": p["id"],
            "url": p["url"],
            "creator": p.get("creator") or "Unknown",
            "creator_url": p.get("creator_url") or p.get("foreign_landing_url"),
            "source_url": p.get("foreign_landing_url"),
            "license": lic,
            "license_url": p.get("license_url"),
            "provider": f"Openverse ({p.get('source', 'web')})",
            "title": p.get("title"),
        })
    return out


PROVIDERS = {"unsplash": unsplash, "pexels": pexels, "openverse": openverse}


# ---------- image processing ----------
def crop_save(data, w, h, dest):
    try:
        from io import BytesIO
        from PIL import Image, ImageOps
    except ImportError:
        dest.write_bytes(data)
        return False
    im = Image.open(BytesIO(data))
    im = ImageOps.exif_transpose(im).convert("RGB")
    im = ImageOps.fit(im, (w, h), Image.LANCZOS, centering=(0.5, 0.5))
    im.save(dest, "JPEG", quality=82, optimize=True, progressive=True)
    return True


def placeholder(w, h, dest, seed):
    """Neutral monochrome block (#D4D4D4 to #A3A3A3), clearly a stand-in."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        svg = dest.with_suffix(".svg")
        svg.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
                       f'<rect width="{w}" height="{h}" fill="#D4D4D4"/></svg>')
        return svg
    im = Image.new("L", (w, h))
    d = ImageDraw.Draw(im)
    for y in range(h):
        d.line([(0, y), (w, y)], fill=int(212 - 49 * y / h))
    im.convert("RGB").save(dest, "JPEG", quality=80)
    return dest


# ---------- main ----------
def main(argv):
    if "--spec" in argv:
        print(json.dumps(EXAMPLE, indent=2))
        return 0
    args = [a for a in argv if not a.startswith("--")]
    if not args:
        print(__doc__)
        return 1
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else Path(".")
    only = argv[argv.index("--provider") + 1] if "--provider" in argv else None
    if "--out" in argv:
        args.remove(str(out))
    if only:
        args.remove(only)
    slots = json.loads(Path(args[0]).read_text())
    img_dir = out / "images"
    img_dir.mkdir(parents=True, exist_ok=True)

    order = [only] if only else ["unsplash", "pexels", "openverse"]
    used, summary = set(), {}
    for i, s in enumerate(slots):
        name, q, w, h = s["name"], s["query"], int(s["w"]), int(s["h"])
        dest = img_dir / f"{name}.jpg"
        done = False
        for prov in order:
            try:
                cands = PROVIDERS[prov](q, w, h)
            except Exception as e:  # network blocked, rate limited, bad key
                print(f"  {name}: {prov} unavailable ({e.__class__.__name__}: {e})", file=sys.stderr)
                continue
            if not cands:
                continue
            cands = [c for c in cands if c["id"] not in used][int(s.get("offset", 0)):]
            for c in cands[:6]:
                try:
                    data = download(c["url"], c.get("headers"))
                    crop_save(data, w, h, dest)
                except Exception as e:
                    print(f"  {name}: skip {c['id']} ({e})", file=sys.stderr)
                    continue
                if c.get("track"):  # Unsplash API guideline: register the download
                    try:
                        get_json(c["track"], c.get("headers"))
                    except Exception:
                        pass
                used.add(c["id"])
                summary[name] = {"file": f"images/{dest.name}", "alt": s.get("alt", ""), "query": q,
                                 "provider": c["provider"], "creator": c["creator"],
                                 "creator_url": c["creator_url"], "source_url": c["source_url"],
                                 "license": c["license"], "license_url": c["license_url"],
                                 "title": c.get("title")}
                print(f"  {name}: {c['provider']} · {c['creator']} · {c['license']}", file=sys.stderr)
                done = True
                break
            if done:
                break
        if not done:
            f = placeholder(w, h, dest, i)
            summary[name] = {"file": f"images/{f.name}", "alt": s.get("alt", ""), "query": q,
                             "provider": "placeholder"}
            print(f"  {name}: PLACEHOLDER (no provider reachable). Replace before shipping.", file=sys.stderr)

    (img_dir / "credits.json").write_text(json.dumps(summary, indent=2))
    contact_sheet(out, summary)
    write_credits_page(out, summary)
    print(json.dumps(summary, indent=2))
    return 0


def contact_sheet(out, summary):
    """Write review/contact-sheet.jpg (outside images/) so every pick can be checked in one look."""
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    files = [(n, out / c["file"]) for n, c in summary.items() if c["file"].endswith(".jpg")]
    if not files:
        return
    cols, cw, chh = 4, 360, 300
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * (chh + 24)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (n, f) in enumerate(files):
        im = Image.open(f)
        im.thumbnail((cw - 10, chh - 10))
        x, y = (i % cols) * cw, (i // cols) * (chh + 24)
        sheet.paste(im, (x + 5, y + 5))
        d.text((x + 6, y + chh), n, fill="black")
    rev = out / "review"
    rev.mkdir(exist_ok=True)
    sheet.save(rev / "contact-sheet.jpg", quality=80)
    print(f"  contact sheet: {rev / 'contact-sheet.jpg'}", file=sys.stderr)


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def write_credits_page(out, summary):
    rows = []
    for name, c in summary.items():
        if c["provider"] == "placeholder":
            continue
        who = f'<a class="u-link" href="{esc(c["creator_url"])}">{esc(c["creator"])}</a>' if c.get("creator_url") else esc(c["creator"])
        lic = f'<a class="u-link" href="{esc(c["license_url"])}">{esc(c["license"])}</a>' if c.get("license_url") else esc(c["license"])
        src = f'<a class="u-link" href="{esc(c["source_url"])}">Source</a>' if c.get("source_url") else ""
        rows.append(f'        <li class="credits__row"><span class="label-lg muted">{esc(name)}</span>'
                    f'<span class="body-md">{esc(c.get("title") or c["alt"])}</span>'
                    f'<span class="body-md">{who} · {lic} · {esc(c["provider"])}</span>'
                    f'<span class="body-md">{src}</span></li>')
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Photo credits</title>
  <meta name="robots" content="noindex" />
  <link rel="icon" href="favicon.svg" type="image/svg+xml" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;700&family=Geist+Mono:wght@400&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="styles.css" />
  <style>
    .credits {{ padding-block: 120px var(--section-pad); }}
    .credits h1 {{ margin-bottom: var(--section-gap); }}
    .credits__list {{ border-top: 1px solid var(--border-subtle); }}
    .credits__row {{ display: grid; grid-template-columns: 160px minmax(0, 3fr) minmax(0, 4fr) 80px; gap: var(--space-20);
      padding-block: var(--space-20); border-bottom: 1px solid var(--border-subtle); align-items: baseline; }}
    @media (max-width: 767px) {{ .credits__row {{ grid-template-columns: 1fr; gap: var(--space-5); }} }}
  </style>
</head>
<body>
  <main class="container credits" id="main">
    <a class="btn btn--tertiary" href="index.html">Back to home</a>
    <h1 class="h2">Photo credits</h1>
    <ul class="credits__list">
{chr(10).join(rows) if rows else '        <li class="credits__row"><span class="body-md muted">No third-party photos yet.</span></li>'}
    </ul>
  </main>
</body>
</html>
"""
    (out / "credits.html").write_text(html)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
