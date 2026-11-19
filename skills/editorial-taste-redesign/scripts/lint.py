#!/usr/bin/env python3
"""Editorial Taste linter: flags CSS/HTML/JSX that breaks Editorial Taste rules.

Usage: python3 lint.py [--strict] <file|dir> [...]
  --strict  also fail on leftover {{placeholders}} (use before delivery)
Exit code 1 if any ERROR is found; WARN entries are advisory.
Add "lint-ok" in a comment on a line to accept a deliberate exception.

Also checks the fixed type roles (hero h1 in .h2, .h0 only for the statement), one statement
per page and never directly under the hero, radius 20 only on case cards, and that every
var(--token) used without a fallback is defined somewhere in the linted files.
"""
import os
import re
import sys

PALETTE = {
    "ffffff", "fafafa", "f5f5f5", "ededed", "e5e5e5", "d4d4d4", "a3a3a3", "737373",
    "525252", "404040", "262626", "1f1f1f", "171717", "0a0a0a", "050505", "000000",
    "151515", "d9d9d9",
    "ff4d2e",  # --signal: one status dot per isometric illustration, nowhere else
}
ALPHAS = {"ff", "e0", "a3", "7a", "52", "29", "14", "0a"}
# Off-5 values the compact web scale explicitly allows
ALLOWED_PX = {0, 1, 2, 3, 4, 6, 8, 12, 14, 16, 18, 22, 24, 26, 28, 32, 36, 44, 48, 56,
              64, 68, 72, 92, 96, 104, 110, 160, 200, 220, 240, 340, 420, 480, 520, 560, 640,
              760, 820, 1020, 1040, 1280, 9999}
ALLOWED_RADII = {0, 2, 4, 8, 10, 20, 9999}
SPACING_PROPS = re.compile(
    r"^\s*(margin|padding|gap|row-gap|column-gap|inset|top|right|bottom|left)"
    r"(-[a-z-]+)?\s*:\s*([^;]+);", re.I)
RADIUS_PROP = re.compile(r"^\s*border(-[a-z-]+)?-radius\s*:\s*([^;]+);", re.I)
FILLER = re.compile(
    r"\b(revolutioni[sz]e|supercharge|cutting[- ]edge|seamless(?:ly)?|effortless(?:ly)?|"
    r"next[- ]level|world[- ]class|game[- ]chang\w*|harness the power|transform your workflow|"
    r"unlock (?:your|the)|empower(?:ing)?|elevate your)\b", re.I)
EXTS = {".css", ".scss", ".html", ".htm", ".jsx", ".tsx", ".js", ".mjs", ".ts", ".vue", ".svelte", ".astro"}
SKIP = {"node_modules", ".git", "dist", "build", ".next", "out", "vendor"}


def check_color(h):
    h = h.lower()
    if len(h) in (3, 4):
        h = "".join(c * 2 for c in h[:3])
    if len(h) == 6:
        return h in PALETTE
    if len(h) == 8:
        return (h[:6] in {"ededed", "151515"} and h[6:] in ALPHAS) or (h[:6] in PALETTE and h[6:] == "ff")
    return False


