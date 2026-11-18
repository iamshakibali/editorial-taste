---
name: editorial-taste-redesign
description: Editorial Taste — redesign or restyle an existing website, app, or page into a monochrome, editorial, photography-led style (Geist + Geist Mono, #151515 / #EDEDED alpha ramps, 5px spacing rhythm, glass blur instead of shadows) while preserving its content, structure, routes, and functionality. Use when the user asks to redesign, restyle, reskin, refresh, modernize, or "make it look editorial / premium / minimal" for a site or codebase that already exists, including Tailwind, React, Next.js, Vue, or plain HTML/CSS. For building a new site from scratch, use editorial-taste-new-site.
---

# Editorial Taste: Redesign

Restyles an existing site in the Editorial Taste style: **monochrome, editorial, photography-led**. A redesign changes the **visual layer**. Content, information architecture, URLs, behavior, forms, SEO metadata, and analytics stay intact unless the user asks otherwise.

## Non-negotiable rules

1. **No accent colors.** Use only the neutral ramp, `--light-*` (#EDEDED alpha), `--dark-*` (#151515 alpha), and semantic tokens. Brand accent colors are removed from the UI; the brand's color lives in its photography. If the user insists on keeping a brand color, confine it to the logo.
2. **Two type voices.** Geist Medium for headings, Geist Regular for body. **Geist Mono only** for buttons, nav, labels, tags, and eyebrows. Never use bold headings.
3. **5px rhythm** for spacing and radii (the compact-scale exceptions are 8, 12, 32, 56, and 96).
4. **Glass, not shadow.** Remove every shadow; use translucent fills plus `backdrop-filter: blur(16px)`, or a `--border-subtle` hairline.
5. **Text on photos always sits on a vignette.**
6. **Radii:** buttons 8 · cards 10 · case cards 20 · chips and pills full.

## Workflow

### 1. Audit what exists (read before you write)
- Identify the stack: plain HTML/CSS, Tailwind (v3 config or v4 `@theme`), CSS Modules, styled-components, or a component library (shadcn, MUI, Chakra).
- List the pages and shared components (layout, nav, footer, buttons, cards, forms).
- Run the token mapper over the source to get a replacement plan:
  `python3 <skill-dir>/scripts/map_tokens.py <src-dir-or-files>`
  It maps every color, font, size, spacing value, radius, shadow, and Tailwind utility to the nearest Editorial Taste token, and flags accents and shadows for removal.
- Note what must not break: forms, auth, routing, JavaScript hooks that depend on class names or IDs, CMS-driven content, and tests or snapshots that assert on markup.
- If the project can run, take "before" screenshots at 1440px and 390px.

### 2. Map content to Editorial Taste blocks
Keep the existing content and pick the closest block for each section (see `references/components.md`):

| Existing section | Editorial Taste block |
|---|---|
| Hero / banner | Hero (split or centered): full-bleed photo + vignettes; or, with no photo, a `--bg-base` hero with a large H0/H2 |
| Feature grid with images | Product cards (3) or split cards (2) |
| Feature list without images | Intro (split) + a 3-column grid of news-card surfaces with H4 + body |
| Testimonials / case studies | Case cards |
| Blog / news / resources | Journal (news cards) |
| Stats / metrics | Highlight numbers |
| Logo wall | Monochrome logos (`grayscale(1)`, 64% opacity) in a row with gutter 20 |
| Pricing | News-card surfaces (r10, white), H4 plan name, H1 price, Body Medium list, Primary CTA on the featured plan only. No colored badges; use a mono tag chip |
| FAQ | Hairline-divided list (`--border-subtle`), H6 questions, Body Medium answers, a mono "+" toggle |
| Newsletter / contact CTA | CTA band |
| Forms | 40px-high inputs, radius 8, 1px `--border-subtle`, `--neutral-white` fill, mono labels, Primary submit, focus ring `--tone-strong` |

If the site has no photography, say so: the style depends on it. Use the user's existing images with vignettes, or ask for photos. Don't hotlink stock images.

### 3. Install the foundation (global first)
1. Add the fonts and `references/tokens.css` (or map them in the framework theme; see `references/frameworks.md`).
2. Replace global styles: body background, text color, font families, and base heading and link styles.
3. Retheme shared primitives at the source: the Button component, Card, Input, and theme config (Tailwind or a component library). One change at the source is better than 100 per-instance overrides.
4. Delete the old palette, shadow, and font tokens once nothing references them. Don't leave two systems side by side.

### 4. Restyle section by section
Order: Nav → Footer → Hero → each section top to bottom → remaining pages. For each one:
- Apply the mapped block anatomy (sizes, gaps, text styles).
- Swap colors, fonts, spacing, radii, and shadows using the mapper report.
- Keep the DOM, IDs, `data-*` attributes, ARIA, and event handlers. Change class names only where the styling system requires it, and keep any class that JavaScript or tests query.
- Tighten copy only if the user asked. Otherwise, keep the wording and change only casing (sentence case for headings, uppercase for mono eyebrows).

### 5. Verify
1. Run the linter on the changed style and markup files and fix every ERROR:
   `python3 <skill-dir>/scripts/lint.py <files…>`
2. Re-run `map_tokens.py`. The Colors table should contain no `ACCENT` rows and the Shadows section should be empty.
3. Run the project's existing build, type-check, and tests. Nothing that passed before should fail.
4. Run the app and compare against the "before" screenshots at 1440px and 390px. Check that all content is still present, links and forms work, nothing scrolls horizontally, focus rings are visible, and contrast meets AA.

### 6. Report
List what changed (foundation, components, sections), what was kept deliberately, anything not mapped cleanly (e.g. charts that need a monochrome palette), and what the user should supply (photography, logo SVG).

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
| Hero headline | H2 40/44/−1.5 |
| Section title | H3 32/36/−1 |
| Card title | H4 24/28/−0.75 |
| Stat value | H1 48/48/−1.5 |
| Paragraph | Body Medium 15/22 |
| Eyebrow / tag / button | Geist Mono 11–13px |

## Accessibility (always include)
`:focus-visible` ring (2px `--tone-strong`, offset 2; `--light-100` on photos) · disabled state (`--tone-faint`) · pressed state · `prefers-reduced-motion` · AA contrast (use `--neutral-600` instead of `--neutral-500` on gray surfaces if needed). Never remove existing accessibility features during a redesign.

## Reference files
- `references/foundations.md`: full color, type, spacing, radius, grid, and effects tables
- `references/components.md`: anatomy of every component and page block
- `references/tokens.css`: the drop-in token set
- `references/frameworks.md`: Next.js, Tailwind v3/v4, and shadcn/MUI theme mapping
- `references/pitfalls.md`: common mistakes to check before finishing
- `scripts/map_tokens.py`: inventories existing styles and maps them to tokens
- `scripts/lint.py`: rule checker
