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
