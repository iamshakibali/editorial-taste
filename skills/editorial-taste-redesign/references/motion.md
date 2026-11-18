# Editorial Taste — Motion

Motion should feel **buttery**: continuous, weighted, and decelerating, like a heavy page settling into place. It's choreographed, never decorative. If someone notices the animation before the content, it's too much.

## What "buttery" means
1. **Decelerate into place.** Fast at the start, long soft landing (expo-out). Never linear, never the browser's `ease`, never bounce or elastic.
2. **Only the compositor moves.** Animate `transform`, `translate`, `scale`, `opacity`, and `clip-path`. Never `top`/`left`/`width`/`height`/`margin`, `box-shadow`, or `filter` (blur repaints every frame).
3. **One clock.** Smooth scrolling, reveals, and scroll-linked effects all run from `requestAnimationFrame`, `IntersectionObserver`, or CSS scroll timelines. Never use unthrottled scroll handlers or `setInterval`.
4. **Choreography over effects.** Things arrive in reading order with small, consistent staggers. A section is one gesture, not five separate tricks.
5. **Interruptible.** Hover states reverse smoothly midway. Nothing blocks input or scroll.
6. **Optional.** `prefers-reduced-motion: reduce` gets final states immediately, and content is fully visible without JavaScript.

## Tokens
| Token | Value | Use |
|---|---|---|
| `--ease-out` (`--ease`) | `cubic-bezier(.16, 1, .3, 1)` | Default: entrances, reveals, hovers, smooth scroll |
| `--ease-in-out` | `cubic-bezier(.65, 0, .35, 1)` | Between two on-screen states: drawer, mask wipes, accordion |
| `--ease-in` | `cubic-bezier(.7, 0, .84, 0)` | Exits only (page-out, dismiss) |
| `--dur-fast` | 200ms | Color and background on hover |
| `--dur-base` | 450ms | Label roll, FAQ toggle, underline, drawer |
| `--dur-slow` | 800ms | Fades, nav entrance |
| `--dur-xslow` | 1.2s | Rises, word masks, image unmask, image zoom on hover |
| Distance | 32px rise · 112% word mask · 12% hero drift · ±6% parallax | Keep it small; heavy easing does the work |
| Stagger | 40ms per word (cap 600ms) · 80ms per card (cap 400ms) · 120ms per illustration block | Reading order |

Scroll-linked animations (parallax) use `linear` timing on purpose: the scroll position is the easing, and Lenis smooths it.

## The motion set (implemented in `templates/motion.js` + `styles.css`)
| Moment | Behavior |
|---|---|
| **Smooth scroll** | Lenis (`lerp: 0.09`) on wheel and trackpad; native on touch; off under reduced motion. Anchor links glide over 1.4s with expo-out and land below the nav, and focus moves to the target |
| **Hero intro** | Waits up to 1.2s for fonts and the hero image, then the image settles from `scale(1.12)` over 2.4s, headline words rise out of masks (40ms stagger, starting at 150ms), the paragraph and CTAs fade up at 550ms, the nav drops in at 350ms, and the scroll cue fades in at 1s |
| **Section reveal** | `.reveal`: fade and rise 32px (opacity 800ms, rise 1.2s), once. Card grids stagger by 80ms through `data-stagger` |
| **Heading reveal** | `data-reveal="text"`: each word rises from its own mask. Screen readers get the original sentence |
| **Image reveal** | `data-reveal="image"`: the frame unmasks upward (`clip-path`, in-out) while the image settles from `scale(1.18)` |
| **Illustration** | `data-reveal="iso"`: the grid fades in, blocks drop 28px into place from back to front (120ms apart), connectors follow, and the signal ring pulses every 2.4s |
| **Statement** | `data-words`: each word goes from `--dark-16` to `--tone-strong` as it crosses a reading line at 62% of the viewport |
| **Stats** | `data-count`: counts up over 1.6s with expo-out, using tabular numbers with a fixed width so nothing jitters |
| **Parallax** | Hero media drifts 12% over the first viewport; the CTA image drifts ±6%. Uses CSS `animation-timeline` where supported and stays static elsewhere |
| **Nav** | Slides away when scrolling down past 60% of the viewport and returns when scrolling up. Never hides while the drawer is open or the nav has focus |
| **Hover** | Button and nav labels roll up (450ms), arrows nudge 2px, card images zoom to 1.04 over 1.2s, links draw an underline from the left and retract to the right. Fine pointers only |
| **Press** | `translateY(1px)` |
| **Drawer** | Fades in, then its links rise in reading order (60ms steps, about 400ms in total). Smooth scroll pauses while it's open |
| **Page transitions** | Cross-document View Transitions: the old page fades and lifts out (300ms, ease-in), the new page rises in (600ms, ease-out). Browsers without support navigate normally |

