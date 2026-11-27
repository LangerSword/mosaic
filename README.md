# Mosaic

**Reference in. Original out.** A Hermes plugin and skill pack for turning a studied design reference or a product brief into an original web direction: a base field, one accent, a type pairing, two signature moves, motion rules and an audit.

It is not a template library, a cloner, or a moodboard generator. It gives the agent a design process and a small set of concrete directions, then asks it to study the actual reference and build its own work.

## What is in the box

- **21 Hermes skills**: one master method, twelve interaction families (including cast, ASCII and glass), a component grammar, study, design, critique and score methods, a measured visual gate, a forge and an inventor.
- **12 local tools**:
  - `mosaic_index`: the reference families, skills and base tokens.
  - `mosaic_study`: reference observations → principles, transfer candidates and a do-not-copy contract (a URL alone returns a checklist, not invented facts).
  - `mosaic_design`: the design director: three concepts, transparent selection, tokens, type, composition and an optional complete page starter.
  - `mosaic_components`: the public component observations, filterable by family or text.
  - `mosaic_stacks`: the HTML, React, Next, Svelte, Vue and Astro matrix with paired Hermes skills.
  - `mosaic_forge`: an original component starter for a stack, with CSS or GSAP motion.
  - `mosaic_invent`: interaction candidates with a state machine and a transparent taste score.
  - `mosaic_recipe`: a deterministic direction for a brief.
  - `mosaic_audit`: a local text scan for generic gradients, `transition: all`, missing reduced-motion and similar slop.
  - `mosaic_critique`: design-specific source critique for prompt leakage, copy, focus, slots, radius/font noise.
  - `mosaic_score`: a transparent pre-awards text score with blockers and next moves.
  - `mosaic_visual`: render a URL or local page in Chromium; return two screenshots, hard-gate results, contrast/overlap/focus/reduced-motion evidence and a bounded `visual_guarantee`.
- **A CLI** over the same handlers, for a demo or CI without Hermes.

No network calls, no API keys, no telemetry, no copied assets. The visual gate is the only renderer: it runs a page the caller already built, locally, and needs Playwright Chromium in a browser-capable Python.

## Install

```bash
cp -a mosaic ~/.hermes/plugins/mosaic
hermes plugins enable mosaic
python scripts/install_skills.py
```

Start a new Hermes session so the tools and skills enter the index. The skills can also be copied by hand from `skills/` to `~/.hermes/skills/web-design/`.

## Use

```bash
python mosaic_cli.py index
python mosaic_cli.py study --reference "DIA" --observations '{"layout":"index and specimen split","what_works":"the index is the navigation"}'
python mosaic_cli.py design --brief "A quiet portfolio for a type designer" --mode page
python mosaic_cli.py recipe --brief "A collectible racing deck for a design conference" --mood tactile
python mosaic_cli.py components --family press
python mosaic_cli.py stacks
python mosaic_cli.py forge --kind swipe-confirm --stack react --motion gsap
python mosaic_cli.py invent --brief "A quiet onboarding for a design tool" --count 3
python mosaic_cli.py critique --path src/app.css
python mosaic_cli.py audit --path src/app.css
python mosaic_cli.py visual --target http://127.0.0.1:4322/
```

In a Hermes session:

```text
mosaic_study(reference={name: "DIA", observations: {layout: "index and specimen split"}})
mosaic_design(brief="A quiet portfolio for a type designer", mode="page")
mosaic_critique(path="src/components/Hero.tsx")
```

`mosaic_design` is the design-director pass. It returns three structural concepts, the selected concept with transparent scores, a reference map, the design system, a content contract and — in `page` mode — a complete static starter. A reference URL alone is not a study; `mosaic_study` returns a capture checklist until observations are supplied.

The recipe is a starting direction, not an answer. It deliberately returns a thesis, a token table, two moves, a build order and acceptance checks; the agent still has to study the reference, write original code and verify in a browser.

## Visual gate

`mosaic_score` is a text score. It is not a visual guarantee. `mosaic_visual` is the browser-backed half:

```bash
python mosaic_cli.py visual --target http://127.0.0.1:4322/
```

One Chromium launch, two viewports (`1440x900`, `390x844`), two screenshots and a hard pass/fail. It measures console errors, overflow, first-screen `h1`, text overlaps, WCAG contrast, focus visibility, reduced motion, control size and a non-blank screenshot. `visual_guarantee` is true only when every hard gate passes; `strict_visual_guarantee` also requires the soft 44px mobile target rule and is reported honestly when it fails.

