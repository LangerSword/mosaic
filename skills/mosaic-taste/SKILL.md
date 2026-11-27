---
name: mosaic-taste
description: Use when a page needs a taste profile, not a fake taste score.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, taste, critique, evidence, preference]
    related_skills: [mosaic, mosaic-score, mosaic-visual]
---

# Mosaic Taste

A transparent proxy profile for taste. It measures the parts of taste that can
be measured, and states the part that cannot: preference.

## Use when

- A page needs a stronger point of view, not just a contrast check.
- Two valid directions need to be compared without pretending one is universal.
- A score says "8.9" and you want to know which dimensions produced it.
- You want to start a pairwise calibration loop with a real audience.

Do not use it as a universal taste oracle. A number without votes is a
hypothesis.

## Run it

```text
mosaic_taste(path="src/pages/index.astro", brief="A quiet portfolio for a type designer")
```

```bash
mosaic taste --path ./dist/index.html --brief "A quiet portfolio for a type designer"
```

Output:

```json
{
  "taste_index": 8.1,
  "confidence": "medium",
  "dimensions": {
    "hierarchy": 6.0,
    "rhythm": 7.8,
    "craft": 10.0,
    "restraint": 8.5,
    "specificity": 9.0,
    "tension": 8.3,
    "fit": 7.8,
    "originality": 7.0
  },
  "calibration": {
    "status": "unpaired",
    "needed": ["blind pairwise votes", "held-out pairs", "judge agreement"]
  }
}
```

## What each dimension means

- **hierarchy** — type-scale contrast, `h1`, and heading order.
- **rhythm** — share of spacing values on a consistent unit.
- **craft** — focus, reduced motion, line-height, measure, alt text, semantics.
- **restraint** — colour, font-family, radius and effect counts.
- **specificity** — content slots, custom elements, real artifacts vs generic copy.
- **tension** — display scale and structural contrast; not random overlap.
- **fit** — overlap between the brief and the page language.
- **originality** — custom structure and artifacts, penalised by generic copy.

These are **proxies**. A page can score well and still feel dead.

## Turn it into a real taste model

1. Generate 3 variants of the same brief.
2. Blind-pair them. Ask "which is better for this audience?" — never "rate out of 10."
3. Record votes with the feature vectors.
4. Fit `P(A > B) = sigmoid(w · (features(A) - features(B)))`.
5. Hold out pairs. Report agreement and rank correlation.
6. Change one feature only and check the preference moves. If it does not, the
   feature is noise.

Until step 5 passes, `confidence` stays low or medium and the index is not a
verdict.

## Efficient usage

- One call per candidate page.
- Use `mosaic_score` for copy/structure and `mosaic_visual` for the browser
  gates; taste is a separate layer.
- Compare profiles, not absolute numbers. A higher `tension` is not better if
  the brief asks for quiet.
- Use the brief; without it `fit` is only a default and confidence stays low.

## Verification

- Run on at least two valid variants.
- Record the dimensions that changed and the one feature you mutated.
- Keep the calibration status visible in the report.
- If the user asks for "the best taste," answer with a preference model and its
  uncertainty, not a universal score.