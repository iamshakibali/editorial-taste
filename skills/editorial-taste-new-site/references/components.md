# Editorial Taste — Components and Blocks

Sizes are given as **canvas (1920) → web desktop** where they differ. Class names match `templates/styles.css`.

## Button
Variants: `Style` Primary | Secondary | Tertiary · `Size` Large | Small · `Icon` None | Left | Right · `State` Default | Hover | Focus | Disabled.

Anatomy: inline-flex, centered, radius 8, 1px transparent border, Geist Mono label, 12px icon (20px for icon-only Large).

| Size | Height | Padding | Gap | Text |
|---|---|---|---|---|
| Large | 44 → 40 | 12×20 → 10×18 (16 on icon side) | 8 | Button Large |
| Small | 32 → 30 | 10×12 → 8×12 | 4 with icon, else 8 | Button Small |
| Icon-only Large | 44 | 12×8 | — | 20px icon |
| Icon-only Small | 28 | 8×8 | — | 12px icon |
| Tertiary | auto | 0 horizontal | 8 / 4 | mono |

| Style | Default | Hover |
|---|---|---|
| Primary | bg tone-strong, text light-100 | bg bg-lift, text tone-strong, border dark-8 |
| Secondary | bg dark-8, text tone-strong, blur 16 | bg bg-lift, border dark-8, blur 16 |
| Tertiary | no bg, text tone-strong | text dark-88 |
| On-image light (`.btn--light`) | bg #FFF, text tone-strong | bg bg-lift |
| On-image glass (`.btn--glass`) | bg light-16, text light-100, blur 16 | bg light-32 |
| Pill CTA (`.btn--pill`) | radius pill, padding 12×30 → 10×22 | — |

Wide CTA min-width: 200 → 160 (`.btn--wide`).

```html
<a class="btn btn--primary btn--wide" href="#">Get started</a>
<a class="btn btn--secondary" href="#">Learn more</a>
<a class="btn btn--tertiary" href="#">Read all <svg width="12" height="12" aria-hidden="true">…</svg></a>
```

## Circle button
50 → 40px circle with a 20px "+" icon. Default: white fill, black icon. Active: black fill, white icon. Used as the expand affordance in the top-right corner of a case card.

## Logo
Wordmark, about 125×24 → 104×20 (mobile 92×18), set as an SVG with `fill="currentColor"`. Use `--tone-strong` on light surfaces and white on photos. Always give it an accessible name.

## Nav bar
Full width, height ≈64, side padding = page margin. `justify-content: space-between`: logo on the left; on the right, nav links (gap 8, mono chips), a 40 gap, then utility icons in 32×32 hit areas with radius 4. Over imagery, links render as glass pills and the logo switches to white. After scrolling past the hero, the nav turns solid (`--bg-base`, dark logo). On mobile, collapse the links into a full-screen drawer.

## Title group
Column, gap 15. Default = H5 only; Expanded = H5 plus Body Medium in muted.

## Intro block (section header)
| Variant | Layout |
|---|---|
| Split | Row, `space-between`: optional mono eyebrow ("01 — Product") + H3 on the left; the right column (max ≈560) holds Body Medium muted and an optional button |
| Simple | Row, `space-between`, aligned to the end: eyebrow + H3 on the left; tertiary "View all →" on the right |
| Centered | Centered column, gap 30: H2, Body Medium in neutral-700, centered button row |

## Cards
| Card | Size (canvas → web min-h) | Surface | Structure |
|---|---|---|---|
| **Case** `.card-case` | 734 → 480 (mobile 340) | neutral-200, **r20**, pad 40 → 24 | Column with space-between: circle button top-right; title group (kicker, H5, expandable body) at the bottom. Optional photo + bottom vignette + white text |
| **News** `.card-news` | 480 → 320 (220) | white (neutral-200 in grids), r10, pad 25 → 20 | Top: Label Large eyebrow + H4 (gap 15). Bottom row: date (Body Medium) ↔ read time (Body Small, muted) |
| **Split** `.card-split` | 657 tall | none | Image (r10, ratio ≈16:9.25), gap 35 → 20, H4 + Body Medium muted (gap 15) |
| **Product** `.card-product` | 772 → 520 (420) | full-bleed image + bottom vignette, r10, pad 24 | Content pinned to the bottom: tag chip → H4 → Body Medium → light pill "Explore" CTA |

Tag chip: Label Large mono, uppercase, `tone-faint` (or light-16 on a photo) + blur 15, pill radius, with a 3px `neutral-400` dot separator (`<i></i>` in the template).

```html
<article class="card-product">
  <div class="card-product__media"><img src="…" alt="…"></div>
  <div class="card-product__body">
    <div class="card-product__head">
      <span class="tag">Category<i></i>Type</span>
      <h3 class="h4">Product name</h3>
    </div>
    <p class="body-md">One-line benefit.</p>
    <a class="btn btn--light btn--pill" href="#">Explore</a>
  </div>
</article>
```

## Highlight numbers
Full-width row, block padding 56 (mobile 40), equal grid columns, items centered. Each item: an **H1** value (`98%`, `12Y`, `40+`) over a **Body Large** muted caption, gap 10. Use `font-variant-numeric: tabular-nums`. 3–4 items.

