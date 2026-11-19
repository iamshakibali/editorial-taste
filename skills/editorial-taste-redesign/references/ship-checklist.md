# Editorial Taste — Ship Checklist

Run this before reporting work as done. Fix failures, or list them explicitly in the report.

## Style
- [ ] `lint.py` reports 0 errors on every changed style and markup file
- [ ] No accent colors, shadows, bold headings, or non-Geist fonts
- [ ] Spacing and radii on the scale; nested radii follow `inner = outer − gap`
- [ ] Every photo with text on it has a vignette; logo is white on photos and dark on light
- [ ] Only one radius per card row
- [ ] Transitions use `var(--ease)` and animate only `transform`, `opacity`, `color`, and `background-color`
- [ ] `--signal` appears only as the single dot in an isometric illustration

## Motion
- [ ] `html.js` class set in `<head>`; nothing is hidden with JS disabled
- [ ] Reduced motion: no smooth scroll, reveals, parallax, count-up, or pulse; final states shown immediately
- [ ] One hero sequence; sections reveal once; no replay on scroll-up
- [ ] Smooth scroll stops while the drawer is open; anchors land below the nav and move focus
- [ ] 60fps while scrolling with the CPU throttled 4×; no long tasks over 50ms; CLS stays at 0
- [ ] No `transition: all`, no animated `filter`/`box-shadow`, no permanent `will-change`

## Content
- [ ] No `{{placeholders}}` left (`grep -n '{{' *.html`), or the remaining ones are listed in the report as needing input from the user
- [ ] No invented prices, statistics, testimonials, or client logos for a real business
- [ ] No banned filler words (see `copy.md`)
- [ ] Sentence case in headings and buttons; no exclamation marks
- [ ] One primary action per screen; no competing CTAs in the hero

## Interaction and states
- [ ] Hover, active (pressed), focus-visible, and disabled states on every button, link, and control
- [ ] Forms validate on the client (required fields, email format) with inline, specific messages and `aria-live`
- [ ] Data-driven areas have a loading skeleton shaped like the content, a composed empty state, and an inline error state
- [ ] No dead links: every `href="#"` is either wired up or rendered as `aria-disabled="true"`
- [ ] The current page is marked in the nav with `aria-current="page"`
- [ ] The mobile drawer opens, traps nothing unexpectedly, closes on link click, and restores scroll

## Accessibility
- [ ] One `h1` per page, with headings in order
- [ ] Semantic landmarks: `header`, `nav`, `main`, `section` with `aria-labelledby`, `footer`
- [ ] A skip link to `#main`
- [ ] Alt text on every meaningful image (`alt=""` on decorative ones)
- [ ] Photos are on-subject; Unsplash photos use the returned `images.unsplash.com` URLs and are credited in `credits.html`, linked from the footer; all other images are local files; `review/` is deleted
- [ ] Contrast of at least 4.5:1 for body text and 3:1 for large text and UI parts. Check text on photos against the lightest area behind it
- [ ] Touch targets of at least 44×44 on mobile
- [ ] `prefers-reduced-motion` turns off reveals, zooms, and the word-by-word statement
- [ ] State is never shown by color alone

## Ship requirements
- [ ] `<title>`, meta description, canonical, `og:title`, `og:description`, `og:image` (1200×630), and `twitter:card`
- [ ] Favicon (`favicon.svg`) and `theme-color`
- [ ] A branded 404 page (`templates/404.html`)
- [ ] Privacy, Terms, and Cookies links in the footer that go to real pages or are marked as `{{placeholders}}`
- [ ] Cookie consent where the jurisdiction requires it (EU/UK, when using analytics or ads)
- [ ] Images sized and compressed: hero under ~400 KB, `loading="lazy"` below the fold, `fetchpriority="high"` on the hero image
- [ ] Fonts preconnected, with `display=swap`

## SEO and answer engines
- [ ] Index evergreen pages and `noindex` campaign-only or time-limited pages
- [ ] FAQ written as plain questions and answers; add `FAQPage` JSON-LD when the page is indexed
- [ ] Internal links between the homepage and the main sections or pages

## Responsive QA
- [ ] At 1440px: container 1280, margins 40, nothing stretched
- [ ] At 768px: grids at two columns, nav collapsed
- [ ] At 390px: no horizontal scroll, button text stays inside its button, primary action visible in the first screen, and nothing overlaps the vignette text
