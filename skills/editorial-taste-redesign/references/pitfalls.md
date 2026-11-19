# Editorial Taste — Common Pitfalls

These mistakes come up repeatedly when applying the system. Check for each one before you finish.

| # | Pitfall | Do this instead |
|---|---|---|
| 1 | A different mono face (IBM Plex Mono, JetBrains Mono, etc.) on tertiary buttons or labels | Geist Mono (`--font-ui`) everywhere UI text appears |
| 2 | Desktop type sizes shipped to mobile | Use the mobile values in `foundations.md`; the `@media (max-width: 767px)` token overrides handle it |
| 3 | Icon-only buttons drawn as circles with radius 8 and uneven widths | Icon-only buttons are squares with radius 8 at fixed sizes (44 / 28). True circles are only the circle button |
| 4 | Nav links at Button Small size | Nav links use Button Large |
| 5 | Hard-coded near-blacks (#000 or off-palette blacks for text) and radius 240 | Use `--tone-strong` for text and `--radius-pill` for pills |
| 6 | Primary hover flipping to a different dark | Hover on primary/secondary goes to `--bg-lift` #D9D9D9 with dark text. Use neutral-800 only if the user asks for a subtler hover |
| 7 | Multi-line H1 with line-height below font size | Allowed for single-line stats. For multi-line H1/H0, set line-height ≥ font size so descenders don't clip |
| 8 | A pricing/testimonial/logo-wall section styled ad hoc | Build it from existing pieces: news-card surface, Body Medium, Label Large eyebrows, and the same gutter and radius. Logo walls are monochrome (`filter: grayscale(1)` + 64% opacity) |
| 9 | Effects redefined per component | Reuse `--blur-glass`, `--vignette-top`, `--vignette-bottom` |
| 10 | Missing focus, disabled and pressed states | Always add them (see SKILL.md, Accessibility) |
| 11 | Colorful stock illustrations or icons | Photography only; icons are 1.2px line icons in `currentColor` |
| 12 | Title Case, exclamation marks, emoji in headlines | Sentence case, short declarative headlines ending in a period |

## Generic patterns to diagnose and remove
These patterns make a site look template-made or AI-generated. On a redesign, list every one you find in the audit. On a new site, never introduce them.

| Pattern | Replace with |
|---|---|
| Purple, blue, or rainbow gradient backgrounds and blobs | Flat `--bg-base` or a full-bleed photo with a vignette |
| Gradient text on headlines | Solid `--tone-strong`, or white on a photo |
| Everything centered, section after section | Left-aligned editorial layouts. Center only the centered hero and the CTA band |
| Three identical icon + title + text cards | Product, case, or split cards with real photography, or a 5/7 split list |
| Emoji or colorful icon bullets | 1.2px line icons, or none |
| Pill "badge" above every heading ("✨ New") | One numbered mono eyebrow per section ("02 — Selected work") |
| Glassmorphism on light backgrounds | Glass only over photos. On light surfaces use `--dark-8` |
| Soft drop shadows on every card | No shadow. Separate with surface tone (`--neutral-200` vs white) or a hairline |
| Rounded-2xl everything | 8 for buttons, 10 for cards, 20 for case cards |
| Every site gets the template's split hero and the same section order | A layout signature per site: a different hero variant, signature moves, and section patterns from `layouts.md` |
| Inter/Roboto with semibold headings | Geist Medium with negative tracking |
| "Get started", "Learn more" | Verb plus object ("Book a site visit") |
| Filler copy ("seamless", "next-level") | Concrete nouns and numbers (see `copy.md`) |
| Stock illustration of people at laptops | Real photography of the product, place, or work |
| Gray placeholder blocks shipped as final, or random stock URLs pasted in | Unsplash photos picked with `scripts/images.py`, reviewed on the contact sheet, credited to the photographer |
| Fake logo walls and invented testimonials | Real proof from the user, or a marked `{{placeholder}}` |
| Fade-in on every element, bouncy springs, or slide-ins from the side | One reveal per block (rise 32px with expo-out), staggered in reading order (see `motion.md`) |
| Scroll-jacking, section snapping, custom cursors, magnetic buttons | Native scroll smoothed by Lenis; standard cursor |
| Clip-art or 3D-render illustrations, colorful isometric scenes | Isometric hairline drawings from `scripts/iso.py`: white blocks, hairlines, vertex dots, one signal dot |
