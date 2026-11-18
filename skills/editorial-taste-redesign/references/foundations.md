# Editorial Taste — Foundations

## Color

### Neutral scale (`neutral/*`, ALL_SCOPES)
| Token | Hex | Token | Hex |
|---|---|---|---|
| white | #FFFFFF | 600 | #525252 |
| 50 | #FAFAFA | 700 | #404040 |
| 100 | #F5F5F5 | 800 | #262626 |
| 150 | #EDEDED | 850 | #1F1F1F |
| 200 | #E5E5E5 | 900 | #171717 |
| 300 | #D4D4D4 | 950 | #0A0A0A |
| 400 | #A3A3A3 | 975 | #050505 |
| 500 | #737373 | black | #000000 |

### Alpha ramps
Steps: 100 · 88 · 64 · 48 · 32 · 16 · 8 · 4 (%) → hex alpha `FF E0 A3 7A 52 29 14 0A`.

- `base/light-*` = `#EDEDED` + alpha. Use on **dark/photo** backgrounds.
- `base/dark-*` = `#151515` + alpha. Use on **light** backgrounds.

### Semantic
| Token | Value | Role |
|---|---|---|
| background/base | #EDEDED | Page surface |
| background/lift | #D9D9D9 | Elevated surface, button hover |
| tone/strong | #151515 | Primary text/icons, primary button |
| tone/medium | #151515 @64% | Secondary text |
| tone/faint | #151515 @16% | Disabled text, tag fill |
| border/subtle | #151515 @16% | Dividers |

### In-practice usage
| Use | Value |
|---|---|
| Body copy on light | neutral/500 #737373 |
| Card surface | neutral/200 (case cards), neutral/white (news / product cards) |
| Text on photo | #FFFFFF, subtitle light-88 |
| Glass button on photo | light-16 + blur 16 |
| Tag chip | tone/faint + blur 15 |
| Image overlay | linear-gradient black 0% → 90–100% |

## Typography

Families: **Geist Medium** (headings) · **Geist Regular/Medium** (body / body bold) · **Geist Mono Regular** (UI).
Values are given as size / line-height / letter-spacing, in px.

| Style | Canvas desktop | Canvas mobile | **Web desktop** | **Web mobile (≤767)** | Usage |
|---|---|---|---|---|---|
| H0 | 96/88/−3 | 56/60/−1.5 | 72/68/−2.5 | 44/48/−1.5 | Display |
| H1 | 64/60/−2 | 48/60/−2 | 48/48/−1.5 | 36/40/−1.25 | Big numbers |
| H2 | 56/60/−2 | 40/52/−1.5 | 40/44/−1.5 | 30/34/−1 | Hero, intro blocks |
| H3 | 48/52/−1.5 | 32/40/−1 | 32/36/−1 | 26/30/−0.75 | Section titles |
| H4 | 36/40/−1.5 | 24/32/−1 | 24/28/−0.75 | 20/26/−0.5 | Card titles (news, split, product) |
| H5 | 28/32/−1 | 20/20/−1 | 20/24/−0.5 | 18/22/−0.5 | Case card title |
| H6 | 16/20/−0.5 | 12/16/0 | 14/18/−0.25 | 12/16/0 | Small heading |
| Body Large | 20/32/−0.8 | 16/24/−0.8 | 17/26/−0.4 | 15/22 | Lead, stat caption |
| Body Medium | 16/24/0 | 14/20/0 | 15/22 | 14/20 | Paragraphs |
| Body Small | 14/20/0 | 12/16/0 | 13/18 | 12/16 | Meta |
| Button Large (mono) | 14/20/−0.5 | 12/20/−0.5 | 13/18/−0.4 | 12 | Buttons, nav |
| Button Small (mono) | 12/12/0 | 10/12/0 | 11/12 | 10 | Small buttons |
| Label Large (mono) | 12/16/0 | 10/12/0 | 11/14 | 10/12 | Eyebrows, tags |
| Label Small (mono) | 10/12/0 | 8/10/0 | 10/12 | 8/10 | Micro labels |


## Spacing (5px scale)
`5 10 15 20 25 30 35 40 45 50 55 60 65 70 75 80 85 90 95 100`

| Context | Canvas (1920) | Web desktop | Web mobile |
|---|---|---|---|
| Heading → body (title group) | 15 | 15 | 15 |
| Text stack (headline / body / CTA) | 20 | 20 | 20 |
| Button group gap | 15 | 10–15 | 10 |
| Card grid gutter | 25 | 20 | 12 |
| Section title → content | 50 | 32 | 24 |
| Page side margin | 50 | 40 | 20 |
| Section vertical padding | — | 96 | 64 |
| Hero headline → subtitle | 32 | 32 | 24 |
| Highlight Numbers item gap | 200 | fluid grid | stack |

> The compact web scale may use 32 / 56 / 96, which are off the 5-step scale. These are sanctioned exceptions of the compact scale. Anything else must stay on the scale.

## Corner radius
Scale: `0 5 10 15 20 25 30 35 40 45 50`.
| Element | Radius |
|---|---|
| Button (rect) | 8 |
| Nav icon hit area | 4 |
| News, split image, product cards | 10 |
| Case card | 20 |
| Circle button | 50% |
| Tag chip / pill CTA | 9999px |

## Grid and breakpoints
| | Canvas (1920) | Web |
|---|---|---|
| Columns | 12 | 12 |
| Margin | 50 | 40 (20 mobile) |
| Gutter | 25 | 20 (12 mobile) |
| Canvas / container | 1920×1080 → 1820 content | max-width 1280 |
| Mobile breakpoint | mobile frame | `max-width: 767px` |

## Effects
- **No shadows.**
- `backdrop-filter: blur(16px)` on secondary and glass buttons; `blur(15px)` on tag chips.
- Top vignette: ~240px tall, `linear-gradient(0deg, transparent, rgba(0,0,0,.9))`, behind the nav.
- Bottom vignette: ~450–600px tall, `linear-gradient(180deg, transparent, rgba(0,0,0,.98))`, behind hero and card copy.

## Other collections
- `Appearance`: opacity 20–100, step 10.
- `Button Text`: default labels "Primary", "Hover", "Secondary", "Tertiary".
