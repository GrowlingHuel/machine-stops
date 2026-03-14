# THE MACHINE STOPS — Complete Image Prompts

## Overview

20 images total across 7 clusters. Each cluster shares a base composition;
variants alter one or two elements. Generate clusters together in a single
session — consistency within a cluster matters more than perfection in any
single image.

Existing images (10): marked ✓
New images needed (10): marked ★
Code changes required for new images: documented per image.

---

## STYLE FOUNDATION

Prepend this block verbatim to every prompt:

> Art Nouveau architectural illustration, warm amber and deep ochre palette,
> light emanates from surfaces themselves with no visible external source,
> speculative engineering aesthetic, 1909 imagining the far future, organic
> botanical motifs integrated into mechanical forms, sinuous decorative line
> work, flat colour areas with fine hatching, square format, no text or
> lettering, muted warm ivory ground

**Style ancestry:** Alphonse Mucha's architectural studies crossed with
Scientific American cross-section illustrations, c.1905. Beautiful. Complete.
Wrong in ways that feel inevitable rather than mistaken.

**Generation notes:**
- If results are too photorealistic: add *woodblock print quality, flat planes
  of colour, visible pen line work, not photographic*
- If too decorative and insufficiently architectural: add *architectural
  cross-section diagram, technical illustration, more geometric than organic*
- Always specify *no text, no lettering* — Gemini will otherwise hallucinate
  captions into architectural drawings
- All images square, minimum 1024×1024
- File destination: `~/Projects/machine_stops/images/`

---

## CLUSTER 1 — THE CELL

*Four variants of the same hexagonal room. The geometry never changes.
The light does. Generate all four in one session; compare as a sequence
before finalising any.*

**Base composition:** Hexagonal room, all six padded walls in perspective,
one thousand small apertures in the padding as a repeating botanical motif,
an oval speaking plate on the near wall with Art Nouveau leaf-and-filament
surround, a reading desk at centre with an elaborately bound book, a low
armchair with organic curved legs. No windows. No exterior implied. Deeply
interior.

---

### ✓ `cell_normal.jpg`

**Used in scenes:** `vashti_cell`, `decision_travel`

> [STYLE FOUNDATION] — Interior of a hexagonal room, all six padded walls
> visible in perspective, amber light distributed with perfect evenness from
> the walls themselves casting no shadows, one thousand small apertures in the
> padding admitting regulated light arranged as a repeating botanical motif of
> stylised tendrils, an oval speaking plate on the near wall glowing steady
> warm amber with an Art Nouveau surround of leaves and filaments, a reading
> desk at centre with an elaborately bound book, a low armchair with organic
> curved legs, the geometry perfect and complete, warm ivory and ochre tones,
> everything in its correct place, the room suggesting total adequacy and
> total enclosure, no exterior implied

**Mood:** Adequate. Complete. The most comfortable room in which nothing
has ever happened.

---

### ✓ `cell_restless.jpg`

**Used in scenes:** `preparing_travel`, `vashti_cell_return`

> [STYLE FOUNDATION] — Interior of the same hexagonal room, same architecture
> as cell_normal but with a quality of recent disturbance: the armchair pushed
> slightly off-centre from its usual position, the book resting on the armchair
> seat rather than the desk, the speaking plate's amber glow slightly uneven —
> brighter on one side of its decorative surround — the padded walls their usual
> ivory but one panel's botanical tendrils seem to reach fractionally further
> than the others, the hexagonal geometry still perfect but no longer quite
> sufficient, warm tones unchanged but a slightly cooler undertone entering the
> peripheral shadows, still beautiful, still complete, but recently noticed

**Mood:** Home, but looked at for the first time.

---

### ✓ `cell_flickering.jpg`

**Used in scenes:** `weeks_passing`

> [STYLE FOUNDATION] — Interior of the same hexagonal room, the amber
> light is wrong: two of the six walls emit light at a slightly different
> temperature — cooler, more grey than amber — creating faint directional
> shadows that should not exist in a room where light has no direction, the
> botanical aperture motifs in the affected walls appear slightly asymmetric as
> though the pattern has lost confidence in itself, the speaking plate's glow
> unsteady — its Art Nouveau surround catching the cooler light and looking
> different for it — the book on the desk casting a faint shadow for the first
> time, the armchair unchanged but the light that should celebrate it does not,
> the room still beautiful but listening for something, predominantly amber with
> two cooler grey-ochre intrusions

