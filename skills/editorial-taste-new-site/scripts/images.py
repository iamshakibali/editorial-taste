#!/usr/bin/env python3
"""Pull photography from Unsplash for an Editorial Taste site.

Every image slot in the page gets a search query. The script searches the
Unsplash API, picks a photo per slot, and returns a ready-to-use image URL
plus the photographer credit. It follows the Unsplash API guidelines:
  - images are hotlinked from images.unsplash.com (never re-hosted)
  - the download endpoint is triggered for every photo the page uses
  - each photo credits the photographer and Unsplash, with utm referral links

Needs an Unsplash Access Key (free: https://unsplash.com/developers, "New Application"):
  export UNSPLASH_ACCESS_KEY=...

Usage:
  images.py --spec > images.json                     # print an example manifest
  images.py images.json --out site/                  # pick photos, write site/unsplash.json + site/credits.html
  images.py images.json --out site/ --placeholders   # no key or offline: neutral local stand-ins
  images.py --apply site/unsplash.json site/index.html   # write src/srcset into <img data-slot="name">

Mark every image in the markup with data-slot="<name>" so --apply can fill it, and so a site
built with placeholders can switch to Unsplash photos later with two commands.

Manifest: a list of slots
  {"name": "hero", "query": "wooden day boat misty lake morning", "w": 2400, "h": 1500,
   "alt": "Wooden day boat at a misty mooring", "offset": 0}
  name    slot name (matches the <img> it fills)
  query   3-6 concrete words: subject, material, place, light. No "people working on laptops".
  w, h    display size in px. Hero 2400x1500, cards 1200x900 or 1000x1250, splits 1600x1000.
  offset  optional: skip the first N results (use it to swap a photo you rejected)

Output (also printed): <out>/unsplash.json
  {name: {src, srcset, w, h, alt, color, photo_id, photographer, photographer_url, photo_url}}
plus <out>/credits.html and <out>/review/contact-sheet.jpg (small previews to check every pick;
delete review/ before shipping).
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.unsplash.com"
UA = "editorial-taste-images/2.0"
TIMEOUT = 25
UTM = "utm_source=editorial_taste&utm_medium=referral"

EXAMPLE = [
    {"name": "hero", "query": "concrete stair light well architecture", "w": 2400, "h": 1500,
     "alt": "Concrete stair rising through a light well"},
    {"name": "product-1", "query": "timber house pine forest", "w": 1200, "h": 900,
     "alt": "Timber house set into a pine slope"},
    {"name": "cta", "query": "evening light living room minimal", "w": 2400, "h": 1200,
     "alt": "Evening light across a quiet living room"},
]


def api(path, key, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, headers={
        "User-Agent": UA, "Accept-Version": "v1", "Authorization": f"Client-ID {key}"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return json.load(r)


def orientation(w, h):
    r = w / h
    return "landscape" if r > 1.15 else "portrait" if r < 0.87 else "squarish"


def with_utm(url):
    return url + ("&" if "?" in url else "?") + UTM


def sized(raw, w, h):
    return f"{raw}&w={w}&h={h}&fit=crop&crop=entropy&auto=format&q=80"


def search(key, query, w, h):
    """Exact orientation first, then any orientation, then the first two words."""
    words = query.split()
    tries = [(query, orientation(w, h)), (query, None)]
    if len(words) > 2:
        tries.append((" ".join(words[:2]), None))
    for q, o in tries:
        params = {"query": q, "per_page": 20, "content_filter": "high"}
        if o:
            params["orientation"] = o
        results = api("/search/photos", key, params).get("results", [])
        if results:
            return results
    return []


def track_download(key, location):
    """Required by the API guidelines whenever a photo is used."""
    u = urllib.parse.urlparse(location)
    api(u.path, key, dict(urllib.parse.parse_qsl(u.query)))


def pick(key, slots):
    used, summary = set(), {}
    for s in slots:
        name, q, w, h = s["name"], s["query"], int(s["w"]), int(s["h"])
        results = [p for p in search(key, q, w, h) if p["id"] not in used][int(s.get("offset", 0)):]
        if not results:
            print(f"  {name}: no Unsplash results for '{q}'. Try a broader query.", file=sys.stderr)
            continue
        p = results[0]
        used.add(p["id"])
        try:
            track_download(key, p["links"]["download_location"])
        except Exception as e:
            print(f"  {name}: download tracking failed ({e})", file=sys.stderr)
        raw = p["urls"]["raw"]
        summary[name] = {
            "src": sized(raw, w, h),
            "srcset": f"{sized(raw, w // 2, h // 2)} {w // 2}w, {sized(raw, w, h)} {w}w",
            "w": w, "h": h,
            "alt": s.get("alt") or p.get("alt_description") or "",
            "unsplash_alt": p.get("alt_description"),
            "color": p.get("color"),
            "photo_id": p["id"],
            "photographer": p["user"]["name"],
            "photographer_url": with_utm(p["user"]["links"]["html"]),
            "photo_url": with_utm(p["links"]["html"]),
            "preview": p["urls"]["small"],
            "query": q,
        }
        print(f"  {name}: {p['id']} · {p['user']['name']} · {p.get('alt_description') or ''}", file=sys.stderr)
    return summary


def placeholders(slots, out):
    """Offline stand-ins: neutral local blocks, flagged for replacement."""
    img = out / "images"
    img.mkdir(parents=True, exist_ok=True)
    summary = {}
    for s in slots:
        w, h = int(s["w"]), int(s["h"])
        f = img / f"{s['name']}.svg"
        f.write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}">'
                     f'<rect width="{w}" height="{h}" fill="#D4D4D4"/></svg>')
        summary[s["name"]] = {"src": f"images/{f.name}", "w": w, "h": h, "alt": s.get("alt", ""),
                              "placeholder": True, "query": s["query"]}
    return summary


def contact_sheet(out, summary):
    """review/contact-sheet.jpg: every pick in one image, for checking subject and quality."""
    try:
        from io import BytesIO
        from PIL import Image, ImageDraw
    except ImportError:
        return
    picks = [(n, c["preview"]) for n, c in summary.items() if c.get("preview")]
    if not picks:
        return
    cols, cw, ch = 4, 360, 300
    rows = (len(picks) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * (ch + 24)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (n, url) in enumerate(picks):
        x, y = (i % cols) * cw, (i // cols) * (ch + 24)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                im = Image.open(BytesIO(r.read())).convert("RGB")
            im.thumbnail((cw - 10, ch - 10))
            sheet.paste(im, (x + 5, y + 5))
        except Exception:
            d.rectangle([x + 5, y + 5, x + cw - 5, y + ch - 5], outline="black")
        d.text((x + 6, y + ch), n, fill="black")
    rev = out / "review"
    rev.mkdir(exist_ok=True)
    sheet.save(rev / "contact-sheet.jpg", quality=80)
    print(f"  contact sheet: {rev / 'contact-sheet.jpg'}", file=sys.stderr)


def esc(t):
    return (t or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def write_credits_page(out, summary):
    rows = []
    for name, c in summary.items():
        if c.get("placeholder"):
            continue
        rows.append(
            f'        <li class="credits__row"><span class="label-lg muted">{esc(name)}</span>'
            f'<span class="body-md">{esc(c["alt"])}</span>'
            f'<span class="body-md">Photo by <a class="u-link" href="{esc(c["photographer_url"])}">{esc(c["photographer"])}</a>'
            f' on <a class="u-link" href="{esc(c["photo_url"])}">Unsplash</a></span></li>')
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
    .credits__row {{ display: grid; grid-template-columns: 160px minmax(0, 3fr) minmax(0, 4fr); gap: var(--space-20);
      padding-block: var(--space-20); border-bottom: 1px solid var(--border-subtle); align-items: baseline; }}
    @media (max-width: 767px) {{ .credits__row {{ grid-template-columns: 1fr; gap: var(--space-5); }} }}
  </style>
</head>
<body>
  <main class="container credits" id="main">
    <a class="btn btn--tertiary" href="index.html">Back to home</a>
    <h1 class="h2">Photo credits</h1>
    <ul class="credits__list">
{chr(10).join(rows) if rows else '        <li class="credits__row"><span class="body-md muted">No Unsplash photos yet.</span></li>'}
    </ul>
  </main>
</body>
</html>
"""
    (out / "credits.html").write_text(html)