def lint(path, strict):
    issues = []
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        return [("ERROR", 0, f"cannot read: {e}")]
    is_markup = os.path.splitext(path)[1].lower() in {".html", ".htm", ".jsx", ".tsx", ".vue", ".svelte", ".astro"}
    in_root = False
    in_svg_symbol = False
    selector = ""
    is_404 = os.path.basename(path).startswith("404")
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith(":root"):
            in_root = True
        if in_root and s.startswith("}"):
            in_root = False
        if "<symbol" in line:
            in_svg_symbol = True
        if "</symbol>" in line or "</svg>" in line:
            in_svg_symbol = False

        def add(level, msg):
            if "lint-ok" not in line:
                issues.append((level, n, msg))

        if "{" in line and not in_root:
            selector = line.split("{")[0].strip() or selector

        # Radius 20 belongs to case cards only
        if re.search(r"border(?:-[a-z-]+)?-radius\s*:[^;]*(?:\b20px|var\(--radius-20\))", line) and not in_root:
            if "case" not in selector:
                add("ERROR", f"radius 20 on '{selector}'. 20 is for case cards only; photos, frames, and panels use 10")

        # Fixed type roles (markup)
        if is_markup and not is_404:
            for m in re.finditer(r"<h1\b[^>]*>", line):
                cls = re.search(r'class(?:Name)?="([^"]*)"', m.group(0))
                classes = cls.group(1).split() if cls else []
                if "h2" not in classes:
                    add("ERROR", "the page h1 (hero headline) must use .h2")
            for m in re.finditer(r"<[a-z0-9]+\b[^>]*class(?:Name)?=\"[^\"]*\bh0\b[^\"]*\"[^>]*>", line):
                if "data-words" not in m.group(0):
                    add("ERROR", ".h0 is reserved for the statement (data-words)")

        # Elevation
        if re.search(r"(box|text)-shadow\s*:\s*(?!none)", line, re.I):
            add("ERROR", "shadow used. Use glass blur or a hairline, never shadows")
        if re.search(r"drop-shadow\(", line, re.I):
            add("ERROR", "drop-shadow filter is not allowed")
        if re.search(r"\bshadow-(?:sm|md|lg|xl|2xl|inner)\b|\bshadow\b(?=[\s\"'])", line) and "class" in line:
            add("ERROR", "Tailwind shadow utility")

        # Color
        for m in re.finditer(r"#([0-9a-fA-F]{3,8})\b", line):
            if len(m.group(1)) in (3, 4, 6, 8) and not check_color(m.group(1)):
                add("ERROR", f"off-palette color #{m.group(1)}")
        for m in re.finditer(r"rgba?\(\s*(\d+)[\s,]+(\d+)[\s,]+(\d+)", line):
            r, g, b = map(int, m.groups())
            if not r == g == b:
                add("ERROR", f"chromatic color rgb({r},{g},{b}). The palette is achromatic")
        if re.search(r"\b(?:bg|text|border|ring|from|via|to)-(?:red|orange|amber|yellow|lime|green|emerald|teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose)-\d{2,3}\b", line):
            add("ERROR", "Tailwind chromatic color utility")
        if re.search(r"background(?:-image)?\s*:[^;]*linear-gradient", line) and "rgba(0,0,0" not in line.replace(" ", "") and "var(--vignette" not in line:
            add("WARN", "gradient background. Only black vignettes over photos are allowed")
        if re.search(r"background-clip\s*:\s*text", line):
            add("ERROR", "gradient text. Headlines are solid")

        # Type
        if re.search(r"font-weight\s*:\s*(bold|bolder|[6-9]00)", line, re.I) and not in_svg_symbol:
            add("ERROR", "bold weight. Headings are Medium (500), body is 400/500")
        if re.search(r"\bfont-(?:semibold|bold|extrabold|black)\b", line):
            add("ERROR", "Tailwind bold weight utility")
        fam = re.search(r"font-family\s*:\s*([^;]+)", line, re.I)
        if fam and not re.search(r"var\(--font-|Geist|inherit", fam.group(1)):
            add("ERROR", f"off-system font: {fam.group(1).strip()}")
        if re.search(r"IBM Plex|\bInter\b|Roboto|Open Sans|Helvetica|Arial", line) and ("font" in line.lower()):
            add("ERROR", "off-system font family referenced")
        if re.search(r"font-style\s*:\s*italic|\bitalic\b(?=[\s\"'])", line):
            add("WARN", "italic. Use tone or weight for emphasis")

        # Motion
        if re.search(r"transition\s*:\s*all\b|transition-property\s*:\s*all", line):
            add("ERROR", "transition: all. List only transform, opacity, and color properties")
        if re.search(r"transition[^;]*\b(width|height|top|left|right|bottom|margin|padding)\b", line, re.I):
            add("WARN", "animating a layout property. Animate transform/opacity instead")
        if re.search(r"(transition|animation)[^;]*\s(ease|linear|ease-in-out|ease-in|ease-out)\s*[;,]", line):
            add("WARN", "browser default easing. Use var(--ease)")

        if re.search(r"transition[^;]*\b(?:backdrop-)?filter\b|transition[^;]*box-shadow", line):
            add("WARN", "animating filter/backdrop-filter/box-shadow repaints every frame. Animate opacity or transform")
        if re.search(r"will-change\s*:", line):
            add("WARN", "will-change kept permanently. Set it only while an element animates")
        if re.search(r"addEventListener\(\s*['\"](?:scroll|wheel|touchmove|touchstart)['\"]", line) and "passive" not in line:
            add("WARN", "scroll/touch listener without { passive: true }. Throttle work with requestAnimationFrame")
        if re.search(r"setInterval\([^)]*\b(?:style|scroll|translate|opacity)", line):
            add("WARN", "setInterval-driven animation. Use CSS transitions or requestAnimationFrame")

        # Icons
        if re.search(r"material-icons|material-symbols|Material\+Icons|Material\+Symbols", line):
            add("ERROR", "Material icons. Use 1.2px line icons or Phosphor Light")

        # Markup checks
        if is_markup:
            for m in re.finditer(r"<img\b[^>]*>", line):
                if not re.search(r"\balt=", m.group(0)):
                    add("ERROR", "<img> without alt")
            if re.search(r"href=\"#\"(?![^>]*aria-disabled)", line):
                add("WARN", 'dead link href="#". Wire it up or mark it aria-disabled="true"')
            if re.search(r"\balert\(", line):
                add("ERROR", "alert(). Show messages inline with aria-live")
            for m in FILLER.finditer(line):
                add("WARN", f"filler word '{m.group(0)}'. Say what it does instead")
            if re.search(r"lorem ipsum", line, re.I):
                add("ERROR", "lorem ipsum. Write real copy")
            if strict and "{{" in line:
                add("ERROR", "unreplaced {{placeholder}}")

        # Scales
        if not in_root:
            for regex, allowed, label in ((SPACING_PROPS, ALLOWED_PX, "spacing"), (RADIUS_PROP, ALLOWED_RADII, "radius")):
                m = regex.match(line)
                if m:
                    for px in re.findall(r"(-?\d+(?:\.\d+)?)px", m.group(m.lastindex)):
                        v = abs(float(px))
                        if v % 5 != 0 and v not in allowed:
                            add("WARN", f"{label} {px}px is off the 5px scale")
    if is_markup and not is_404:
        issues += structure(text)
    return issues


