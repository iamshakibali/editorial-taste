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

## Astro (recommended for marketing sites)
Static by default, so it ships almost no JavaScript, has great Core Web Vitals, and reads like the plain-HTML template.
```bash
npm create astro@latest -- --template minimal
npm i lenis @fontsource/geist-sans @fontsource/geist-mono
```
- `src/styles/styles.css` ← the template's `styles.css`; `src/scripts/motion.js` ← `templates/motion.js`; `public/favicon.svg`; `src/pages/404.astro` ← `templates/404.html`.
- `src/layouts/Base.astro` holds `<head>` (meta, OG, the inline `js`-class script) and loads Lenis plus `motion.js` (see `motion.md` → Astro).
- One component per block: `Nav.astro`, `Hero.astro`, `Stats.astro`, `Statement.astro`, `ProductCard.astro`, `CaseCard.astro`, `SplitCard.astro`, `IllustrationSplit.astro`, `NewsCard.astro`, `Faq.astro`, `CtaBand.astro`, `Footer.astro`. Pass content as props or from a content collection (`src/content/`).
- Images: `astro:assets` `<Image>` with `widths` and `sizes`; the hero gets `loading="eager"` and `fetchpriority="high"`.
- Isometric SVGs: save the generator output as `src/components/illustrations/IsoModules.astro` (inline, so it animates).
- Interactivity (drawer, case-card toggle, form) stays in small `<script>` blocks. No UI framework is needed.

## React + Vite
```bash
npm create vite@latest site -- --template react-ts
npm i lenis motion geist
```
Same component split as Astro, written as `.tsx`. Use `ReactLenis` plus Framer Motion variants from `motion.md` instead of `motion.js` (or call `motion.js` once in a root `useEffect`, never both). Import the CSS once in `main.tsx`.

## Vue / Nuxt
Port each block into an SFC and keep the class names. Import the CSS in `app.vue` or `nuxt.config` `css`. Add the `js` class with `useHead({ htmlAttrs: { class: 'js' } })`, and import `motion.js` in `onMounted` in the root layout (client only). Fonts: `@fontsource/geist-sans` and `@fontsource/geist-mono`.

## SvelteKit
Put blocks in `src/lib/components`, CSS in `+layout.svelte`, the `js` class in `app.html` (`<html class="js">` is fine, because SvelteKit always runs JS when hydrated), and `motion.js` in `onMount` in the root layout. Prerender marketing routes (`export const prerender = true`).

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