def apply(summary_path, pages):
    """Write each slot's src, srcset, width, and height into <img data-slot="name"> tags."""
    summary = json.loads(Path(summary_path).read_text())
    for page in pages:
        html = Path(page).read_text()
        count = 0

        def fill(m):
            nonlocal count
            tag = m.group(0)
            slot = re.search(r'data-slot="([^"]+)"', tag).group(1)
            c = summary.get(slot)
            if not c:
                return tag
            for attr in ("src", "srcset", "width", "height"):
                tag = re.sub(rf'\s{attr}="[^"]*"', "", tag)
            extra = f' src="{esc(c["src"])}"'
            if c.get("srcset"):
                extra += f' srcset="{esc(c["srcset"])}"'
                if " sizes=" not in tag:
                    extra += ' sizes="(max-width: 767px) 100vw, 60vw"'
            extra += f' width="{c["w"]}" height="{c["h"]}"'
            if c.get("color"):
                tag = re.sub(r'\sstyle="[^"]*"', "", tag)
                extra += f' style="background:{c["color"]}"'
            count += 1
            return tag.replace("<img", "<img" + extra, 1)

        html = re.sub(r'<img\b[^>]*\bdata-slot="[^"]+"[^>]*>', fill, html)
        Path(page).write_text(html)
        print(f"  {page}: filled {count} image(s)", file=sys.stderr)
    return 0


