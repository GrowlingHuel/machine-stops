# IF DESIGN BIBLE
## The Machine Stops — and the Engine Behind It

*A reference document for narrative structure, player guidance, branching design,
and the craft of text adventure writing. Applicable to all future games on this engine.*

---

## PART ONE: THE CORE PROBLEM

### What Goes Wrong in IF, and Why

Text adventure games fail players in one specific way more than any other: **the player has no idea what the game considers interesting.** They are placed in a space described in words, and they do not know which words are load-bearing.

This is different from being stuck on a puzzle. Being stuck on a puzzle is fine. Being stuck on the question *what am I even supposed to be doing* is not fine, and it is a mood-killer that kills games.

The classic era acknowledged this and largely didn't care. Zork was notoriously obtuse; players died constantly and restarted. This was acceptable in 1977 because:

1. The audience self-selected for patience
2. There was no competing entertainment
3. Discovery *was* the game — finding the parser's vocabulary was a puzzle in itself

None of these conditions apply now. The audience for this game includes people who have never played IF. Mobile players in transit. People who will give an unfamiliar format ninety seconds before deciding it isn't for them.

The solution is not to make the game easier. It is to make the game *legible* — to ensure that at every moment, the player has at least one clearly available thread to pull.

---

## PART TWO: THE BREADCRUMB PRINCIPLE

### The HHGTTG Model

The opening of the Infocom Hitchhiker's Guide to the Galaxy game (Adams/Meretzky, 1984) is the gold standard of IF onboarding. The player wakes in a dark room, head throbbing. There is a paragraph of description. Almost everything in that paragraph is interactive. The game's first puzzle — turning on the light — is *in the description*. The next puzzle (the hangover, the bulldozers) arrives before the first one is fully resolved. The player is never without something to do, because the *world is visibly doing things around them*.

The lesson is not "make it obvious." The lesson is: **the description contains the affordances.** Every object named in a room description is an implicit promise that the object rewards interaction. If you name something and it does nothing, you have broken the contract.

### The Three Levels of Breadcrumb

**Level 1 — Environmental:** The description itself. Every object mentioned should do *something*. Not necessarily advance the plot — but reward the player's attention. A speaking plate that glows amber rewards examination. A Book that has worn patches from years of use rewards reading. The room's *texture* should be interactive.

**Level 2 — Directional:** At least one element in each location's description should actively *invite* a specific verb. Not "the plate is on the wall" — but "the plate glows amber, as though waiting." The word *waiting* invites `use plate` or `touch plate`. This is not hand-holding. This is craft.

**Level 3 — Escalating Fallback:** When a player has entered three or more unrecognised commands in a row, the fallback response should shift register — from atmospheric to gently directive. This is the hint system disguised as prose.

### The Fallback Escalation System

The engine currently has a single `_fallback` string per scene. This should be extended to support **escalating fallbacks**:

```json
"_fallback": [
  "The cell hums around you. The plate glows.",
  "Your attention returns, again, to the speaking plate. It carries something.",
  "The plate. You should use the plate."
]
```

When `_fallback` is an array, the engine uses index `min(fallback_count, array.length - 1)`, where `fallback_count` tracks consecutive unresolved inputs in the current scene. Reset on any successful action.

**Engine change required:** Add `G.fallback_count` to state; increment on unresolved input; reset on resolved input; modify `resolve()` to handle array fallbacks.

This system preserves atmosphere — the first fallback is poetic, in-world — while guaranteeing that a player who is genuinely lost will eventually be given a legible push.

---

## PART THREE: NARRATIVE ARCHITECTURE — CURRENT STATE AUDIT

### Scene Inventory (32 scenes)