**Mood:** The same room. Not the same room.

---

### ✓ `cell_dark.jpg`

**Used in scenes:** `machine_stops`

> [STYLE FOUNDATION] — Interior of the same hexagonal room in near-total
> darkness, the hexagonal geometry implied rather than shown — near-black shapes
> against a slightly less black ground — the speaking plate a dark oval, the
> armchair a darker mass within the dark, the botanical motifs in the padded
> walls invisible but their shapes present as the architecture of shadow, the
> book on the desk a pale rectangular suggestion, the room's perfect proportions
> still present as structure but no longer as experience, deep charcoal and
> near-black throughout with only the faintest warm amber undertone remaining —
> not light, but the memory of light that the room is trying to hold

**Mood:** The room remains. Only the room remains.

**Generation note:** Near-total darkness risks becoming illegible. Aim for
*architecture implied by shadow* rather than genuine black. The hexagonal
geometry should remain just readable — six walls, the desk, the chair —
as ghost shapes.

---

## CLUSTER 2 — THE AIRSHIP

*Three variants of the same berth. The blind is the variable. Generate all
three together — the contrast between amber interior and cold exterior is
the whole point of the cluster.*

**Base composition:** A small, well-appointed sleeping berth inside an airship.
Walls of warm pale timber with Art Nouveau inlay of botanical motifs in brass
and ivory. A rectangular porthole blind on the left wall. A narrow berth with
precise geometric bedding. A small reading surface. Amber light from concealed
wall sources. Another berth barely visible through a latticed partition.

---

### ✓ `airship_peaceful.jpg`

**Used in scenes:** `airship_cabin` (default), `departure` (default)

> [STYLE FOUNDATION] — Interior of an airship sleeping berth, walls of warm
> pale timber with Art Nouveau botanical inlay in brass and ivory, a circular
> porthole on the left wall covered by a heavy curtain drawn fully across it
> and gathered to one side on a brass rail — the curtain is thick amber-coloured
> fabric, hanging straight, completely obscuring the porthole, no light entering
> from outside, the curtain is a side-drawn drape NOT a Roman blind NOT a
> roller blind NOT a venetian blind — it hangs from a rail and can be drawn
> aside, a narrow berth with precise geometric bedding, a small reading surface
> with an elaborately bound book, amber light from concealed sources in the
> walls, claustrophobic in the most comfortable sense — everything in its
> correct place, another berth just visible through a latticed partition
> suggesting other passengers, no exterior present or implied

**Mood:** Small and complete and deliberately not looking.

---

### ✓ `airship_blind.jpg`

**Used in scenes:** `airship_cabin` (blind opened, day)

**Code trigger:** `__IMAGE:airship_blind.jpg` in `open.blind` and `use.blind`
actions within `airship_cabin`

> [STYLE FOUNDATION] — Interior of an airship sleeping berth, the rectangular
> blind drawn fully to one side on its runner, a circular porthole open to the
> outside world, through the porthole: vast cold grey-blue sky above and the
> surface of the earth visible at an incomprehensible distance below — not
> realistic photography but a stylised Art Nouveau rendering of altitude itself,
> the earth's surface as abstract organic texture in browns, greens, and ochres,
> the interior amber wall-light meeting the cold exterior light at the porthole
> edge in a precise border that is neither quality, the cabin's warm botanical
> decoration reaching its absolute limit at the glass, the blind gathered to
> one side like a curtain, the scale of the outside world entirely wrong against
> the scale of the berth

**Mood:** The vocabulary of the Machine has no word for this.

---

### ★ `airship_night.jpg`

**Used in scenes:** `departure` (blind opened at night)

**Code change required:** In `departure` scene, `open.blind` action, change
`__IMAGE:airship_blind.jpg` to `__IMAGE:airship_night.jpg`

> [STYLE FOUNDATION] — Interior of an airship sleeping berth, the rectangular
> blind drawn fully to one side, a circular porthole open to a night exterior,
> through the porthole: absolute darkness broken only by the faintest suggestion
> of stars as botanical points of light in deep indigo — rendered in the same
> Art Nouveau decorative language as the machine's apertures but vast and
> unmanaged — and the surface of the earth below completely invisible in the
> dark, the interior amber light spills slightly into the porthole frame but
> cannot penetrate the exterior darkness, the contrast between the warm
> inhabited amber of the cabin and the absolute cold darkness outside is the
> whole composition, the blind gathered to one side

