# Editorial Taste — Working in Figma

Use this when the target is a Figma file rather than code. Load the official Figma skills first (`figma-use` before any `use_figma` call; `figma-generate-design` for screens; `figma-generate-library` for tokens and components). This file adds only the Editorial Taste rules.

## Workflow
1. **Inspect the file first.** List variable collections, text styles, and components, and reuse whatever already exists.
2. **Set up foundations if they're missing**, before any screen:
   - `Colors`: one mode. `neutral/*`, `base/light-*` and `base/dark-*` (alpha stored in the variable), and the semantic `background/base`, `background/lift`, `tone/strong`, `tone/medium`, `tone/faint`, `border/subtle`. Semantic tokens alias base and neutral tokens.
   - `Typography`: two modes, **Desktop** and **Mobile**, holding the size, line-height, and letter-spacing for every style in `foundations.md`. Apply the Mobile mode to mobile frames, or the mobile text styles will show desktop values.
   - `Spacing`: `spacing/5` … `spacing/100`.
   - `Corner Radius`: `radius/0` … `radius/50`.
   - `Grid`: columns 12, margin 50, gutter 25, plus a `12 Column Grid` style bound to them.
   - Effect styles: `Glass/Blur 16`, `Glass/Blur 15`, `Vignette/Top`, `Vignette/Bottom`.
3. **Scope every variable**: color → `FRAME_FILL`, `SHAPE_FILL`, `TEXT_FILL`, `STROKE_COLOR`; type → `FONT_SIZE`, `LINE_HEIGHT`, `LETTER_SPACING`; spacing → `GAP`; radius → `CORNER_RADIUS`. Never leave `ALL_SCOPES`.
4. **Text styles**: `Heading/{Desktop|Mobile}/H0–H6`, `Body/{Desktop|Mobile}/{Large|Medium|Small}[ Bold]`, `UI/{Desktop|Mobile}/{Button|Label} {Large|Small}`, each bound to the Typography variables. UI styles use Geist Mono Regular.
5. **Foundations frame**: on a `Foundations` page, show every color swatch, spacing bar, radius sample, and text style, with each sample bound to its variable so the frame updates when a token changes.
6. **Build section by section** on a 1920×1080 canvas. Take a screenshot after each section and fix problems before moving on.
7. **Bind, don't type.** Every fill, stroke, radius, padding, and gap is bound to a variable, and every text layer uses a text style. Use auto layout on every frame that has children.

## Components
- **Button**: one component set with `Style` (Primary · Secondary · Tertiary), `Size` (Large · Small), `Icon` (None · Left · Right), and `State` (Default · Hover · Pressed · Focus · Disabled). Expose the label as a text property. Focus adds a 2px outside stroke in `tone/strong`.
- **Circle button**: `Value` = Default · Active.
- **Logo**: `Mode` = Dark · White.
- **Cards**: case, news, split, and product cards as components with text and image properties.
- Layer names are meaningful (`Section / Product / Card / Solar`). Never leave `Frame 427` or `Group 3`, and avoid typos like "Platfrom" or "Tilte". Variant properties have real names (`Alignment`, not `Property 1`).

## Prototype motion
Smart Animate with a custom bezier of `0.2, 0.7, 0.2, 1`: 400ms for movement and 200ms for color or opacity. Don't use Figma's default ease or linear presets.

## Checklist
- [ ] All tokens exist and are scoped, and Typography has Desktop and Mobile modes
- [ ] Every text layer uses a style; mono only on UI styles
- [ ] Every fill, stroke, radius, padding, and gap is bound
- [ ] No drop shadows; glass and vignettes come from effect styles
- [ ] Buttons have every state, including Focus and Disabled
- [ ] Mobile frames have the Mobile variable mode applied
- [ ] No unnamed layers and no placeholder copy