```
PART ONE — THE AIR-SHIP
  vashti_cell           [SCENE]     Opening cell. Good bones, thin affordances.
  examine_book          [PASSAGE]   Book examination. Good but isolated.
  kuno_first_words      [PASSAGE]   Kuno's request. Works.
  kuno_why              [PASSAGE]   Kuno explains. Works.
  kuno_press            [PASSAGE]   Pressing for detail. Works.
  kuno_refuse           [PASSAGE]   Refusing to come. Works.
  decision_travel       [SCENE]     Post-call decision. Good.
  preparing_travel      [SCENE]     Booking passage. Thin but functional.
  corridor              [SCENE]     First corridor. Needs more texture.
  airship_cabin         [SCENE]     The blind scene. Strong.
  kuno_cell             [SCENE]     Arrival at Kuno's. Strong.
  kuno_tells            [PASSAGE]   Kuno's revelation. Strong.
  kuno_detail           [PASSAGE]   The sky. Strong.
  kuno_why_surface      [PASSAGE]   Why he went. Good.
  kuno_homeless_threat  [PASSAGE]   The charge. Strong.
  vashti_decision_look  [PASSAGE]   The shaft. THE KEY BRANCH. Well-fixed.
  vashti_refuses_shafts [PASSAGE]   Refusing the shaft. Good.
  departure             [SCENE]     Return journey. Good.

PART TWO — THE MACHINE STOPS
  vashti_cell_return    [SCENE]     Home again. Good.
  book_discolouration   [PASSAGE]   The stain. Good detail.
  messages              [PASSAGE]   The judgement notice. Good.
  kuno_judgement_call   [PASSAGE]   Kuno's response. Good.
  the_sound             [PASSAGE]   Hearing the irregularity. Good.
  weeks_passing         [SCENE]     Time passing. THIN. Needs expansion.
  committee_announcement[PASSAGE]   The denial. Good.
  kuno_last_call        [PASSAGE]   Final warning. Good.
  plate_failing         [PASSAGE]   Plate failing. Good.

PART THREE — HOMELESS
  machine_stops         [SCENE]     Darkness. Strong.
  corridor_dark         [SCENE]     The dying corridor. Strong.
  find_kuno             [SCENE]     Searching. Good.
  reunion               [SCENE]     Finding him. Good.
  surface_approach      [SCENE]     The shaft. Good.
```

### Structural Problems

**1. The opening has no urgency signal.**
The plate is described as glowing amber. This is passive. The player has no reason to believe the plate is the thing that opens the game. Compare to HHGTTG: the light is off, which *demands* a response.

*Fix:* The plate should be doing something active at game-open. Not necessarily alarming — but present. A pulse. An attempted connection. Something that says: *this is the door.*

**2. Part Two is a single corridor.**
The journey from `vashti_cell_return` to `machine_stops` passes through only: the stain, the messages, the judgement call, the sound, and weeks passing. That is not enough for a middle act. The player has returned changed from Kuno's cell. The Machine is beginning to fail. This is the most psychologically complex moment in the story — Vashti noticing something she doesn't want to notice — and it gets five scenes.

*Fix:* Part Two needs a minimum of four additional scenes. Proposals below.

**3. The branch at the shaft has no downstream weight.**
`looked_in_shaft` is set as a flag but is never checked again. The shaft scene is the most important choice in the game — Vashti chose to look into the unmediated dark, or she didn't — and currently it has zero effect on Part Three. This is the game's biggest structural failure.

*Fix:* The flag must gate something meaningful in Part Three. See Endings Architecture below.

**4. There is only one pathway through Part Three.**
The corridor after the Machine stops is essentially linear. There are two possible endings (surface or reunion) but the path to both is the same. The difference is a flag set at a scene twenty minutes earlier. The player in Part Three has no meaningful choices to make.

*Fix:* Part Three needs at least one genuine in-the-moment decision that affects outcome.

**5. The "compliant death" ending is not a real choice.**
The `compliant_death` ending exists in the ENDINGS object but there is no path to it in the scenes. A player cannot choose to stay in their cell and die with the Machine. This is a dramatically important option — Vashti, in the novel, almost makes this choice — and it should be available.

*Fix:* `machine_stops` should allow the player to sit and wait. After several wait inputs, the air becomes unbreathable and the ending triggers.

**6. The `witnessed_death` ending has no path either.**
Same problem. These endings exist as text but are unreachable.

---

## PART FOUR: THE PERFECT PLAN

### Guiding Principles

1. **Every named thing rewards interaction.** If it's in the text, it does something.
2. **Every scene has a visible thread.** The player always has one clear invitation.
3. **Branches have weight.** Every meaningful choice must affect at least one downstream scene.
4. **Endings are earned.** Each of the four endings is the result of accumulated choices, not a single late decision.
5. **The fallback escalates.** A stuck player is never abandoned; the world gently redirects them.
6. **The prose never breaks register.** All of the above is achieved through the world's own voice, not mechanical instruction.

---

### REVISED SCENE ARCHITECTURE

#### PART ONE — THE AIR-SHIP

**`vashti_cell` — Opening Cell**

*Problem:* Passive opening. No urgency.

*Fix:* Change the plate from `glows amber` to `pulses amber — a rhythm you have not seen before, like a call not yet answered`. This single change transforms the plate from furniture to protagonist. The player's first instinct will be to interact with it.

