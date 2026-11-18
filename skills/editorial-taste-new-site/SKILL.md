---
name: editorial-taste-new-site
description: Editorial Taste — create a brand-new website or landing page from scratch in a monochrome, editorial, photography-led style (Geist + Geist Mono, #151515 / #EDEDED alpha ramps, 5px spacing rhythm, glass blur instead of shadows, full-bleed photos with vignettes). Use when the user asks to build, create, scaffold, or design a new site, landing page, homepage, or marketing page with Editorial Taste, an editorial / minimal / monochrome / premium look, or "in our style". Not for restyling an existing site; use editorial-taste-redesign for that.
---

# Editorial Taste: New site

Builds a new site in the Editorial Taste style. It's **monochrome, editorial, and photography-led**: the UI is achromatic, and color comes only from photography. Start from the bundled template, which is complete, responsive, accessible, and passes the linter, then adapt it rather than writing from a blank file.

## Non-negotiable rules

1. **No accent colors.** Use only the neutral ramp, `--light-*` (#EDEDED alpha), `--dark-*` (#151515 alpha), and semantic tokens. Express hierarchy with alpha steps.
2. **Two type voices.** Geist Medium for headings, Geist Regular for body. **Geist Mono only** for buttons, nav, labels, tags, and eyebrows. Never use bold headings. Headings use negative tracking and line-height ≤ 1.0× at display sizes.
3. **5px rhythm.** Spacing and radii come from the 5-step scale (the compact-scale exceptions are 8, 12, 32, 56, and 96).
4. **Glass, not shadow.** No `box-shadow`. For depth, use translucent fills plus `backdrop-filter: blur(16px)`.
5. **Text on photos always sits on a vignette.** Use white text, subtitles in `--light-88`, and a white logo on photos (dark logo on light surfaces).
6. **Radii:** buttons 8 · cards 10 · case cards 20 · chips and pill CTAs full pill. Don't mix radii within a row.

## Workflow

### 1. Get the brief
From the request or the repo, collect: brand name, what the brand does and for whom, the primary action (e.g. "Book a demo"), the sections needed, and available photography and logo. **Don't block on a missing detail.** Use sensible placeholders and list what's assumed at the end. Ask only if the brand or purpose is unknowable.

### 2. Choose the stack
- No existing project or no preference → plain `index.html` + `styles.css` (copy the template).
- Existing Next.js / React / Vue / Astro project → port the template into components (see `references/frameworks.md`).
- Tailwind project → map tokens in the theme (`references/frameworks.md`), but keep `tokens.css` as the source of truth.

### 3. Scaffold from the template
Copy `templates/index.html` and `templates/styles.css` from this skill's directory into the target. The template contains these sections:

Nav → Hero (split) → Highlight numbers → Product cards → Case cards → Split cards → Journal (news cards) → CTA band (+ email form) → Footer, plus a mobile drawer, scroll reveal, solid-on-scroll nav, and expandable case cards.

Then:
- Replace every `{{placeholder}}` with real or plausible brand copy. Run `grep -n '{{' index.html` at the end; it should return nothing.
- **Delete blocks the content doesn't need.** Never invent content to fill a block. Add blocks only from `references/components.md`.
- Swap the `#logo` symbol for the client's SVG logo (keep `fill="currentColor"`). Otherwise keep the text wordmark.
- Point images at real photography. Without client images, keep descriptive `alt` text and either use neutral gray placeholder blocks (`background: var(--neutral-300)`) or ask the user for photos. Don't hotlink random stock URLs.
- Update `<title>`, the meta description, and the anchor IDs and nav links so they match the remaining sections.

### 4. Write copy in the editorial voice
- Headlines: short, declarative, sentence case, ending with a period. ("Clean data, built to last.")
- Eyebrows: mono, uppercase, numbered sections ("01 — Product").
- Body: two or three plain sentences. Concrete nouns and numbers rather than adjectives.
- Stats: 3–4 values that fit in about 5 characters (`98%`, `12Y`, `40+`, `24/7`).
- CTAs: 1–3 words ("Explore", "Contact us", "How it works").
- No exclamation marks, emoji, or Title Case Headlines.

### 5. Verify
1. Lint, then fix every ERROR:
   `python3 <skill-dir>/scripts/lint.py styles.css index.html`
2. Check that no placeholders remain: `grep -n '{{' index.html`.
3. Open the page and check it at 1440px and 390px widths. Check that the nav turns solid after the hero, the drawer opens, case cards expand, nothing scrolls horizontally, and every photo with text has its vignette.
4. Check accessibility: every interactive element has a visible focus ring, images have alt text, there's one `h1`, headings are in order, and muted text on `--neutral-200` meets 4.5:1 (switch to `--neutral-600` if not).

### 6. Report
Summarize the sections built, the assumptions made (placeholder copy, missing images or logo), and what the user should supply next.

## Quick token reference (web desktop)

| Need | Token |
|---|---|
| Page background | `--bg-base` #EDEDED |
| Hover fill / raised surface | `--bg-lift` #D9D9D9 |
| Primary text, primary button | `--tone-strong` #151515 |
| Secondary text | `--text-muted` #737373 / `--tone-medium` |
| Hairlines, chip fill, disabled | `--border-subtle` / `--tone-faint` |
| Glass on a photo | `--light-16` + `--blur-glass` |
| Container / margin / gutter | 1280 / 40 / 20 (mobile: fluid / 20 / 12) |
| Section padding / title→content | 96 / 32 (mobile 64 / 24) |

| Role | Style |
|---|---|
| Hero headline | `.h2` 40/44 |
| Section title | `.h3` 32/36 |
| Card title | `.h4` 24/28 (case card `.h5` 20/24) |
| Stat value | `.h1` 48/48 |
| Paragraph | `.body-md` 15/22 |
| Eyebrow / tag | `.label-lg` / `.eyebrow` 11/14 mono uppercase |

## Accessibility (always include)
`:focus-visible` ring (2px `--tone-strong`, offset 2; `--light-100` on photos) · disabled state (`--tone-faint`, `cursor: not-allowed`) · pressed state · `prefers-reduced-motion` respected · skip link · `aria-expanded` on toggles.

## Reference files
- `templates/index.html`, `templates/styles.css`: the starter site
- `references/foundations.md`: full color, type, spacing, radius, grid, and effects tables
- `references/components.md`: anatomy of every component and page block
- `references/tokens.css`: the token set on its own, for framework projects
- `references/frameworks.md`: setup for Next.js, Tailwind v3/v4, and shadcn/MUI
- `references/pitfalls.md`: common mistakes to check before finishing
- `scripts/lint.py`: rule checker