## HTML API
```html
<h2 class="h3" data-reveal="text">Section title</h2>
<div class="hero__aside reveal" style="--d: .55s">…</div>     <!-- extra delay -->
<div class="grid grid--3" data-stagger="80"> <article class="reveal">…</article> … </div>
<div class="card-split__media" data-reveal="image"><img …></div>
<figure class="illo" data-reveal="iso"><svg class="iso">…</svg></figure>
<span class="h1 stat__value" data-count>22.8%</span>
<p class="h0 statement__text" data-words>…</p>
```
Required in `<head>`, before any stylesheet is used: `<script>document.documentElement.classList.add('js')</script>`. Every hidden start state is scoped to `html.js` inside `@media (prefers-reduced-motion: no-preference)`.

## Restraint rules
- **One hero sequence per page.** Other sections reveal once and stay put. Never replay animations on scroll-up.
- **Don't animate body text word by word.** Word masks are for headings only, and the statement is the only scroll-scrubbed text.
- **Don't use** scroll-jacking or section snapping, horizontal scroll hijacking, custom cursors and cursor followers, magnetic buttons, typewriter text, marquees of client logos, auto-rotating carousels, confetti, spinning, bouncing, or 3D tilt cards.
- Never delay content by more than about 600ms after it enters the viewport.
- Avoid looping animation except the hero scroll cue and the illustration signal pulse, and keep both subtle.

## Performance budget
- 60fps while scrolling on a mid-range laptop with the CPU throttled 4× in DevTools: no long tasks over 50ms, no layout or paint storms (Rendering → Paint flashing).
- Set `will-change` only during an animation, never permanently.
- Split text once, after `document.fonts.ready`, so word widths don't shift.
- One `IntersectionObserver` per behavior, and unobserve after revealing.
- Images are sized and lazy-loaded below the fold; the hero image uses `fetchpriority="high"`.
- Cumulative Layout Shift stays at 0: animations use transforms, so the layout never moves.

## Accessibility
- `prefers-reduced-motion: reduce` disables Lenis, reveals, masks, parallax, count-up, the label roll, nav hiding, and the signal pulse. The statement shows in full color immediately.
- No JavaScript means nothing is hidden: the start states require `html.js`.
- Word splitting keeps a `.sr-only` copy of the sentence, and the split words are `aria-hidden`.
- Anchor scrolling moves focus to the target section.
- Parallax stays within ±12% to avoid vestibular discomfort.

## Framework recipes

**Astro**: load Lenis and `motion.js` once in the base layout:
```astro
---
// src/layouts/Base.astro
import '../styles/styles.css';
---
<html lang="en">
  <head>
    <script is:inline>document.documentElement.classList.add('js')</script>
  </head>
  <body><slot /></body>
</html>
<script>
  import 'lenis/dist/lenis.css';
  import Lenis from 'lenis';
  window.Lenis = Lenis;
  await import('../scripts/motion.js');
</script>
```
Use either the CSS `@view-transition` rule (multi-page) or Astro's `<ClientRouter />`, not both. With `<ClientRouter />`, re-run the init on `astro:page-load`.

**React / Next.js**: smooth scroll with `lenis/react`, reveals with Framer Motion (`motion`):
```tsx
'use client';
import { ReactLenis } from 'lenis/react';
import { motion, useReducedMotion } from 'motion/react';

export const ease = [0.16, 1, 0.3, 1] as const;          // --ease-out
export const reveal = {
  hidden: { opacity: 0, y: 32 },
  show: (i = 0) => ({ opacity: 1, y: 0, transition: { duration: 1.2, ease, delay: Math.min(i * 0.08, 0.4) } }),
};

export function SmoothScroll({ children }) {
  const reduce = useReducedMotion();
  return reduce ? children : <ReactLenis root options={{ lerp: 0.09 }}>{children}</ReactLenis>;
}

// <motion.article variants={reveal} initial="hidden" whileInView="show" viewport={{ once: true, margin: '0px 0px -12% 0px' }} custom={index} />
```
Word masks: map words to `<span className="tw"><motion.span className="tw__i" initial={{ y: '112%' }} whileInView={{ y: 0 }} transition={{ duration: 1.2, ease, delay: i * 0.04 }} /></span>`, plus an `sr-only` copy of the sentence.

**GSAP**: when the project already uses it:
```js
gsap.defaults({ ease: 'expo.out', duration: 1.2 });
const lenis = new Lenis({ lerp: 0.09, autoRaf: false });
lenis.on('scroll', ScrollTrigger.update);
gsap.ticker.add((t) => lenis.raf(t * 1000));
gsap.ticker.lagSmoothing(0);
```

**Tailwind**: register the curves (`--ease-out` etc.) in `@theme` as `--ease-editorial: cubic-bezier(.16,1,.3,1)` and use `ease-editorial duration-[1200ms]`. Never use `transition-all`.

**Vue / Svelte**: import `motion.js` once in the root layout's mount hook (`onMounted` / `onMount`), after adding the `js` class.
