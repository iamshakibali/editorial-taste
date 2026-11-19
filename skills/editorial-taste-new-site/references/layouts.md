# Editorial Taste: Layouts and composition

The **design system is fixed**: tokens, type voices, the 5px rhythm, radii, glass, vignettes, motion, and the rules in `foundations.md`. The **layout is not**. Every site composes its own page from the patterns below, chosen for its content. The starter template is one worked example of the system, not the layout to reproduce.

Two sites built with this skill should look like they come from the same studio, never like the same page with different words.

## 1. Write a layout signature first
Before any markup, decide and post these five choices as part of the plan:

| Knob | Options |
|---|---|
| **Hero** | One of H1–H8 below |
| **Signature moves** | Two patterns that define this site (e.g. index list + sticky split, mosaic + quote band) |
| **Surface rhythm** | How sections alternate between `--bg-base`, white (`--neutral-white`), and dark (`--neutral-black`) |
| **Image density** | Photo-led (full-bleed, large crops) · balanced · type-led (few images, big type, hairlines, illustrations) |
| **Grid rhythm** | The sequence of column structures down the page, e.g. full → 12 → 5/7 → 4-up → 7/5 → full |

Choose from the brand and the content, not from habit:
- Strong photography → photo-led, H1/H2/H5/H7.
- Few or no photos, a sharp idea → type-led, H3/H6, illustrations and hairline lists.
- One product or offer → H4/H8 with the action in the first view.
- Many offers or audiences → H6 index hero or a mosaic.

