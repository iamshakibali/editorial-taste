# Editorial Taste — Framework setup

The source of truth is always the CSS custom properties in `tokens.css`. Frameworks only *reference* them.

## Plain HTML / CSS
Link the Google Fonts stylesheet, then paste `tokens.css` (or the template `styles.css`) as the first stylesheet.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Geist:wght@400;500;700&family=Geist+Mono:wght@400&display=swap" rel="stylesheet">
```
(700 is used only for the logo wordmark.)

## Next.js
Use the `geist` package (`npm i geist`) and map it to the token names:

```tsx
// app/layout.tsx
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import "./tokens.css";
export default function RootLayout({ children }) {
  return <html lang="en" className={`${GeistSans.variable} ${GeistMono.variable}`}><body>{children}</body></html>;
}
```
```css
/* tokens.css (top) */
:root { --font-heading: var(--font-geist-sans); --font-body: var(--font-geist-sans); --font-ui: var(--font-geist-mono); }
```
Port template sections into components (`Nav`, `Hero`, `Stats`, `ProductCard`, `CaseCard`, `SplitCard`, `NewsCard`, `CtaBand`, `Footer`), keeping the same class names or CSS Modules with the same declarations. Use `next/image` with `fill` + `object-fit: cover` for card and hero media.

## Tailwind v4
```css
@import "tailwindcss";
@import "./tokens.css";

@theme {
  --font-sans: var(--font-body);
  --font-mono: var(--font-ui);
  --color-base: var(--bg-base);
  --color-lift: var(--bg-lift);
  --color-strong: var(--tone-strong);
  --color-medium: var(--tone-medium);
  --color-faint: var(--tone-faint);
  --color-muted: var(--text-muted);
  --color-subtle: var(--border-subtle);
  --color-glass: var(--light-16);
  --radius-btn: 8px;
  --radius-card: 10px;
  --radius-case: 20px;
  --spacing: 5px;            /* p-1 = 5px, p-5 = 25px, p-10 = 50px */
  --container-page: 1280px;
}
```
Then: `bg-base text-strong`, `rounded-btn`, `rounded-card`, `font-mono uppercase text-[11px]` for labels, `backdrop-blur-[16px] bg-glass` for glass. Note that `--spacing: 5px` changes the meaning of every spacing utility; on a redesign of a large existing Tailwind codebase, leave the default and use arbitrary values (`gap-[25px]`) or `gap-(--space-25)` instead.

## Tailwind v3
```js
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      fontFamily: { sans: ["var(--font-body)"], mono: ["var(--font-ui)"] },
      colors: {
        base: "var(--bg-base)", lift: "var(--bg-lift)", strong: "var(--tone-strong)",
        medium: "var(--tone-medium)", faint: "var(--tone-faint)", muted: "var(--text-muted)",
        subtle: "var(--border-subtle)", glass: "var(--light-16)",
      },
      borderRadius: { btn: "8px", card: "10px", case: "20px" },
      maxWidth: { page: "1280px" },
      backdropBlur: { glass: "16px" },
    },
  },
};
```
Disable or avoid `shadow-*` utilities; don't use the default chromatic palette.

## Component libraries (shadcn/ui, MUI, Chakra)
Restyle at the theme level instead of per instance:
- shadcn: point `--background`, `--foreground`, `--primary`, `--muted`, `--border`, `--ring`, `--radius` at the Editorial Taste tokens in `globals.css`, and set `--radius: 8px`.
- MUI/Chakra: set the palette to the neutral ramp, typography families to Geist / Geist Mono, `shape.borderRadius: 8`, and `shadows: Array(25).fill("none")`.