**Mood:** The darkness outside the porthole is a different darkness to the
darkness of the cabin.

---

## CLUSTER 3 — THE CORRIDOR

*Three states of the same tube. Functional, failing, failed.*

**Base composition:** A long tubular corridor, padded walls with repeating
Art Nouveau botanical fern-and-tendril motifs, ceiling and floor curving to
meet the walls, amber distributed light, perspective to a vanishing point.

---

### ✓ `corridor.jpg`

**Used in scenes:** `corridor`

> [STYLE FOUNDATION] — Interior perspective of a long tubular corridor,
> walls padded with a repeating Art Nouveau botanical pattern of stylised
> ferns and tendrils in warm ivory and amber, ceiling and floor curving
> seamlessly into the walls forming a continuous tube, amber light distributed
> without direction from the walls themselves, two or three figures at distance
> as dark silhouettes only — no faces, no individual detail — each maintaining
> careful personal space, the corridor extending to a vanishing point of
> slightly brighter amber suggesting a platform ahead, a quality of regulated
> movement, the air itself suggested by gentle atmospheric perspective

**Mood:** Movement without acknowledgement. Human warmth, mediated by distance.

---

### ★ `corridor_failing.jpg`

**Used in scenes:** Could be applied via `__IMAGE:` in `weeks_passing`
when player goes into corridor (`noticed_corridor_air` path)

**Code change required:** In `weeks_passing` scene, `go.corridor` and
`go.outside` actions, prefix the existing text with
`__IMAGE:corridor_failing.jpg|` so the image swaps when Vashti steps out.
Swap back on any transition back to cell.

> [STYLE FOUNDATION] — Interior perspective of the same tubular corridor,
> same botanical padded walls and curved geometry, but the amber light is
> uneven: sections of wall fully lit, sections dimmer — the botanical motifs
> in the dimmer sections losing colour and definition — creating pools of
> shadow that should not exist in this space, one figure visible at middle
> distance standing still rather than moving, facing the wall with one hand
> pressed flat against the padding, two other figures moving at normal pace
> further along, the vanishing point ahead darker than it should be, the
> corridor still recognisably itself but the confidence has left the light,
> predominantly amber with grey intrusions

**Mood:** The corridor performs. Mostly.

---

### ✓ `corridor_dark.jpg`

**Used in scenes:** `corridor_dark`, `corridor_fork`, `find_kuno`,
`reunion`, `witnessed_approach`

> [STYLE FOUNDATION] — Interior of the same tubular corridor in near-failure,
> the amber wall-light replaced by a cold residual phosphorescence remaining
> only in patches, the botanical motifs half-visible and half-lost to shadow,
> multiple seated figures visible against the walls as dark shapes — some
> with heads bowed, some entirely still — an open elaborately bound book on
> the floor in the foreground its pages the brightest white in the image,
> the corridor perspective still visible but its vanishing point ending in
> darkness rather than light, above the main corridor a darker opening
> suggests a shaft upward, the palette moving from amber to grey-blue, the
> Art Nouveau decoration functioning now as elegy

**Mood:** Something enormous is ending. The architecture remains.

---

## CLUSTER 4 — KUNO'S CELL

*Three states of the same room as Vashti's, distinguished only by what
Kuno is doing in it and what has been revealed.*

**Base composition:** A hexagonal cell architecturally identical to Vashti's —
same padded walls, same aperture motifs, same speaking plate, same reading
desk and book, same armchair geometry. The difference is always Kuno.

---

### ✓ `kuno_cell.jpg`

**Used in scenes:** `kuno_cell`

> [STYLE FOUNDATION] — Interior of a hexagonal cell architecturally identical
> to any other cell — same padded walls with botanical aperture motifs, same
> oval amber speaking plate with Art Nouveau surround, same reading desk and
> elaborately bound book, same armchair — but at the centre of the floor stands
> a single male figure, seen from slightly behind or in three-quarter profile,
> hands resting at his sides without occupation, standing in the centre of the
> room rather than at its periphery, the figure's scale making the room's
> dimensions newly legible as a space with a person in it rather than a
> perfectly adequate provision, the amber light falling on him differently
> than it falls on furniture, warm ivory and amber tones, the figure slightly
> darker than the room around him

