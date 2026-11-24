# Palimpsest

**Reference in. Original out.** A Hermes plugin and skill pack for turning a studied design reference or a product brief into an original web direction: a base field, one accent, a type pairing, two signature moves, motion rules and an audit.

It is not a template library, a cloner, or a moodboard generator. It gives the agent a design process and a small set of concrete directions, then asks it to study the actual reference and build its own work.

## What is in the box

- **10 Hermes skills**: one master method and nine interaction families.
- **3 local tools**:
  - `palimpsest_index`: the reference families, skills and base tokens.
  - `palimpsest_recipe`: a deterministic direction for a brief.
  - `palimpsest_audit`: a local text scan for generic gradients, `transition: all`, missing reduced-motion and similar slop.
- **A CLI** over the same handlers, for a demo or CI without Hermes.

No network calls, no API keys, no telemetry, no rendering, no copied assets.

## Install

```bash
cp -a palimpsest ~/.hermes/plugins/palimpsest
hermes plugins enable palimpsest
python scripts/install_skills.py
```

Start a new Hermes session so the tools and skills enter the index. The skills can also be copied by hand from `skills/` to `~/.hermes/skills/web-design/`.

## Use

```bash
python palimpsest_cli.py index
python palimpsest_cli.py recipe --brief "A collectible racing deck for a design conference" --mood tactile
python palimpsest_cli.py audit --path src/app.css
```

In a Hermes session:

```text
palimpsest_recipe(brief="A quiet portfolio for a type designer", mood="editorial")
palimpsest_audit(path="src/components/Hero.tsx")
```

The recipe is a starting direction, not an answer. It deliberately returns a thesis, a token table, two moves, a build order and acceptance checks; the agent still has to study the reference, write original code and verify in a browser.

## Skills

| Skill | Use |
|---|---|
| `palimpsest` | Master method: reference map, system choice, composition, motion, audit |
| `palimpsest-cards` | Card objects, stacks, fans, arcs, pockets |
| `palimpsest-press` | Press, hold-to-confirm, destructive actions |
| `palimpsest-drag` | Direct manipulation, reorder, drop targets |
| `palimpsest-hover` | Hover reveals, cursor previews, magnetic actions |
| `palimpsest-select` | Segmented controls, tabs, small pickers |
| `palimpsest-shader` | Atmospheric shaders with static fallbacks |
| `palimpsest-type` | Editorial type, wordmarks, labels, numerals |
| `palimpsest-scroll` | Scroll-driven narrative and pinned scenes |
| `palimpsest-loading` | Agent thinking states and honest progress |

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

## Reference study and independence

The reference notes in `skills/palimpsest/references/construct-teardown.md` are an original study of the public Construct Design catalog and four free specimen pages at `https://www.tobiadonadon.com/projects/construct/design`. The study records layout, type, tokens and interaction behavior. It does not copy code, assets or the paid library. Palimpsest is unaffiliated with Construct or Tobia Donadon.

Construct is a useful reference precisely because it is plural: a quiet gallery around many independent specimens. Palimpsest turns that observation into a method, not a skin.

## Evidence

- 12 unit tests pass with stdlib only.
- `smoke_load.py` loads the real entry point against a recording context, asserts 3 tools and dispatches all three.
- `hermes plugins validate` and `hermes plugins doctor` are the admission gates.
- CLI outputs are deterministic and JSON.

## Limits

- The audit is a text heuristic, not a browser, contrast or performance test.
- Recipes are directions, not generated pages. The agent must still build and verify.
- The reference study is public-page observation, not a licence to reuse the reference.
- No code is generated or executed by the plugin.

## License

MIT. See `LICENSE`.