def structure(text):
    """Page-level checks: one statement, never directly under the hero."""
    out = []
    words = [m.start() for m in re.finditer(r"\bdata-words\b", text)]
    line_of = lambda pos: text.count("\n", 0, pos) + 1
    if len(words) > 1:
        out.append(("ERROR", line_of(words[1]), "more than one statement (data-words). One per page"))
    main = re.search(r"<main\b", text)
    if words and main:
        sections = [m.start() for m in re.finditer(r"<section\b", text) if m.start() > main.start()]
        owner = [i for i, pos in enumerate(sections) if pos < words[0]]
        if owner and owner[-1] == 1:
            out.append(("ERROR", line_of(words[0]),
                        "statement sits directly under the hero. Put at least one section between them"))
    return out


TOKEN_DEF = re.compile(r"(--[a-zA-Z0-9-]+)\s*:")
TOKEN_USE = re.compile(r"var\(\s*(--[a-zA-Z0-9-]+)\s*\)")


def token_issues(files):
    """var(--x) with no fallback must be defined in one of the linted files."""
    defined, uses = set(), []
    for f in files:
        try:
            text = open(f, encoding="utf-8").read()
        except OSError:
            continue
        defined.update(TOKEN_DEF.findall(text))
        for n, line in enumerate(text.splitlines(), 1):
            if "lint-ok" in line:
                continue
            for name in TOKEN_USE.findall(line):
                uses.append((f, n, name))
    if "--bg-base" not in defined:  # the token file isn't among the linted files: can't judge
        return []
    return [(f, n, "ERROR", f"undefined token {name}. It renders as nothing; use a token from styles.css")
            for f, n, name in uses if name not in defined]


def expand(paths):
    for p in paths:
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                dirs[:] = [d for d in dirs if d not in SKIP and not d.startswith(".")]
                for f in files:
                    if os.path.splitext(f)[1].lower() in EXTS:
                        yield os.path.join(root, f)
        else:
            yield p


def main(argv):
    strict = "--strict" in argv
    paths = [a for a in argv if a != "--strict"]
    if not paths:
        print(__doc__)
        return 2
    errors = warns = 0
    files = list(expand(paths))
    for path in files:
        for level, n, msg in lint(path, strict):
            errors += level == "ERROR"
            warns += level == "WARN"
            print(f"{path}:{n}: {level}: {msg}")
    for path, n, level, msg in token_issues(files):
        errors += 1
        print(f"{path}:{n}: {level}: {msg}")
    print(f"\n{errors} error(s), {warns} warning(s)." if errors or warns else "\nNo issues.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