**Mood:** The room is the same room. He is not the same as the room.

---

### ★ `kuno_cell_conversation.jpg`

**Used in scenes:** `kuno_tells`, `kuno_detail`, `kuno_why_surface` (all
passage-only scenes that inherit kuno_cell.jpg currently)

**Code change required:** In `kuno_tells` scene, add `__IMAGE:
kuno_cell_conversation.jpg` as part of `on_enter` (prepend as a sentinel
before the text, or as the first action of `wait._default`). Since
`kuno_tells` is a passage, the image will persist through the conversation.

> [STYLE FOUNDATION] — Interior of the same hexagonal cell, the male figure
> now seated in the armchair on the right side of the composition, a second
> armchair on the left side occupied by a female figure — seen from behind or
> in partial profile — the two chairs angled slightly toward each other across
> the room's floor, the reading desk between them with its book untouched, the
> speaking plate dark on the wall behind, both figures present to each other
> rather than to apparatus, the amber light unchanged but the room now
> containing something it was not designed to contain — direct human presence
> meeting direct human presence — the botanical motifs in the walls the same
> as always, indifferent to this

**Mood:** The plate is not in use. This is what that means.

---

### ★ `kuno_cell_shaft.jpg`

**Used in scenes:** `vashti_decision_look`

**Code change required:** In `vashti_decision_look` `on_enter`, prepend
`__IMAGE:kuno_cell_shaft.jpg|` before the text — fires once when the
panel passage is entered.

> [STYLE FOUNDATION] — Interior of the same hexagonal cell, one panel of the
> padded wall at left has been pressed open at an angle, revealing behind it
> a rectangular opening of absolute darkness — rough, unpadded, undecorated,
> a purely functional passage in the WALL with no Art Nouveau treatment
> whatsoever, the shaft opening is IN THE WALL ONLY, there is NO opening in
> the floor, NO floor hatch, NO hole in the ground, the floor is completely
> solid and unbroken throughout, the contrast between the botanical motifs of
> the cell wall and the raw darkness of the wall shaft interior is the visual
> crux of the image, faint cool air movement implied by the composition,
> the male figure standing to one side of the open wall panel gesturing
> toward it without pressure, the female figure at the panel's edge looking
> into the dark wall opening, the armchair is pushed to the far side of the
> room well away from the shaft and is in a completely normal stable position
> on the floor, the cell's amber light stops cleanly at the shaft entrance
> and does not penetrate it, the book untouched on the desk

**Mood:** The shaft is the only thing in this room that was not made
by the Machine.

---

## CLUSTER 5 — THE SURFACE

*Three images of a single journey upward. Looking up from below,
emerging into grey light, and sky.*

---

### ✓ `surface_glimpse.jpg`

**Used in scenes:** `surface_approach`

> [STYLE FOUNDATION] — Looking upward from inside a ventilation shaft, the
> shaft walls are rough and completely unpadded — raw functional material with
> no Art Nouveau decoration whatsoever, dark grey-brown scarred and real —
> the shaft walls converge upward toward a circle of light at the top that
> is entirely unlike the amber of the Machine: cool, vast, grey-blue,
> sourceless in a different way — not distributed through walls but arriving
> from an open sky, the circle of exterior light at the top is the compositional
> focus, the contrast between the rough functional shaft and the implied
> memory of the Machine's decorated interiors is the whole image, the shaft
> walls show use — scratches, worn handholds

**Mood:** The amber ends here. Something else begins.

---

### ★ `surface_top.jpg`

**Used in scenes:** `surface_approach` — triggered when player goes up

**Code change required:** In `surface_approach`, `go` actions (up/surface/
out/default) currently fire `__GAMEOVER:surface__` directly. Change to
`__IMAGE:surface_top.jpg|__GAMEOVER:surface__` so the image fires as the
last thing seen before the end screen fades in.

> [STYLE FOUNDATION] — The top of a ventilation shaft, emerging from below
> into a grey open exterior, the shaft rim visible in the lower foreground
> as rough undecorated material — the last edge of the Machine's structure —
> beyond it: a vast grey sky, no ceiling, no amber, no decoration, the sky
> rendered in Art Nouveau technique but depicting pure unmanaged space,
> the horizon at distance where a hillside of abstract botanical texture
> meets the sky — the same decorative language used for the machine's
> botanical motifs but now describing real plants, real earth, uncurated,
> unhexagonal, the visual register of the entire image is the same style
> as the interior images but describing something that has never been
> managed, the light is cool and sourceless and enormous

