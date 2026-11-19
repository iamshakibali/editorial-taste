# Editorial Taste

Two Claude Code skills for monochrome, editorial, photography-led websites: Geist and Geist Mono type, #151515 and #EDEDED with opacity steps, a 5px spacing rhythm, glass blur instead of shadows, full-bleed photos behind vignettes, buttery motion, and isometric hairline illustrations.

| Skill | Use it to |
|---|---|
| `editorial-taste-new-site` | Build a new site or landing page. Asks which stack to use (Astro, Next.js/React, plain HTML, Vue, Svelte), runs intake, picks a page type, writes editorial copy, and composes a fresh layout per site on top of a tested starter system with a full motion system and generated isometric illustrations |
| `editorial-taste-redesign` | Restyle an existing site (HTML, React, Next.js, Tailwind, shadcn, MUI). Audits and diagnoses generic patterns, maps old styles to tokens, restyles section by section, then runs a motion pass and replaces clip-art with hairline illustrations, without breaking content or behavior |

Both work in code and in Figma.

## Install

**As a Claude Code plugin (recommended).** Run these as two separate commands:
```
/plugin marketplace add iamshakibali/editorial-taste
```
```
/plugin install editorial-taste@editorial-taste
```
Then run `/reload-plugins`.

**With the skills CLI** (Claude Code, Cursor, Codex and other agents):
```bash
npx skills add iamshakibali/editorial-taste
```

**Manually**
```bash
git clone https://github.com/iamshakibali/editorial-taste /tmp/editorial-taste
cp -R /tmp/editorial-taste/skills/* ~/.claude/skills/        # all projects
# or: cp -R /tmp/editorial-taste/skills/* .claude/skills/    # this project only
```

## Usage

Ask in plain language:
- "Build a landing page for a coffee roastery in Editorial Taste."
- "Redesign this site with Editorial Taste."
- "Audit this page against Editorial Taste."

## What's inside

```
skills/
├── editorial-taste-new-site/
│   ├── SKILL.md            intake → page type → plan → build → verify → report
│   ├── templates/          index.html, styles.css, motion.js, 404.html, favicon.svg
│   ├── references/         shared reference set (below)
│   └── scripts/            lint.py, iso.py
└── editorial-taste-redesign/
    ├── SKILL.md            audit → diagnose → map → foundation → sections → verify → report
    ├── references/         shared reference set
    └── scripts/
        ├── map_tokens.py   maps an existing site's styles to tokens
        ├── iso.py          isometric illustration generator
        └── lint.py
```

| Reference | Covers |
|---|---|
| `motion.md` | Easing and duration tokens, every animation, HTML API, Astro/React/GSAP/Tailwind recipes, performance budget |
| `illustrations.md` | Isometric hairline illustration rules, generator spec, compositions |
| `foundations.md` | Color, type, spacing, radius, grid, effects, motion, icons, contrast |
| `components.md` | Buttons, nav, cards, statement, FAQ, forms, states, layout variety, page blocks |
| `layouts.md` | Layout signature, variation rules, 8 hero variants, section patterns by job, recipes, example compositions |
| `copy.md` | Voice, headline formulas, CTAs, content realism, banned filler |
| `ship-checklist.md` | Style, content, states, accessibility, SEO, and responsive QA |
| `frameworks.md` | Next.js, Tailwind v3/v4, shadcn, MUI |
| `figma.md` | Variables, modes, text styles, and components in Figma |
| `pitfalls.md` | Common mistakes and generic patterns to diagnose |
| `tokens.css` | The drop-in token set |

## Scripts

```bash
# Check code against the rules (add --strict to fail on leftover {{placeholders}})
python3 skills/editorial-taste-new-site/scripts/lint.py ./site

# Generate an isometric hairline illustration (presets: modules, stack, flow, single)
python3 skills/editorial-taste-new-site/scripts/iso.py --preset modules > modules.svg

# Get a token replacement plan for an existing codebase
python3 skills/editorial-taste-redesign/scripts/map_tokens.py ./src
```

Add `lint-ok` in a comment on a line to accept a deliberate exception.

## Contributing

The reference files and `lint.py` are shared, so keep them identical in both skills. CI runs `python scripts/validate.py`, which checks the skill frontmatter, the referenced files, that shared files are in sync, and that the template passes the linter.

## License

MIT