def main(argv):
    if "--apply" in argv:
        rest = [a for a in argv if a != "--apply"]
        return apply(rest[0], rest[1:])
    if "--spec" in argv:
        print(json.dumps(EXAMPLE, indent=2))
        return 0
    out = Path(argv[argv.index("--out") + 1]) if "--out" in argv else Path(".")
    skip = {argv.index("--out") + 1} if "--out" in argv else set()
    args = [a for i, a in enumerate(argv) if not a.startswith("--") and i not in skip]
    if not args:
        print(__doc__)
        return 1
    slots = json.loads(Path(args[0]).read_text())
    out.mkdir(parents=True, exist_ok=True)

    if "--placeholders" in argv:
        summary = placeholders(slots, out)
        print("  wrote neutral placeholders. Replace them with Unsplash photos before shipping.", file=sys.stderr)
    else:
        key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if not key:
            print("UNSPLASH_ACCESS_KEY is not set.\n"
                  "Create a free app at https://unsplash.com/developers, copy its Access Key, then:\n"
                  "  export UNSPLASH_ACCESS_KEY=your_key\n"
                  "Or run with --placeholders to build with neutral stand-ins for now.", file=sys.stderr)
            return 2
        try:
            summary = pick(key, slots)
        except urllib.error.HTTPError as e:
            msg = {401: "the Access Key is invalid", 403: "rate limit reached (50 requests an hour in demo mode)"}
            print(f"Unsplash API error {e.code}: {msg.get(e.code, e.reason)}.", file=sys.stderr)
            return 2
        except urllib.error.URLError as e:
            print(f"Cannot reach api.unsplash.com ({e.reason}). Run with --placeholders to continue offline.", file=sys.stderr)
            return 2
        contact_sheet(out, summary)

    (out / "unsplash.json").write_text(json.dumps(summary, indent=2))
    write_credits_page(out, summary)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