**Mood:** The Machine made everything you have ever seen. This was not made.

---

### ★ `surface_sky.jpg`

*Optional. Reserved for a potential extended surface sequence if the game
expands. Not required for current build.*

> [STYLE FOUNDATION] — A view of open sky from ground level, looking upward
> at roughly 45 degrees, a hillside in the lower quarter of the frame with
> stylised botanical ground cover in Art Nouveau rendering — but rendering
> the chaos of real unplanted growth, not the regulated motifs of the Machine
> — the sky in the upper three-quarters vast grey-blue fading toward pale
> at the horizon, no ceiling, no architecture visible, the ventilation shaft
> opening visible at extreme lower left as a small dark rectangle — the only
> manufactured thing in the image and dwarfed by everything around it,
> cool tones throughout, the palette as far from amber as this style tradition
> can reach

**Mood:** Indifferent. Enormous. Correct.

---

## CLUSTER 6 — THE BOOK

*Two close-up images of the Book of the Machine. Same object, before and
after the stain.*

---

### ★ `book_reverenced.jpg`

**Used in scenes:** `examine_book` passage

**Code change required:** In `examine_book` scene `on_enter`, prepend
`__IMAGE:book_reverenced.jpg|` before the text.

> [STYLE FOUNDATION] — Close-up of an elaborately bound book resting on a
> reading desk, seen from a slight angle, the cover decorated with an Art
> Nouveau design of interlocking geometric and botanical motifs in deep amber
> and ivory, the title not visible or rendered as abstract decorative line
> rather than legible text, the corners and spine showing significant wear
> from long use — the cover smooth where hands habitually fall, slightly
> raised where they do not — the pages visible at the fore-edge as a dense
> compressed thickness, the desk beneath it the same warm material as the
> cell's furnishings, the book lit by the same directional-less amber light
> as all interior scenes, the whole image conveying an object that has been
> consulted every day for an entire life

**Mood:** The sum of all permitted wisdom. Worn soft in the right places.

---

### ★ `book_stained.jpg`

**Used in scenes:** `book_discolouration` passage

**Code change required:** In `book_discolouration` `on_enter`, prepend
`__IMAGE:book_stained.jpg|` before the text.

> [STYLE FOUNDATION] — Close-up of the same elaborately bound book, same
> angle and composition as book_reverenced.jpg, but on the lower portion of
> the cover a thumbprint-sized discolouration is visible — not dramatic,
> not a wound, a small shadow of transferred material from a padded wall,
> the surrounding cover unchanged and beautiful, the stain itself small enough
> that the eye almost passes over it and then does not, the mark sits within
> the Book's decorative border motifs like something that has been placed there
> and cannot be removed, the amber light catches it slightly differently from
> the surrounding cover material, the rest of the image identical to
> book_reverenced.jpg

**Mood:** A small physical fact. It connects the Book to a place it
has not been before.

---

## CLUSTER 7 — THE SPEAKING PLATE

*Two close-up images of the speaking plate. Active and failing.*

---

### ★ `plate_active.jpg`

**Used in scenes:** `kuno_first_words` through the conversation chain

**Code change required:** In `kuno_first_words` `on_enter`, prepend
`__IMAGE:plate_active.jpg|` before the text. This fires once when Kuno's
face first appears and persists through the conversation passages.

> [STYLE FOUNDATION] — Close-up of an oval speaking plate mounted in a
> padded wall, the plate itself showing a face in transmission — rendered
> as Art Nouveau portraiture, the face of a young man in partial profile,
> the image slightly stylised by the transmission as though seen through
> amber glass, the plate's decorative surround of leaves and filaments lit
> more warmly than in the default cell view, the glow of the plate's amber
> deepened to a richer ochre to indicate active connection, the padding
> of the wall visible at the plate's edges with its botanical aperture
> motifs, the face in the plate carrying an expression that is legible as
> attention — direct, present, requesting

**Mood:** The plate transmits his face. What it cannot transmit is what
his face contains.

---

### ★ `plate_static.jpg`

**Used in scenes:** `plate_failing`, `plate_static`

**Code change required:** In `plate_failing` `on_enter`, prepend
`__IMAGE:plate_static.jpg|` before the text.