Add to `on_enter`: *"The speaking plate on the near wall pulses in a rhythm you do not recognise. Not the steady amber of standby. Something is asking."*

Add escalating fallback:
```json
"_fallback": [
  "The room contains what it has always contained. The plate pulses.",
  "The pulse of the plate is patient. It is waiting for your attention.",
  "The speaking plate is asking for you. You could use it, or touch it, to answer."
]
```

**`examine_book` — The Book**

No structural change needed. This is a good digression that enriches the world. Ensure all named procedures in the Book's description (music, food, temperature, Mending Apparatus) are interactive.

**Kuno conversation chain — `kuno_first_words` through `kuno_press`**

These work well. The dialogue tree is appropriately constrained. 

*One addition:* Add a `refuse` path that is truly viable — a player who refuses and closes the call should reach `decision_travel` with a different text variant, maintaining the branch feeling. Currently `kuno_refuse` loops back toward acceptance. It should be possible to *genuinely* refuse — but the cell should then do something to make you reconsider (a flicker in the light; the Music slightly wrong for the first time).

**`airship_cabin` — The Blind**

This is one of the game's strongest scenes. The open/close blind mechanic is genuinely evocative.

*Addition:* The blind should have more consequence. If the player opens it and reads the text carefully, they get `__FLAG:saw_outside__`. This flag enables an additional response at `vashti_decision_look` (Vashti already knows what outside looks like from the porthole) — and contributes to the Reunion ending.

**`vashti_decision_look` — The Shaft**

This is the game's most important scene. The current structure is good (after fixes). 

*Critical addition:* Looking in the shaft must set a flag that matters in Part Three. Current flag `looked_in_shaft` should gate `find_kuno` in Part Three — Kuno told her where the shaft was; without having looked at it, she cannot find it in the dark. This creates genuine consequence.

**New scene: `corridor_outbound`**

Currently the outbound corridor is passed through instantly. Add one beat: Vashti notices a person in the corridor who appears to be looking out — not inward, as is correct — but toward the wall, pressing one hand against the padding. The attendant moves them along. Vashti files this away.

This plants a seed: people outside their cells, people pressing against walls, the idea of what is behind the surface. It is not plot. It is texture that makes the world feel inhabited.

---

#### PART TWO — THE MACHINE STOPS

This act is currently a single corridor. It needs four additional scenes:

**New scene: `lecture_given`**

Vashti gives a lecture (she is described in the story as a lecturer on music). The player can choose her topic — Music of the Australian Period is canonical. The lecture is received through plates across the world. During it, a connection drops. Just one, briefly, in the middle of a sentence. It reconnects. She continues.

*Purpose:* Establishes Vashti's competence and social role; plants the first clear sign of Machine failure in a context she cares about; gives the player something to *do* in Part Two rather than just witnessing events.

*Flag set:* `gave_lecture`. If flag is set when Machine stops, a specific line triggers in `machine_stops`: *"The lecture you were to give tomorrow will now not be given."*

**New scene: `mending_delayed`**

Something in the cell fails — the bath-water, specifically, which Forster mentions. Vashti summons the Mending Apparatus. It does not respond immediately. This has never happened. After what feels like a long time (a wait sequence), it responds. Slowly. Something is repaired. Not quite as before.

*Purpose:* The Machine's decline becomes personal. Not abstract. Not something happening to others. Happening to her bath.

*Flag set:* `mending_was_late`. In `weeks_passing`, adds a line: *"The Mending Apparatus has been late twice more since the bath incident."*

**New scene: `plate_conversations`**

Vashti connects with other residents — colleagues, students — through the plate. The player can choose to raise the subject of fluctuations or not. If raised: she receives a range of responses. Some deny it. One person, anonymous, says quietly: *"It has been wrong for a long time. I have been thinking that for a while."* Then disconnects.

*Purpose:* Shows the societal texture of denial. Vashti is not alone in noticing; she is alone in not fully suppressing the noticing. The anonymous voice is important: someone else is awake. This foreshadows the Homeless survivors in Part Three.

**New scene: `kuno_homeless` (after `messages`)**

