# Editorial Taste — Copy and Content

The visual system is quiet, so the words carry the page. Write like a good magazine: short, concrete, confident.

## Voice
- **Declarative, not promotional.** State what is true. "Storage that runs for thirty winters." Not "Revolutionary storage solutions!"
- **Concrete nouns and numbers over adjectives.** "Installs in 9 days" beats "fast installation".
- **Sentence case everywhere**: headings, buttons, nav, form labels. Mono eyebrows and tags are uppercase through CSS (`text-transform`), never typed in caps.
- **No exclamation marks, no emoji, no rhetorical questions in headlines.**

## Headlines
| Where | Shape | Example |
|---|---|---|
| Hero (H2) | 3–7 words, ending with a period. Outcome or conviction | "Clean data, built to last." |
| Statement (H0) | 2–4 lines, one idea, the brand's core belief | "We build the quiet infrastructure that keeps a city running when everything else stops." |
| Section title (H3) | 1–3 words, a noun or short phrase | "Product", "Selected work" |
| Card title (H4/H5) | A name or an outcome | "Grid storage", "4 GWh in 11 months" |

Formulas that suit the voice:
- "{Outcome}, {quality}." → "Clean energy, built to last."
- "{Category} for {audience}." → "Field software for rail engineers."
- "{Verb} {object} in {time}." → "Survey a site in one afternoon."

Break long headlines where the thought breaks. `text-wrap: balance` handles most cases; add a manual `<br>` only when a phrase would split awkwardly.

## Eyebrows and labels
Numbered section eyebrows: `01 — Product`, `02 — Selected work`. Tags combine a category and a type with a dot separator: `Energy · Solar`. Keep them to 1–3 words.

## Body
- Hero paragraph: 2–3 sentences. What it is, who it's for, what makes it different.
- Card body: one sentence, 10–20 words.
- Never more than about 70 characters per line (the template caps `max-width`).

## CTAs
- A verb plus what they get: "Book a site visit", "See the platform", "Get the spec sheet". "Explore" is fine on product cards because the card supplies the object.
- **Never use** "Learn more", "Click here", "Submit", or "Get started" on its own.
- **One primary action per screen.** In the hero, pair one light button with at most one glass button.

## Proof
- Put proof right next to the claim it supports: a stat under the hero, a case card beside a capability.
- Stats: 3–4 values that fit in about 5 characters (`22.8%`, `30Y`, `-40°C`, `EPC`). Captions are 2–4 words.

## Content realism
- **Write real copy.** No lorem ipsum and no "Your headline here". The template's `{{placeholders}}` must all be replaced before delivery.
- **Never invent facts for a real business.** Prices, statistics, customer counts, certifications, testimonials, and client logos must come from the user or a real source. If one is missing, leave a clearly marked `{{placeholder}}` and list it in your report.
- **In fictional demos**, make numbers look measured rather than round (`22.8%`, `4,312 homes`, `11 months`). Vary dates across a list. Give people specific names suited to the audience and region. Invent brand names that sound like they belong in the industry.
- **Banned filler:** revolutionize, supercharge, cutting-edge, seamless, effortless, next-level, world-class, game-changing, unlock, empower, harness the power, transform your workflow, elevate. Say what the thing does instead.

## System messages
- Confirmations are calm and specific: "Thanks. You're on the list for {{Brand}} updates."
- Errors say what failed and what to do next: "That email looks incomplete. Check the part after the @."
- Don't use `alert()`. Show messages inline, in Label Large mono, with `aria-live="polite"`.