## 2. What never varies
Layouts vary. These rules from `SKILL.md` and `foundations.md` don't, in any pattern, new or old:
- **Type roles.** The hero headline is always `.h2` (the page's `h1`). `.h0` is used only by the one statement. Section titles `.h3`, card titles `.h4`/`.h5`, stat values and prices `.h1`, quotes `.h2`.
- **Statement.** One per page, 2 to 4 lines, `data-words`. Never directly under the hero: at least one section (stats, proof, or content) sits between them. Never the hero itself.
- **Radii.** Buttons 8, cards 10, **case cards 20 and nothing else**, chips and pills full, nav icons 4. Photos, mosaics, inset hero frames, image bands, form panels, plan highlights, and illustration panels all use 10 (or 0 when full-bleed).
- **Spacing.** Only `--space-*` tokens and the sanctioned compact values (8, 12, 32, 56, 96). Section padding `--section-pad`, title to content `--section-gap`, gutters `--grid-gutter`.
- **Color, depth, type voices, motion.** Neutral ramps only, glass instead of shadows, vignettes only behind text on photos, Geist Medium and Regular, Geist Mono for UI labels, the shared motion attributes and tokens.

If a pattern seems to need a break from these, change the pattern, not the rule.

## 3. Variation rules
1. **Never reproduce the template composition.** Don't ship the template's section sequence (split hero → stats → statement → 3 product cards → 3 case cards → 2 split cards → illustration → 4 news → FAQ → CTA band) unchanged, even with new copy.
2. **No default hero.** H1 (the template hero) is one option of eight. If a site already exists in the repo or the conversation, pick a different hero and different signature moves than that site used.
3. **At least half the sections** use a pattern or variant that the template doesn't show.
4. **Adjacent sections differ** in column structure and surface. Never two 3-up card rows in a row.
5. **One or two full-bleed moments per page**, not more. Center only a centered hero, a quote, and a CTA.
6. **Order follows the argument**, not a list: hook → proof → how → offer → objections → action. Sections the content can't support are left out.
7. **New patterns are allowed** when built only from the system: tokens, the type scale, hairlines, glass, vignettes, the radius rules, and the motion API. Name them with BEM classes beside the template's.

## 4. Hero variants
All heroes: one `h1` set in `.h2`, one primary action plus at most one secondary, `data-reveal="text"` on the headline, one intro sequence.

| | Hero | Recipe |
|---|---|---|
| H1 | **Split bottom** (template) | Full-bleed photo, top and bottom vignettes, H2 bottom left, paragraph and CTAs bottom right |
| H2 | **Centered** | Full-bleed photo, vignette, centered tag → H2 (max 760) → light-88 subtitle → CTA row |
| H3 | **Type first** | Type first, photo second. `--bg-base`, a mono eyebrow, the `.h2` headline across 7 of 12 columns with generous space around it, then a hairline row with the paragraph (5 cols) and CTAs (aligned end). Below, a full-width photo band (`aspect-ratio: 21/9`, radius 0 full-bleed or 10 inset) that unmasks with `data-reveal="image"` |
| H4 | **Split screen** | 100svh, two columns 1:1 (or 5/7). Text side on `--bg-base`: eyebrow, H2, paragraph, CTAs, pinned to the bottom with a stat row. Image side full height, no radius, no vignette (no text on it) |
| H5 | **Inset frame** | Photo inside the container with `border-radius: var(--radius-10)`, ~85svh, 20px from the nav. Headline top left on a top vignette, a glass panel bottom right (`--light-16` + blur) holding paragraph and CTAs |
| H6 | **Index** | 5/7 grid on `--bg-base`. Left: eyebrow, H2, paragraph, CTA. Right: a numbered list of offers in H4 with hairline dividers and mono numbers; hovering a row swaps a small preview image (opacity and clip-path only) |
| H7 | **Mosaic** | Headline row (H2 left, paragraph and CTA right) over a 12-col image grid: one large image (7 cols, tall) and two stacked (5 cols). Radii 10, gutter 20. Images unmask in sequence with `data-stagger` |
| H8 | **Dark product** | `--neutral-black` surface, nav on dark. Centered or left H2 in white, light-64 paragraph, CTAs, and below them a single product photo or isometric illustration on a glass plate. The rest of the page returns to light |

## 5. Section patterns by job
Pick the pattern that fits the content. The **(T)** mark means the template shows it.

**Proof (numbers)**
- Stat row, centered, 4 items (T).
- Stat bar inside the hero bottom edge, left aligned, separated by vertical hairlines.
- Big number: one `.h1` figure in 5 cols with its caption, a list of three supporting facts in 7 cols.
- Dark band: stats in white on `--neutral-black`, left aligned, labels in mono.

**Proof (people and clients)**
- Quote band: one testimonial in `.h2` (no quote cards, no carousels), mono name and role beneath, optional small portrait radius full. Center or 2/10 offset.
- Logo wall: monochrome logos (`currentColor`, `--tone-medium`) in a 6-col grid with hairline cell borders.
- Case list: rows of client · project · year · result in a table-like grid with hairlines, H5 names, hover reveals an image.

**Offer (products, services)**
- Product cards 3-up (T).
- Feature + list: one large card spanning 7 cols beside 5 cols of two stacked cards.
- Index rows: numbered rows (mono number · H3 name · body muted · arrow), full width, hairline dividers, row hover moves to `--bg-lift`.
- 2×2 tiles on white with an isometric drawing or photo each, radius 10.
- Pricing: 2 or 3 plan columns separated by hairlines (not boxed cards), plan name in mono, price in `.h1`, list of inclusions, one Primary button per column, the recommended plan on `--bg-lift`.

**Work**
- Case cards 3-up, expandable (T).
- Lead case: one large case card (r20, it is a case card) with vignette and overlay text, then two smaller case cards 1:1.
- Rail: horizontal scroll-snap row of case cards (`scroll-snap-type: x mandatory`, gutter 20, a peek of the next card, arrow buttons, keyboard scrollable).
- Alternating: image 7 cols and text 5, then reversed, three times at most.

**Approach (how it works)**
- Split cards 2-up (T).
- Illustration split 5/7 with steps (T).
- Sticky split: title, paragraph, and CTA in 4 cols `position: sticky; top: 96px`; steps or features scroll in 8 cols, each separated by a hairline, each step's mono number in a fixed column.
- Timeline: horizontal row of 4–5 steps on a single hairline, mono numbers on the line, H5 + body below.

**Story and brand**
- Statement, word by word (T). One per page, never directly under the hero.
- Image + caption: a single wide photo (radius 10) (`data-reveal="image"`) with a mono caption and a short paragraph offset to 7/12.
- Team grid: 4-up portraits (radius 10, aspect 4/5), H6 name, muted role in mono.

**Journal**
- 4 news cards (T).
- List: rows with date (mono, 2 cols), headline (H4, 7 cols), topic tag (3 cols), hairline dividers.
- Feature + two: one large article with image (7 cols) beside two text-only news cards stacked.

**Objections**
- FAQ 5/7 (T).
- FAQ single column, centered within 8 cols, title above.
- FAQ two columns of `<details>` under a full-width title.

**Action**
- Full-bleed CTA band with photo (T).
- Split CTA: H2 and line on the left, a form on a `--bg-lift` panel (radius 10) on the right.
- Type CTA: dark band, a `.h2` line across 8 columns, a hairline, then the supporting line and a light button. No photo.
- Contact sheet: address, email, hours in mono columns with a map-free studio photo.

**Footer**
- Dark with giant wordmark (T).
- Light minimal: one row of logo, links, legal on `--bg-base` with a top hairline.
- Dark with a final subscribe form and a 4-col sitemap.

## 6. Recipes for patterns not in the template
Reuse tokens only. Keep the template's motion attributes: `.reveal`, `data-stagger`, `data-reveal="text|image|iso"`, `data-count`, `data-words`.

```css
/* Index rows (H6 list, offer rows, case list) */
.index { border-top: 1px solid var(--border-subtle); }
.index__row { display: grid; grid-template-columns: 64px minmax(0,1fr) minmax(0,420px) 24px; gap: var(--space-20); align-items: center;
  padding-block: var(--space-25); border-bottom: 1px solid var(--border-subtle); transition: background var(--dur-fast) var(--ease-out); }
.index__row:hover { background: var(--bg-lift); }
.index__num { font: 400 var(--label-lg-size)/var(--label-lg-lh) var(--font-ui); color: var(--text-muted); }

/* Sticky split */
.sticky-split { display: grid; grid-template-columns: 4fr 8fr; gap: var(--space-75); }
.sticky-split__aside { position: sticky; top: 96px; align-self: start; }

/* Mosaic */
.mosaic { display: grid; grid-template-columns: 7fr 5fr; grid-template-rows: repeat(2, minmax(0, 1fr)); gap: var(--grid-gutter); height: min(80svh, 760px); }
.mosaic > :first-child { grid-row: span 2; }
.mosaic img { width: 100%; height: 100%; object-fit: cover; border-radius: var(--radius-10); }

/* Rail */
.rail { display: grid; grid-auto-flow: column; grid-auto-columns: minmax(300px, 32%); gap: var(--grid-gutter);
  overflow-x: auto; scroll-snap-type: x mandatory; overscroll-behavior-x: contain; }
.rail > * { scroll-snap-align: start; }

/* Quote band */
.quote { max-width: 960px; margin-inline: auto; text-align: center; }
.quote blockquote { font: 500 var(--h2-size)/var(--h2-lh) var(--font-heading); letter-spacing: var(--h2-ls); }

/* Dark surface section */
.section--dark { background: var(--neutral-black); color: var(--neutral-white); }
.section--dark .muted { color: var(--light-64); }
```

Every new pattern collapses cleanly: multi-column grids → 1 column at ≤767 (sticky becomes static, rails keep scrolling), 12-col splits → stacked at ≤1024. Check it at 1440, 768, and 390 like the rest.

## 7. Example compositions
These are examples of range, not menus to copy.

- **Architecture studio, photo-led**: H5 inset frame → stat bar → statement → lead case + 2 → sticky split approach → quote band → team grid → journal list → split CTA → light footer.
- **SaaS product, type-led**: H3 type-first hero with product band → logo wall → index rows of features → illustration split → pricing → FAQ two columns → type CTA → dark footer.
- **Consumer brand, one product**: H4 split screen → big number proof → alternating features → quote band → FAQ single column → full-bleed CTA band → dark footer.
- **Energy company, many audiences**: H6 index hero → dark stat band → feature + list offers → statement → timeline → journal feature + two → FAQ 5/7 → CTA band → dark footer.