Between learning of the judgement and calling Kuno, a beat: Vashti sits with the notice. She could contact the Committee — appeals are within provision. She could do nothing. She could call Kuno immediately. Each choice is available; each has a slightly different texture in the scene that follows. The appeal path goes nowhere (the Committee's response is polite and absolute) but gives the player the feeling of having tried, which matters emotionally.

*Flag set:* `attempted_appeal` if player tried. In the final corridor: *"There had been a notice from the Committee. You had appealed. The Committee had responded. The Committee was silent now."*

---

**Revised `weeks_passing`**

This scene currently has one job — transition to the Machine's failure — but should do two: let the player explore the failing world, *and* allow an optional act of unusual noticing that contributes to the `surface` ending.

*Addition:* Allow `go outside`, `go corridor`, `explore`. Vashti cannot leave (this is slightly unusual — she is allowed to, but the impulse is rare). If the player tries, she steps into the corridor briefly and notices: the air is slightly different. Returns to her cell. Sets flag `noticed_corridor_air`. In Part Three, this makes `surface_approach` available without Kuno's instruction.

---

#### PART THREE — HOMELESS

**`machine_stops` — The Cell in Darkness**

*Addition:* Make `wait` truly available — not just "you cannot wait through this" but an actual sequence. First wait: the air is still. Second wait: thicker. Third wait: the armchair is still the armchair. The cell is still the cell. The Book is here. Fourth wait: `__GAMEOVER:compliant_death__`.

This is the most important addition to Part Three. The compliant death should be a *genuine* ending for players who embody Vashti's faith in the Machine. It is not a failure state. It is a choice with a beautiful, sad ending text.

**`corridor_dark` — The Dying Corridor**

*Addition:* Allow the player to pick up a Book from the floor. `__INVENTORY:add:found_book__`. The found Book, if carried to `surface_approach`, adds a coda to the surface ending: *"You carried it up. You did not read it on the surface. You left it at the top of the shaft, pages open, as though it might still instruct something."*

**`plate_failing` — Noise on the Line**

*Addition:* Player can `listen` to the static. Within it: a voice, saying something too broken to parse. This is not Kuno. This is someone else, somewhere else, still trying to connect. Sets flag `heard_the_voice`. In the `witnessed_death` ending, adds: *"You had heard a voice in the static. You never knew whose it was."*

**New scene: `corridor_fork`**

After `corridor_dark`, before the final approach, the player faces a genuine in-the-moment decision: air from above (the surface) or a sound from ahead (voices — possibly Kuno). 

The player must choose direction. Going up leads to `surface_approach`. Going forward leads to `find_kuno` (only if `kuno_final_message` flag is set; otherwise Kuno is not there, and the player reaches `witnessed_death`).

This gives Part Three its own agency — independent of earlier choices — while those earlier choices still determine whether the forward path is viable.

---

### ENDINGS ARCHITECTURE

#### Four Endings — Paths and Requirements

```
COMPLIANT DEATH — "The Machine Stops"
  Path: machine_stops → wait × 4
  No flags required.
  Meaning: Perfect faith. The Machine was everything.
           There is a dignity to this ending that must be in the text.
  Text: "You remained in your armchair. The air grew slow, 
         then still. The dark was total and quiet. You had 
         not gone anywhere you were not supposed to go.
         The Machine, at the end, held you."

WITNESSED DEATH — "The Last Transmission"  
  Path: machine_stops → corridor_dark → corridor_fork → forward 
        (without kuno_final_message flag)
  Optional enrichment: heard_the_voice flag adds a coda.
  Meaning: Tried to connect. Found no one. Witnessed the end.
  Text: "You went toward the voices and found the corridor
         ending. The phosphorescence was nearly gone.
         You sat against a wall that had, until very recently,
         been lit from within. You were present at the end
         of something enormous. You understood what it was.
         This was not nothing."

SURFACE — "The Homeless"
  Path: machine_stops → corridor_dark → corridor_fork → up →
        surface_approach → go up
  Enrichment: noticed_corridor_air makes the climb easier (different text).
              found_book adds the Book coda.
              saw_outside adds: "The sky was exactly as the porthole had
              suggested, and entirely different."
  Meaning: Physical survival. Contact with the noumenal.
  Text: "The sky was there. It did not care about you.
         This was, you found, the correct response.
         You breathed it directly. The air had no procedure.
         It entered you without instruction."

REUNION — "What Survives"
  Path: machine_stops → corridor_dark → corridor_fork → forward
        (WITH kuno_final_message AND 
         [looked_in_shaft OR saw_outside OR attempted_appeal])
  Meaning: Love, direct and unmediated. The noumenal through a person.
  Note: This is the hardest ending to reach — requires both
        the final message flag AND evidence of accumulated
        openness to the unmediated. Not just one choice.
        The player who earns it has been playing a specific
        kind of Vashti throughout.
  Text: "They found each other in the dark. His hand.
         Her hand. Real. The word the Book had warned 
         against was the only word that applied.
         What came next is not the story.
         That there was a next is."
```

#### Flag Accumulation for Reunion Ending

The Reunion ending requires the player to have accumulated evidence of Vashti's awakening throughout. This is the novel's real thesis: the change is not sudden. It is a series of small attended-to things that build toward the capacity to act.

Qualifying flags (any one is sufficient alongside `kuno_final_message`):
- `looked_in_shaft` — looked into the unmediated dark
- `saw_outside` — opened the blind on the airship
- `attempted_appeal` — tried to intervene for Kuno
- `noticed_corridor_air` — went into the corridor during weeks_passing
- `heard_the_voice` — listened to the static on the failing plate

This means the Reunion ending is reachable through multiple different playthroughs with different emphases. A player who never opened the blind but appealed for Kuno and listened to the static can still reach it. A player who did nothing but examine things attentively cannot.

---

## PART FIVE: THE BREADCRUMB AUDIT

For each scene, the `on_enter` must contain at least one embedded affordance — a word or phrase that invites a specific verb.

### Affordance Checklist Per Scene

| Scene | Embedded Affordance | Invited Verb |
|---|---|---|
| `vashti_cell` | "plate pulses amber, as though waiting" | `use plate` / `touch plate` |
| `examine_book` | "summoning food, adjusting temperature, producing music" | `use food` / `produce music` |
| `kuno_first_words` | "He is waiting" | `talk` / `ask why` |
| `airship_cabin` | "a blind covers the porthole to your left" | `open blind` |
| `kuno_cell` | "He stands in the centre of the floor" | `talk kuno` |
| `vashti_decision_look` | "Kuno says nothing" | `examine shaft` / `go in` |
| `weeks_passing` | "the music has been slightly wrong" | `listen` / `examine music` |
| `machine_stops` | "what are you, here, without the Machine to answer it" | `wait` / `go out` |
| `corridor_dark` | "the sound of air" | `go toward air` / `listen` |

Every scene not listed needs its `on_enter` reviewed for affordances before content expansion.

---

## PART SIX: CONTENT GENERATION DIRECTIVES

When using Claude (or any LLM) to generate game text for this engine, the following constraints apply to every prompt:

### Tonal Constraints

1. **Write entirely from within the world.** No character has a frame of reference outside the Machine's reality. The Machine is not a metaphor to anyone inside it — it is the literal structure of existence.

2. **Second person for immediate experience; third person for expository description.** "You notice the plate is warm" — not "Vashti noticed the plate was warm." But: "The Book of the Machine was compiled over nine generations" — not "You know that the Book was compiled..."

3. **The Gnostic register.** The world is the phenomenal: managed, mediated, adequate. What Kuno has touched is the noumenal: immediate, vast, indifferent. The horror is not that the phenomenal is bad. The horror is that it has occluded something. Vashti's tragedy is that she has genuinely lost the capacity to miss what she has lost. Write from inside that loss.

4. **No modern register.** No word, image, or construction that would be recognisably contemporary. The aesthetic is the story's own era: Forster writing in 1909, imagining forward. The machinery should feel genuinely speculative, not retro-fitted.

5. **Earn every moment of beauty.** The surface ending, Kuno's descriptions of the sky, the hand found in the dark — these must feel earned by the bleakness that precedes them. Do not soften the Machine's world in early passages.

### Structural Constraints for Generated Passages

Every generated passage must:
- Contain at least one **named interactive object** (a thing the player can examine, take, use, or go toward)
- Contain at least one **implicit invitation** (a phrase that suggests what to do next without stating it)
- Have a **`_fallback`** that is atmospheric on first trigger and directive by third trigger (array format)
- Never use `_fallback` to eject the player from a passage — only `go` should transition away

---

## PART SEVEN: PASSAGES STILL NEEDED

Beyond the new scenes described above, the following passages are needed to reach the target passage count and provide meaningful player latitude:

### Part One (gaps)
- `lecture_given` + 3 sub-passages (topic choice, delivery, the dropped connection)
- `corridor_outbound` (the person pressing the wall)
- `refusing_travel_final` (genuine refusal path — Machine flickers, Vashti reconsiders)

### Part Two (gaps)
- `mending_delayed` + 2 sub-passages
- `plate_conversations` + 4 sub-passages (3 denial responses + 1 anonymous voice)
- `kuno_homeless` (sitting with the notice; the appeal option)
- `committee_appeal` + 1 sub-passage (the response)
- `weeks_passing` extension: `corridor_briefly` (stepping out)

### Part Three (gaps)
- `corridor_fork` (the directional decision)
- `plate_failing` extension: `heard_static_voice`
- `compliant_death` sequence (wait × 4)
- `witnessed_death` approach (forward path without Kuno)

### Total Passage Count Projection

| Part | Current | Additional | Projected |
|---|---|---|---|
| Part One | 18 | 8 | 26 |
| Part Two | 10 | 12 | 22 |
| Part Three | 8 | 6 | 14 |
| **Total** | **36** | **26** | **62 scenes/passages** |

This does not yet approach 500 unique text responses. The passage *count* is one axis; the response *depth* is another. Each scene should have 8–15 unique examine/look/use responses. At 62 scenes × 10 responses average = 620 unique text nodes. The target is met through depth, not just scene count.

---

## PART EIGHT: ENGINE IMPROVEMENTS REQUIRED

### 1. Fallback Counter
```javascript
G.fallback_count = 0; // reset on scene load and successful action
// In process(): if result is _fallback, increment G.fallback_count
// In resolve(): if array, use min(G.fallback_count, array.length - 1)
```

### 2. Wait Counter Per Scene
Some scenes need to count consecutive `wait` inputs to trigger delayed outcomes (compliant death, urgency escalation).
```javascript
G.wait_count = 0; // reset on scene change or non-wait action
```

### 3. `__WAIT_GATE:n|action__` Sentinel
Triggers `action` only after `n` consecutive wait inputs:
```json
"wait": { "_default": "__WAIT_GATE:4|__GAMEOVER:compliant_death__" }
```
Before the gate triggers, each wait prints a passage from a `_wait_sequence` array.

### 4. `__CHOICE:` Sentinel for Branching Decisions
For the `corridor_fork` scene and similar, a more explicit choice prompt:
```json
"_on_enter_choice": {
  "prompt": "The corridor divides. Air comes from above. Voices — or something like voices — come from ahead.",
  "up": "__TRANSITION:surface_approach__",
  "forward": "__IF:kuno_final_message|__TRANSITION:find_kuno__|__TRANSITION:witnessed_approach__|__"
}
```

### 5. `scenes.json` as Source of Truth
The inline `SCENES` object in `index.html` is a development fallback. For production, `scenes.json` is the single source of truth. A build step (simple Node script) should validate `scenes.json` against a schema: check all `__TRANSITION:`, `__PASSAGE:`, and `__GAMEOVER:` targets exist; check all `flags_required` are set somewhere; report orphaned scenes.

---

## PART NINE: APPLICABILITY TO FUTURE GAMES

This document was written for *The Machine Stops* but the principles below apply to any game on this engine:

### Universal IF Design Checklist

**Opening beat:**
- [ ] Player has an immediate, visible thing to do within the first description
- [ ] That thing rewards interaction (not a dead end)
- [ ] Something in the environment is *doing something* (not static)
- [ ] The fallback on the opening scene escalates to explicit direction by third trigger

**Per scene:**
- [ ] Every named noun in `on_enter` has an `examine` entry
- [ ] At least one noun in `on_enter` embeds an invitation (a verb-suggesting word)
- [ ] `_fallback` is an array of 2–3 responses, escalating from atmospheric to directive
- [ ] No passage ejects player to a new scene on `_fallback` — only `go` transitions

**Branches:**
- [ ] Every flag set at a branch has at least one downstream check
- [ ] Every meaningful choice has a visible (though not necessarily immediate) consequence
- [ ] The hardest/best ending requires accumulated choices, not a single late decision

**Endings:**
- [ ] Each ending is reachable through a distinct play style, not just a different late choice
- [ ] The worst ending (death, failure) is still a real ending with real text — not just "you died"
- [ ] The best ending is genuinely hard to reach but fair — a player who played attentively will find it

**Prose:**
- [ ] Every passage stays in its chosen register (second person for experience, third for exposition)
- [ ] No character speaks about their world in a way that implies outside knowledge of it
- [ ] The world's horror/beauty is earned through accumulation, not stated

---

*Document version: 1.0*
*Written for: The Machine Stops (Jesse Clark / GrowlingHuel)*
*Engine: Static JSON + vanilla JS PWA*
*Next review: After Part Two expansion*
