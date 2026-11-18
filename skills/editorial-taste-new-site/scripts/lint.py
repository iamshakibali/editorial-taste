#!/usr/bin/env python3
"""Editorial Taste linter: flags CSS/HTML that breaks Editorial Taste rules.

Usage: python3 lint.py <file> [<file> ...]
Exit code 1 if any ERROR is found; WARN entries are advisory.
"""
import re
import sys

PALETTE = {
    # neutral
    "ffffff", "fafafa", "f5f5f5", "ededed", "e5e5e5", "d4d4d4", "a3a3a3", "737373",
    "525252", "404040", "262626", "1f1f1f", "171717", "0a0a0a", "050505", "000000",
    # base + semantic
    "151515", "d9d9d9",
}
ALPHAS = {"ff", "e0", "a3", "7a", "52", "29", "14", "0a"}
SHORT = {"fff": "ffffff", "000": "000000"}

# Off-5 values the compact web scale explicitly allows (DESIGN.md §5.3)
ALLOWED_PX = {0, 1, 2, 3, 4, 6, 8, 12, 14, 16, 18, 22, 24, 26, 28, 32, 36, 44, 48, 56,
              64, 68, 72, 92, 96, 104, 160, 200, 220, 240, 340, 420, 480, 520, 560, 760, 820,
              1020, 1280, 9999}
SPACING_PROPS = re.compile(
    r"^\s*(margin|padding|gap|row-gap|column-gap|inset|top|right|bottom|left)"
    r"(-[a-z-]+)?\s*:\s*([^;]+);", re.I)
RADIUS_PROP = re.compile(r"^\s*border(-[a-z-]+)?-radius\s*:\s*([^;]+);", re.I)
ALLOWED_RADII = {0, 4, 8, 10, 20, 9999}


def check_color(hexv):
    h = hexv.lower()
    if len(h) in (3, 4):
        h = SHORT.get(h[:3], "".join(c * 2 for c in h[:3]))
    if len(h) == 6:
        return h in PALETTE
    if len(h) == 8:
        return h[:6] in {"ededed", "151515"} and h[6:] in ALPHAS or h[:6] in PALETTE and h[6:] == "ff"
    return False


def lint(path):
    issues = []
    try:
        text = open(path, encoding="utf-8").read()
    except OSError as e:
        return [("ERROR", 0, f"cannot read: {e}")]
    in_root = False
    for n, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith(":root"):
            in_root = True
        if in_root and s.startswith("}"):
            in_root = False

        if re.search(r"(box|text)-shadow\s*:\s*(?!none)", line, re.I):
            issues.append(("ERROR", n, "shadow used. use glass blur, never shadows"))
        if re.search(r"drop-shadow\(", line, re.I):
            issues.append(("ERROR", n, "drop-shadow filter is not allowed"))

        for m in re.finditer(r"#([0-9a-fA-F]{3,8})\b", line):
            if len(m.group(1)) in (3, 4, 6, 8) and not check_color(m.group(1)):
                issues.append(("ERROR", n, f"off-palette color #{m.group(1)}"))
        for m in re.finditer(r"rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", line):
            r, g, b = map(int, m.groups())
            if not (r == g == b):
                issues.append(("ERROR", n, f"chromatic color rgb({r},{g},{b}). The palette is achromatic"))
        if re.search(r"\bhsla?\(", line) and not re.search(r"hsla?\(\s*\d+\s*,?\s*0%", line):
            issues.append(("WARN", n, "hsl() color, verify it is achromatic"))

        if re.search(r"font-weight\s*:\s*(bold|[6-9]00)", line, re.I):
            issues.append(("ERROR", n, "bold weight. Headings are Medium (500), body is 400/500"))
        fam = re.search(r"font-family\s*:\s*([^;]+)", line, re.I)
        if fam and not re.search(r"var\(--font-|Geist", fam.group(1)) and "inherit" not in fam.group(1):
            issues.append(("ERROR", n, f"off-system font: {fam.group(1).strip()}"))
        if re.search(r"IBM Plex", line):
            issues.append(("ERROR", n, "IBM Plex Mono. Use Geist Mono"))

        if not in_root:
            for regex, allowed, label in ((SPACING_PROPS, ALLOWED_PX, "spacing"), (RADIUS_PROP, ALLOWED_RADII, "radius")):
                m = regex.match(line)
                if m:
                    for px in re.findall(r"(-?\d+(?:\.\d+)?)px", m.group(m.lastindex)):
                        v = abs(float(px))
                        if v % 5 != 0 and v not in allowed:
                            issues.append(("WARN", n, f"{label} {px}px is off the 5px scale"))
    return issues


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    errors = 0
    for path in argv:
        for level, n, msg in lint(path):
            errors += level == "ERROR"
            print(f"{path}:{n}: {level}: {msg}")
    print(f"\n{errors} error(s)." if errors else "\nNo errors. Editorial Taste approved.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
