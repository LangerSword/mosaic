# Mosaic

**Reference in. Original out.** A Hermes plugin and skill pack for turning a studied design reference or a product brief into an original web direction: a base field, one accent, a type pairing, two signature moves, motion rules and an audit.

It is not a template library, a cloner, or a moodboard generator. It gives the agent a design process and a small set of concrete directions, then asks it to study the actual reference and build its own work.

## What is in the box

- **13 Hermes skills**: one master method, nine interaction families, a component grammar, a forge and an inventor.
- **7 local tools**:
  - `mosaic_index`: the reference families, skills and base tokens.
  - `mosaic_components`: the public component observations, filterable by family or text.
  - `mosaic_stacks`: the HTML, React, Next, Svelte, Vue and Astro matrix with paired Hermes skills.
  - `mosaic_forge`: an original component starter for a stack, with CSS or GSAP motion.
  - `mosaic_invent`: interaction candidates with a state machine and a transparent taste score.
  - `mosaic_recipe`: a deterministic direction for a brief.
  - `mosaic_audit`: a local text scan for generic gradients, `transition: all`, missing reduced-motion and similar slop.
- **A CLI** over the same handlers, for a demo or CI without Hermes.

No network calls, no API keys, no telemetry, no rendering, no copied assets.

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
python mosaic_cli.py recipe --brief "A collectible racing deck for a design conference" --mood tactile
python mosaic_cli.py components --family press
python mosaic_cli.py stacks
python mosaic_cli.py forge --kind swipe-confirm --stack react --motion gsap
python mosaic_cli.py invent --brief "A quiet onboarding for a design tool" --count 3
python mosaic_cli.py audit --path src/app.css
```

In a Hermes session:

```text
mosaic_recipe(brief="A quiet portfolio for a type designer", mood="editorial")
mosaic_audit(path="src/components/Hero.tsx")
```

The recipe is a starting direction, not an answer. It deliberately returns a thesis, a token table, two moves, a build order and acceptance checks; the agent still has to study the reference, write original code and verify in a browser.

## Skills

| Skill | Use |
|---|---|
| `mosaic` | Master method: reference map, system choice, composition, motion, audit |
| `mosaic-cards` | Card objects, stacks, fans, arcs, pockets |
| `mosaic-press` | Press, hold-to-confirm, destructive actions |
| `mosaic-drag` | Direct manipulation, reorder, drop targets |
| `mosaic-hover` | Hover reveals, cursor previews, magnetic actions |
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

[Watch the demo](https://github.com/LangerSword/mosaic/releases/tag/v0.5.0): a kinetic intro, real footage of the live site, the Forge playground, the generated component lab, the Taste lab and the end card. Source and build steps are in `demo/`.

## Reference study and independence

The reference notes in `skills/mosaic/references/construct-teardown.md` are an original study of the public Construct Design catalog and four free specimen pages at `https://www.tobiadonadon.com/projects/construct/design`. The study records layout, type, tokens and interaction behavior. It does not copy code, assets or the paid library. Mosaic is unaffiliated with Construct or Tobia Donadon.

Construct is a useful reference precisely because it is plural: a quiet gallery around many independent specimens. Mosaic turns that observation into a method, not a skin.

## Evidence

- 21 unit tests pass with stdlib only.
- `smoke_load.py` loads the real entry point against a recording context, asserts 7 tools and dispatches them.
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
