# Editorial Taste

Two Claude Code skills for monochrome, editorial, photography-led websites: Geist and Geist Mono type, #151515 and #EDEDED with opacity steps, a 5px spacing rhythm, glass blur instead of shadows, and full-bleed photos behind vignettes.

| Skill | Use it to |
|---|---|
| `editorial-taste-new-site` | Build a new site or landing page from a tested, responsive starter template |
| `editorial-taste-redesign` | Restyle an existing site (HTML, React, Next.js, Tailwind, shadcn, MUI) without breaking its content or behavior |

## Install

**As a plugin (recommended)**
```
/plugin marketplace add iamshakibali/editorial-taste
/plugin install editorial-taste@editorial-taste
```

**Or copy the skills manually**
```bash
git clone https://github.com/iamshakibali/editorial-taste /tmp/editorial-taste
cp -R /tmp/editorial-taste/skills/* ~/.claude/skills/        # all projects
# or: cp -R /tmp/editorial-taste/skills/* .claude/skills/    # this project only
```

## Usage

Ask Claude in plain language:
- "Build a landing page for a coffee roastery in Editorial Taste."
- "Redesign this site with Editorial Taste."

## Structure

```
skills/
├── editorial-taste-new-site/
│   ├── SKILL.md
│   ├── templates/          index.html + styles.css starter site
│   ├── references/         foundations, components, tokens.css, frameworks, pitfalls
│   └── scripts/lint.py
└── editorial-taste-redesign/
    ├── SKILL.md
    ├── references/         (same reference set)
    └── scripts/
        ├── map_tokens.py   maps an existing site's styles to tokens
        └── lint.py
```

## Scripts

```bash
python3 skills/editorial-taste-redesign/scripts/map_tokens.py ./src     # replacement plan for an existing site
python3 skills/editorial-taste-new-site/scripts/lint.py styles.css index.html   # rule check
```

## License

MIT