The tool returns paths to the screenshots instead of base64, so a normal call stays small. It needs Playwright Chromium in a browser-capable Python; on a machine without one it returns `status: "needs_browser"` and refuses to claim a pass.

A bounded guarantee: rendered layout, contrast, interaction affordance and interaction state. It does not judge taste.

## Skills

| Skill | Use |
|---|---|
| `mosaic` | Master method: reference map, system choice, composition, motion, audit |
| `mosaic-cards` | Card objects, stacks, fans, arcs, pockets |
| `mosaic-press` | Press, hold-to-confirm, destructive actions |
| `mosaic-drag` | Direct manipulation, reorder, drop targets |
| `mosaic-hover` | Hover reveals, cursor previews, magnetic actions |
| `mosaic-cast` | Random character peeks behind section rules |
| `mosaic-study` | Reference observations → transferable principles |
| `mosaic-design` | Brief → three concepts → system and page starter |
| `mosaic-critique` | Source review for specificity and honesty |
| `mosaic-ascii` | Monospace character fields and ASCII atmosphere |
| `mosaic-glass` | One glass material with a real fallback |
| `mosaic-score` | Pre-awards design, usability and originality gate |
| `mosaic-visual` | Render a page and pass or fail measured visual gates |
| `mosaic-select` | Segmented controls, tabs, small pickers |
| `mosaic-shader` | Atmospheric shaders with static fallbacks |
| `mosaic-type` | Editorial type, wordmarks, labels, numerals |
| `mosaic-scroll` | Scroll-driven narrative and pinned scenes |
| `mosaic-loading` | Agent thinking states and honest progress |
| `mosaic-components` | Component state matrices and the public component grammar |
| `mosaic-forge` | Stack-aware component starters with CSS or GSAP |
| `mosaic-invent` | Interaction candidates with a typed taste rubric |

Each skill has a trigger, a procedure, pitfalls and a verification pass. The master skill carries the reference method and the public Construct teardown.

## Design stance

1. A specimen is one idea. Name it before you style it.
2. The shell is quiet; the object is loud. Spend colour, type and motion on one thing.
3. State is physical. Press, hold, drag and select should show contact, commitment and release.
4. Type carries hierarchy. Display, body and utility are different jobs.
5. Data is an instrument. Use ticks, counters and rails, not generic dashboards.
6. Motion has a cause. Remove decoration that does not answer a state change.
7. Texture is a material, not a default. Pick paper, glass, metal or pixel; not all four.
8. The document works without the show: keyboard, reduced motion and slow network are part of the design.

## Example site

`site/index.html` is a static, dependency-free product page for the plugin: a reference table, a live component lab, a recipe panel and the install path. Serve it locally with:

```bash
python3 -m http.server 4173 --directory site
```

The page is verified at 1440 and 390, with no horizontal overflow and no console errors. Screenshots are in `docs/site-1440.png` and `docs/site-390.png`.

## 60 second film

[Read the 0.8.0 release](https://github.com/LangerSword/mosaic/releases/tag/v0.8.0): strict visual-gate notes, new specimens and the catalog pin. The earlier 60-second film is at [v0.5.0](https://github.com/LangerSword/mosaic/releases/tag/v0.5.0); source and build steps are in `demo/`.

## Reference study and independence

The reference notes in `skills/mosaic/references/construct-teardown.md` are an original study of the public Construct Design catalog and four free specimen pages at `https://www.tobiadonadon.com/projects/construct/design`. The study records layout, type, tokens and interaction behavior. It does not copy code, assets or the paid library. Mosaic is unaffiliated with Construct or Tobia Donadon.

Construct is a useful reference precisely because it is plural: a quiet gallery around many independent specimens. Mosaic turns that observation into a method, not a skin.

## Evidence

- 40 unit tests pass with stdlib only.
- `smoke_load.py` loads the real entry point against a recording context, asserts 12 tools and dispatches them.
- `hermes plugins validate` and `hermes plugins doctor` are the admission gates.
- CLI outputs are deterministic and JSON.
- 20 public component observations are included; six second-row components were account-gated, and the rest of the catalog requires an account. None were bypassed.

## Limits

- The audit is a text heuristic, not a browser, contrast or performance test.
- Recipes are directions, not generated pages. The agent must still build and verify.
- The reference study is public-page observation, not a licence to reuse the reference.
- No code is generated or executed by the plugin.

## License

MIT. See `LICENSE`.
