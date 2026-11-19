#!/usr/bin/env python3
"""Validate the Editorial Taste skills.

Checks:
  - each skills/<name>/SKILL.md has frontmatter with a valid name equal to its folder
    and a description of at most 1024 characters
  - every file a SKILL.md mentions under references/, templates/ or scripts/ exists
  - shared files (references/*, scripts/lint.py) are identical across skills
  - the starter template passes lint.py with no errors
Exit 1 on any problem.
"""
import filecmp
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SHARED = ["scripts/lint.py", "scripts/iso.py", "scripts/images.py"]


def frontmatter(text):
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    data = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            k, v = line.split(":", 1)
            data[k.strip()] = v.strip().strip('"')
    return data


def main():
    problems = []
    dirs = sorted(p for p in SKILLS.iterdir() if p.is_dir())
    for d in dirs:
        f = d / "SKILL.md"
        if not f.is_file():
            problems.append(f"{d.name}: SKILL.md missing")
            continue
        text = f.read_text(encoding="utf-8")
        fm = frontmatter(text)
        if fm is None:
            problems.append(f"{d.name}: invalid or missing frontmatter")
            continue
        name, desc = fm.get("name", ""), fm.get("description", "")
        if not NAME_RE.match(name) or len(name) > 64:
            problems.append(f"{d.name}: invalid name '{name}'")
        if name != d.name:
            problems.append(f"{d.name}: name '{name}' does not match folder")
        if not desc or len(desc) > 1024:
            problems.append(f"{d.name}: description length {len(desc)} (must be 1-1024)")
        for ref in sorted(set(re.findall(r"`((?:references|templates|scripts)/[\w./-]+\.\w+)`", text))):
            if not (d / ref).exists():
                problems.append(f"{d.name}: SKILL.md mentions missing file {ref}")

    first = dirs[0]
    shared = SHARED + [f"references/{p.name}" for p in (first / "references").iterdir()]
    for other in dirs[1:]:
        for rel in shared:
            a, b = first / rel, other / rel
            if not b.exists() or not filecmp.cmp(a, b, shallow=False):
                problems.append(f"{other.name}/{rel} differs from {first.name}/{rel}")

    tpl = SKILLS / "editorial-taste-new-site" / "templates"
    lint = SKILLS / "editorial-taste-new-site" / "scripts" / "lint.py"
    res = subprocess.run([sys.executable, str(lint), str(tpl)], capture_output=True, text=True)
    if res.returncode != 0:
        problems.append("template fails lint:\n" + res.stdout)

    for p in problems:
        print(f"✗ {p}")
    print(f"Checked {len(dirs)} skill(s): {'OK' if not problems else f'{len(problems)} problem(s)'}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