## Statement (word-by-word reveal)
One per page. It's the editorial signature: a single large statement of the brand's core idea, set apart from the hero. Place it after the stats or between two card sections, never directly under the hero.
- Copy: 2–4 lines, one idea, written as a statement (see `copy.md`). It isn't a section heading.
- Type: `.h0` (`.h1` if the statement is over about 18 words), max-width about 1040px, left-aligned.
- Motion: each word starts at `--dark-16` and turns `--tone-strong` in reading order as it crosses a trigger line about 60% down the viewport, over 400ms with `--ease`. Use one `IntersectionObserver` per word (see the template script), never an unthrottled scroll handler. Under reduced motion, show the full color immediately.
- Padding: 1.5 × the section padding.

```html
<section class="statement" aria-label="Brand in one statement">
  <div class="container"><p class="h0 statement__text" data-words>We build the quiet infrastructure that keeps a city running.</p></div>
</section>
```

## Illustration split
A 5/7 split: on the left, an eyebrow, an H3 (`data-reveal="text"`), Body Medium muted (max 460), and a numbered step list (Label Large mono numbers, hairline dividers, `data-stagger`). On the right, a `figure.illo` on a `--bg-base` panel (radius 10) holding an inline isometric SVG from `scripts/iso.py` with `data-reveal="iso"`. Match the step numbers to the labels in the drawing. It stacks to one column at ≤1024. Rules and recipes are in `illustrations.md`.

## FAQ
5/7 split: eyebrow + H3 on the left; on the right, a list of `<details>` items divided by `--border-subtle` hairlines (full width, never borders on a single side of a card). Each question is an H6 `summary` with a 14px "+" icon that rotates 45° when open; each answer is Body Medium muted, max-width 640. Use 6–10 real objections. Add `FAQPage` JSON-LD when the page is indexed.

## Forms
- Input: 40px high, padding 0 14px, radius 8, 1px `--border-subtle`, fill `--neutral-white`, Body Medium text, placeholder `--neutral-400`.
- Label: Label Large mono uppercase, above the field, gap 8. Never use the placeholder as the only label.
- States: hover → border `--dark-32`; focus → 2px `--tone-strong` outline, offset 2; error → border `--tone-strong` plus an inline message with a "!" icon (state is never shown by color alone); disabled → fill `--dark-4`, text `--tone-faint`.
- Messages: Label Large in `aria-live="polite"` beneath the field. Validate required fields and email format on the client.
- Submit: Primary button. On photos, the input is glass (`--light-16` + blur) with light text and the button is `.btn--light`.

## States (every interactive element)
| State | Treatment |
|---|---|
| Hover | Background moves to `--bg-lift` (light) or `--light-32` (glass), over 200ms. Labels roll up and arrows nudge 2px (see `motion.md`) |
| Pressed | `translateY(1px)` |
| Focus | 2px outline in `--tone-strong` (or `--light-100` on photos), offset 2–3px |
| Disabled | `--dark-4` fill, `--tone-faint` text, `cursor: not-allowed`, `aria-disabled="true"` |
| Current | Nav link with `aria-current="page"`: solid `--tone-strong` chip (white chip on photos) |
| Loading | Skeleton blocks in `--neutral-200` with radius matching the real element and a gentle opacity pulse. No spinners |
| Empty | A composed view: H5, one line of muted Body Medium, one Secondary button that tells the user what to do next |
| Error | Inline, specific, in mono Label Large, with a retry action. Never `alert()` |

## Layout variety
Don't default to three equal cards in every section. Rotate layouts across the page:
- **3-up**: product cards and case cards.
- **2-up split**: split cards, 1:1.
- **Asymmetric 5/7 or 4/8**: intro and FAQ, or a large image beside a text column.
- **Feature + list**: one large case card (span 2) beside two stacked small ones.
- **Full-bleed**: hero and CTA band. Use one or two per page, not more.

Align shared elements across side-by-side cards: titles, tags, and buttons start at the same height (use a grid with `align-items: stretch` and `margin-top: auto` on the card footer).

## Page blocks
| Block | Recipe |
|---|---|
| **Hero (split)** | min(100vh, 820), full-bleed photo, top and bottom vignettes. Nav with the white logo. Bottom row: H2 white headline on the left (max ≈520); on the right, a white body paragraph and CTA row (`.btn--light` + `.btn--glass`) |
| **Hero (centered)** | Same frame with centered content: optional tag, H2 (max ≈760), gap 32, subtitle in light-88, CTA row |
| **Case cards** | Intro (simple), gap 32, 3 × case card (gutter 20) |
| **Journal** | Intro (simple), 4 × news card |
| **Split cards** | Intro (split), 2 × split card |
| **Product cards** | Intro (split), 3 × product card |
| **CTA band** | Photo + vignette, 560 tall (mobile 520), centered tag → H2 → line → CTA row → optional email form |
| **Footer** | Dark (`--neutral-black`/`--dark-100`), brand blurb + 3 link columns (Label Large headers, Body Small links), bottom bar in light-64, a giant faint wordmark (light-8) |

These are the blocks the starter template demonstrates. They are not a default page order: compose each page from `layouts.md`, which adds more hero variants and section patterns. Drop blocks the content doesn't need; never invent content to fill a block.

Responsive: 3- and 4-column grids → 2 columns at ≤1024 → 1 column at ≤767.
