---
name: editorial-taste-new-site
description: Editorial Taste — create a brand-new website or landing page from scratch in a monochrome, editorial, photography-led style (Geist + Geist Mono, #151515 / #EDEDED alpha ramps, 5px spacing rhythm, glass blur instead of shadows, full-bleed photos with vignettes, a word-by-word statement section). Covers intake, page structure, editorial copy, a tested starter template, states, and a ship checklist. Use when the user asks to build, create, scaffold, or design a new site, landing page, homepage, or marketing page with Editorial Taste, an editorial / minimal / monochrome / premium look, or "in our style", in code or in Figma. Not for restyling an existing site; use editorial-taste-redesign for that.
---

# Editorial Taste: New site

Builds a new site in the Editorial Taste style. It's **monochrome, editorial, and photography-led**: the UI is achromatic, color comes only from photography, and the words carry the page. Start from the bundled template, which is complete, responsive, accessible, and passes the linter, then adapt it rather than writing from a blank file.

Work through **Part A (what the page says)** before **Part B (how it looks)**.

## Non-negotiable rules

1. **No accent colors.** Use only the neutral ramp, `--light-*` (#EDEDED alpha), `--dark-*` (#151515 alpha), and semantic tokens. Express hierarchy with alpha steps.
2. **Two type voices.** Geist Medium for headings, Geist Regular for body. **Geist Mono only** for buttons, nav, labels, tags, and eyebrows. No bold headings and no italics.
3. **5px rhythm.** Spacing and radii come from the 5-step scale (the compact-scale exceptions are 8, 12, 32, 56, and 96). Nested radii: `inner = outer − gap`.
4. **Glass, not shadow.** No `box-shadow`. For depth, use translucent fills plus `backdrop-filter: blur(16px)`. The only gradients allowed are black vignettes over photos.
5. **Text on photos always sits on a vignette.** Use a white logo on photos and a dark logo on light surfaces.
6. **Radii:** buttons 8 · cards 10 · case cards 20 · chips and pills full. Don't mix radii within a row.
7. **Motion decelerates** (`var(--ease)`, 200/400/800ms). Animate only transform and opacity, and respect reduced motion.
8. **Never invent facts** for a real business. Missing prices, stats, testimonials, and logos stay as marked `{{placeholders}}`.

---

# Part A: Strategy and content

## A1. Intake: ask once, in one batch
Collect what's missing in **a single message**, never one question at a time:
- **Brand**: name, what it does, for whom, and the one thing that makes it different.
- **Goal**: the one primary action (book, buy, contact, join a waitlist) and what counts as a conversion.
- **Audience**: who they are, what they already know when they land, and their top 2–3 objections.
- **Proof**: real numbers, clients, case studies, testimonials, press.
- **Assets**: logo SVG, photography (the style depends on it), existing copy.
- **Constraints**: stack or framework, pages beyond the homepage, deadline, whether it's indexed or campaign-only.

If the user doesn't answer or says "just build it", make reasonable assumptions, state each in one line, and continue. Don't stall the build.

## A2. Choose the page type, and say why
| Type | Use when | Blocks |
|---|---|---|
| **Editorial homepage** | A brand with several products or audiences | Hero → Stats → Statement → Product cards → Case cards → Split → Journal → FAQ → CTA band |
| **Product landing** | One offer, one audience, one action | Hero → Stats → Statement → Split (how it works) → Case cards (proof) → FAQ → CTA band |
| **Long-form story** | The audience needs educating or convincing | Centered hero → Statement → alternating Split cards → Stats → Case cards → FAQ → CTA band |
| **Minimal conversion** | High-intent traffic: waitlist, download, event | Centered hero with form → Stats → FAQ → Footer |

**One primary action per page.** The hero gets one light button plus at most one glass button.

## A3. Plan before code
Before writing code, post a short plan (don't wait for approval unless the user asked to review first):
1. Page type and why
2. Section outline in order
3. Hero copy: headline, paragraph, CTAs, and a proof line or stats
4. Statement line (2–4 lines)
5. FAQ: 6–10 real questions
6. Assumptions and missing assets (become `{{placeholders}}`)
7. SEO: index or noindex, plus title and meta description

## A4. Copy
Follow `references/copy.md`: declarative headlines ending in a period, sentence case, numbered mono eyebrows, CTAs built from a verb and an object, concrete numbers, no filler words, and calm, specific system messages.

---

# Part B: Build

## B1. Choose the stack
- No project or no preference → plain `index.html` + `styles.css` (copy the template).
- Existing Next.js / React / Vue / Astro project → port the template into components (`references/frameworks.md`).
- Tailwind → map the tokens in the theme, keeping `tokens.css` as the source of truth.
- Figma → follow `references/figma.md` (variables, modes, text styles, auto layout, components with every state).

## B2. Scaffold from the template
Copy everything in `templates/` from this skill's directory: `index.html`, `styles.css`, `404.html`, `favicon.svg`. The template includes:

Nav (glass over the hero, solid on scroll, mobile drawer with staggered links) → Hero (split) → Highlight numbers → **Statement** (word-by-word reveal) → Product cards → Case cards (expandable) → Split cards → Journal → **FAQ** → CTA band with an email form → Footer, plus meta and OG tags, a skip link, scroll reveal, and reduced-motion handling.

## B3. Build section by section
Order: Hero → Stats → Statement → main content sections → FAQ → CTA → Footer → 404. For each section:
- Replace its `{{placeholders}}` with the planned copy, and point images at real photography. With no photos, use neutral blocks (`background: var(--neutral-300)`) with descriptive alt text, and ask for photos. Never hotlink random stock images.
- **Delete blocks the content doesn't support.** Add blocks only from `references/components.md`, and vary layouts (3-up, 2-up, 5/7, feature + list) so the page doesn't repeat the same grid.
- Swap the `#logo` symbol for the client's SVG logo (keep `fill="currentColor"`), and update the favicon letter.
- Keep diffs per section. Don't regenerate the whole page on every iteration.

## B4. States and details
Every interactive element has hover, pressed, focus-visible, and disabled states. Forms validate inline. Data areas get loading, empty, and error states. Mark the current nav item with `aria-current="page"`. No dead `href="#"` links. Specs are in `references/components.md` under States and Forms.

## B5. Verify
1. `python3 <skill-dir>/scripts/lint.py <project-dir>`: fix every ERROR and review the WARNs.
2. `python3 <skill-dir>/scripts/lint.py --strict index.html`: catches leftover `{{placeholders}}`.
3. Open the page at 1440, 768, and 390px widths. Check the nav switches state, the drawer opens and closes, the statement lights up word by word, FAQ items toggle, nothing scrolls horizontally, and every photo with text has its vignette.
4. Work through `references/ship-checklist.md`.

## B6. Report
Summarize the page type, the sections built, the assumptions made, any remaining `{{placeholders}}` (real facts the user must supply), and the missing assets (photos, logo, legal pages).

---

## Quick token reference (web desktop)

| Need | Token |
|---|---|
| Page background | `--bg-base` #EDEDED (white for card-heavy pages) |
| Hover fill / raised surface | `--bg-lift` #D9D9D9 |
| Primary text, primary button | `--tone-strong` #151515 |
| Secondary text | `--text-muted` #737373 (`--neutral-600` on gray surfaces) |
| Hairlines, chip fill, disabled | `--border-subtle` / `--tone-faint` |
| Glass on a photo | `--light-16` + `--blur-glass` |
| Container / margin / gutter | 1280 / 40 / 20 (mobile: fluid / 20 / 12) |
| Section padding / title→content | 96 / 32 (mobile 64 / 24) |
| Motion | `--ease`, `--dur-fast` .2s, `--dur-base` .4s, `--dur-slow` .8s |

| Role | Style |
|---|---|
| Statement | `.h0` 72/68 |
| Hero headline | `.h2` 40/44 |
| Section title | `.h3` 32/36 |
| Card title | `.h4` 24/28 (case card `.h5` 20/24) |
| Stat value | `.h1` 48/48 |
| Paragraph | `.body-md` 15/22 |
| Eyebrow / tag | `.eyebrow` / `.label-lg` 11/14 mono uppercase |

## Reference files
- `templates/`: `index.html`, `styles.css`, `404.html`, `favicon.svg`
- `references/foundations.md`: color, type, spacing, radius, grid, effects, motion, icons, contrast
- `references/components.md`: anatomy of every component and block, forms, states, layout variety
- `references/copy.md`: voice, headline formulas, CTAs, content realism, banned words
- `references/ship-checklist.md`: final QA, SEO, and ship requirements
- `references/frameworks.md`: Next.js, Tailwind v3/v4, shadcn/MUI
- `references/figma.md`: building in Figma
- `references/pitfalls.md`: common mistakes and generic patterns to avoid
- `references/tokens.css`: the token set on its own
- `scripts/lint.py`: rule checker (`--strict` for delivery)
