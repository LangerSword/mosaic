# Public component notes

Observed on the public Construct Design preview pages, 2026-11-24. The source is a public preview, not paid code; these notes are paraphrases of visible behavior and are not a licence to copy implementation. Live tool: `mosaic_components`.

| id | Family | State and timing observation | Source |
|---|---|---|---|
| flow-canvas | select | A token of light travels a dotted graph; nodes light and tick; clicking selects a node in an inspector strip. | `?block=flow-canvas` |
| face-card | hover | Halftone portrait; tilt, sheen, local dot swell; the eye reveals digits; copy becomes a tick. | `?block=face-card` |
| live-card | press | Pulsing LIVE tag, count tick, lift; Join live becomes Joining... then You're in. | `?block=live-card` |
| glass-month | hover | Frosted word over a photo; lean and light sweep; click sweeps once. | `?block=glass-month` |
| card-arc | drag | Portrait cards on a ring; ghost ends; drag, click, arrows or keys spring to the next card. | `?block=card-arc` |
| script-over | press | A hand writes a word over a condensed word; press writes the next; pen 1400ms. | `?block=script-over` |
| channel-rail | drag | The middle channel rises and goes live; count and caption change; the next glides in on a 4.5s step. | `?block=channel-rail` |
| publish-bar | press | Autosave spins; Publish fills, ticks and flips DRAFT to LIVE. | `?block=publish-bar` |
| beat-wordmark | press | Letters pump to a beat; press drops the word with a squash. | `?block=beat-wordmark` |
| join-group | press | Join becomes Joined; your disc slides into the member stack; the count rolls up. | `?block=join-group` |
| live-cursors | hover | Named cursors glide, pause and colour a node; a click pings the spot. | `?block=live-cursors` |
| story-pills | press | An unread badge pops; the pill hops to the front; tapping springs the badge away. | `?block=story-pills` |
| hold-to-confirm | press | A 1200ms fill from the left; measured about 21% at 250ms and 96% at 1150ms; completion becomes a check and holds itself; release keeps the completed state. | `?block=hold-to-confirm` |
| segmented-control | select | One track, one sliding indicator, content changes without moving the furniture. | `?block=segmented-control` |
| thinking-shimmer | loading | Named steps, elapsed time and a quiet shimmer; no invented percentage. | `?block=thinking-shimmer` |
| quanta | type | One large claim, a live tokens-per-second instrument, a proof block and a benchmark area. | `?block=quanta` |
| paper-plane | press | A send action folds a plane out of the button, flies it across the surface and resolves into a sent confirmation. | Guanmo AI, UI microinteractions #4 |
| swipe-confirm | drag | A handle drags along a track; crossing the threshold confirms, releasing early settles back; a keyboard alternative is required. | Guanmo AI, UI microinteractions #4 |
| download-ring | loading | A circular progress ring fed by real bytes or job events, not a timer; completion becomes a check. | Guanmo AI, UI microinteractions #4 |
| checklist | select | Tasks with a real done state, a strike and a progress rail; the remaining count is announced. | Guanmo AI, UI microinteractions #4 |

## What to carry into an original component

1. Write the state matrix before the surface: rest, hover, focus, press, loading, success, error, disabled, cancelled.
2. Pick one primary type: object, control, instrument or surface.
3. Make the state understandable in a still frame; use motion to explain the transition.
4. Give every pointer state a keyboard or focus equivalent.
5. Use public observations as a design vocabulary, not a template gallery.
