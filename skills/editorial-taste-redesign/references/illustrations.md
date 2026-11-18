# Editorial Taste — Isometric hairline illustrations

Photography carries the brand. **Isometric hairline illustrations** explain what photos can't: a system, a platform, a process, modules, layers, a flow. They're technical drawings, not decoration. Think product spec sheet, not marketing clip art.

## When to use one
- **Do:** a "How it works", platform, architecture, or modules section; steps of a process; a product that is software or invisible infrastructure; an empty state; a feature with no honest photo.
- **Use 1–3 per page**, each in its own section, alternating with photo sections.
- **Don't** use one in the hero when a real photo exists, as decoration beside body text, or to replace photography of real places, products, and people.

## Visual rules
| Element | Rule |
|---|---|
| Projection | True isometric, 30°. x runs down-right, y down-left, z up. No perspective and no other angles |
| Grid | Ground grid of 0.75px `--neutral-300` hairlines, one line per unit (40px), faded radially to the edges |
| Objects | Simple blocks: slabs, modules, stacked layers. 3–6 objects per illustration, with generous negative space |
| Faces | Top `--neutral-white`, left `--neutral-100`, right `--neutral-200`. Flat fills: no gradients, no shadows, no textures |
| Edges | 1px `--neutral-400` hairlines that stay 1px at any size (`vector-effect: non-scaling-stroke`) |
| Active object | One at most: edges `--tone-strong`, top `--neutral-100` |
| Vertex dots | 2px `--tone-strong` dots inset at the top-face corners. They're the signature detail, so always include them |
| Labels | Geist Mono 11px, uppercase, letter-spacing 1.6px, `--neutral-700`, lying on the left face in perspective. Use short nouns plus a number: `MODULE #1`, `LAYER 02 · CONTROL`, `STEP 03` |
| Status LEDs | 2–6 small `--neutral-300` dots under a label (`--neutral-500` on the active object) |
| Connectors | 1px dashed `--neutral-500` hairlines (3 4 dash) on the ground or between stacked layers |
| **Signal** | The **only** color in the system: one `--signal` #FF4D2E dot on the active object, with a dashed ring and a slow pulse. At most one per illustration, and never used outside illustrations |
| Frame | Sits on a `--bg-base` panel, radius 10, full width of its column, aspect about 4:3 to 3:2 |

## Generate with `scripts/iso.py`
```bash
python3 <skill-dir>/scripts/iso.py --list                       # modules · stack · flow · single
python3 <skill-dir>/scripts/iso.py --preset modules > modules.svg
python3 <skill-dir>/scripts/iso.py --preset stack --spec > my.json   # start from a preset
python3 <skill-dir>/scripts/iso.py my.json > my.svg
```
Spec format:
```json
{
  "id": "iso-platform",
  "title": "Three platform layers, software active",
  "unit": 40,
  "aspect": 1.25,
  "blocks": [
    {"x": 0, "y": 0, "z": 0,   "w": 6, "d": 6, "h": 0.7, "label": "Layer 01 · Hardware", "leds": 6},
    {"x": 0, "y": 0, "z": 1.6, "w": 6, "d": 6, "h": 0.7, "label": "Layer 02 · Software", "active": true, "signal": true}
  ],
  "paths": [{"points": [[0, 6, 0.7], [0, 6, 1.6]], "dashed": true}]
}
```
- Units are grid cells. Keep blocks side by side on the ground with gaps of at least 0.5 units, or stack them exactly. Overlapping footprints at different heights won't sort correctly.
- `h` ≥ 0.9 fits a label plus LEDs; 0.5–0.8 fits a label only.
- Make `id` unique per page, because it prefixes the internal mask ids.
- Write `title` as the accessible description of what the drawing shows.

## Composition recipes
| Idea | Layout |
|---|---|
| **Modules** (a product made of parts, team pods, regions) | 2×2 blocks, 4×4×1.1, gap 0.6, one active with a signal |
| **Stack** (platform layers, architecture) | 3 slabs of 6×6×0.7, stacked 1.6 apart, dashed vertical connectors at the corners, the top or relevant layer active |
| **Flow** (process, pipeline, onboarding) | 3 blocks in a row along x, 3×3, gap 2, dashed ground connectors, the final step taller and active |
| **Single unit** (one device or product) | One 5×5×1.6 block, active, with a signal and 6 LEDs |
| **Grid of many** (scale, fleet, sites) | 3×3 small 2×2×0.6 blocks with 0.5 gaps, no labels except one active block |

## Placing it in a page
```html
<section class="section" aria-labelledby="how-title">
  <div class="container illo-split">
    <div class="illo-split__text reveal"> eyebrow · H3 · body · numbered steps </div>
    <figure class="illo" data-reveal="iso"> <!-- paste the generated <svg class="iso"> inline --> </figure>
  </div>
</section>
```
- **Inline the SVG** to get the build-in animation (`data-reveal="iso"`: grid fades, blocks drop in from back to front, connectors follow, signal pulses). Used as an `<img>`, it renders statically with the pulse only.
- Pair it with a numbered list whose items match the labels in the drawing (`01` ↔ `MODULE #1`).
- In frameworks, save the SVG as a component (`IsoModules.astro`, `IsoModules.tsx`) and keep the `class` names. In JSX, convert `class` to `className` and `stroke-width` to `strokeWidth`, or import the file with SVGR.

## Hand-authoring and Figma
If the generator can't express the idea, draw it by hand with the same rules:
- **SVG math:** a point (x, y, z) maps to screen `((x − y) · cos30° · u, (x + y) · 0.5 · u − z · u)`. A circle of radius r on a top face becomes an ellipse with `rx = √2 · r · cos30° · u` and `ry = √2 · r · 0.5 · u`.
- **Text on the left face:** `transform="matrix(0.866 0.5 0 1 ox oy)"`.
- **Figma:** draw the plan view at 1×, then rotate 45°, scale height to 57.735%, and extrude the side faces. Keep strokes at 1px inside and turn on "Scale strokes: off". Build each block as a component (`Iso/Block` with properties for Active, Signal, LED count, and Label).

## Don't
Shading gradients, drop shadows, perspective or 2.5D angles other than isometric, colored blocks, multiple signal colors, icons pasted onto faces, people or characters, or more than one active object.