> [STYLE FOUNDATION] — Close-up of the same oval speaking plate, same
> decorative surround, but the plate's surface shows interference rather
> than a clear face: multiple overlapping transmissions rendered as Art
> Nouveau line-work in conflict with itself — botanical curves crossing
> and cancelling, amber light neither fully on nor fully off but fluctuating
> between states, the plate's decorative surround intact and beautiful as
> always but the oval surface within it showing visual noise, the glow
> unsteady, multiple voices implied by multiple overlapping face-ghosts
> — each partially visible, none complete, the amber deepened to an
> unsteady flickering ochre, the padded wall behind unchanged and indifferent

**Mood:** The channel is open. There is too much in it.

---

## CODE CHANGES REQUIRED (Summary)

All new images need a corresponding `__IMAGE:` sentinel added to the game.
Changes listed in implementation order:

| Image | Scene | Where to add sentinel |
|---|---|---|
| `airship_night.jpg` | `departure` | `open.blind` action — replace `__IMAGE:airship_blind.jpg` |
| `kuno_cell_conversation.jpg` | `kuno_tells` | Add `__IMAGE:kuno_cell_conversation.jpg\|` prefix to `on_enter` |
| `kuno_cell_shaft.jpg` | `vashti_decision_look` | Add `__IMAGE:kuno_cell_shaft.jpg\|` prefix to `on_enter` |
| `corridor_failing.jpg` | `weeks_passing` | Add `__IMAGE:corridor_failing.jpg\|` prefix to `go.corridor` and `go.outside` response text |
| `surface_top.jpg` | `surface_approach` | Change all `__GAMEOVER:surface__` to `__IMAGE:surface_top.jpg\|__GAMEOVER:surface__` |
| `book_reverenced.jpg` | `examine_book` | Add `__IMAGE:book_reverenced.jpg\|` prefix to `on_enter` |
| `book_stained.jpg` | `book_discolouration` | Add `__IMAGE:book_stained.jpg\|` prefix to `on_enter` |
| `plate_active.jpg` | `kuno_first_words` | Add `__IMAGE:plate_active.jpg\|` prefix to `on_enter` |
| `plate_static.jpg` | `plate_failing` | Add `__IMAGE:plate_static.jpg\|` prefix to `on_enter` |

*Note: `surface_sky.jpg` is optional/reserved; no code change required now.*

---

## GENERATION ORDER

Recommended session sequence for compositional consistency:

**Session 1 — The Cell**
Generate `cell_normal` → `cell_restless` → `cell_flickering` → `cell_dark`
in one run. Compare all four before keeping any. The light progression must
read as a single arc.

**Session 2 — The Airship**
Generate `airship_peaceful` → `airship_blind` → `airship_night` together.
The porthole is the compositional constant; the exterior varies.

**Session 3 — The Book and Plate**
Generate `book_reverenced` → `book_stained` as a pair (same composition,
one altered detail). Then `plate_active` → `plate_static` as a pair.

**Session 4 — Kuno's Cell**
Generate `kuno_cell` → `kuno_cell_conversation` → `kuno_cell_shaft` in order.
The room is constant; the configuration of people and revealed architecture changes.

**Session 5 — Corridors and Surface**
Generate `corridor` → `corridor_failing` → `corridor_dark` together.
Then `surface_glimpse` → `surface_top` as a pair — the shaft from below,
then the shaft from above.

---

## COMPLETE FILE LIST

```
images/
  cell_normal.jpg         ✓ existing
  cell_restless.jpg       ✓ existing
  cell_flickering.jpg     ✓ existing
  cell_dark.jpg           ✓ existing
  airship_peaceful.jpg    ✓ existing
  airship_blind.jpg       ✓ existing
  airship_night.jpg       ★ new
  corridor.jpg            ✓ existing
  corridor_failing.jpg    ★ new
  corridor_dark.jpg       ✓ existing
  kuno_cell.jpg           ✓ existing
  kuno_cell_conversation.jpg  ★ new
  kuno_cell_shaft.jpg     ★ new
  surface_glimpse.jpg     ✓ existing
  surface_top.jpg         ★ new
  surface_sky.jpg         ★ optional/reserved
  book_reverenced.jpg     ★ new
  book_stained.jpg        ★ new
  plate_active.jpg        ★ new
  plate_static.jpg        ★ new
```
