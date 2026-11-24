---
name: mosaic-type
description: Compose editorial type, wordmarks and labels.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, typography, editorial, wordmark, labels]
    related_skills: [mosaic]
---

# Mosaic Type

Type is the fastest way to make a page feel like something. This skill covers editorial display, wordmarks, mixed voices, labels, and the small type that makes a system feel designed.

## When to Use

- A hero needs a point of view rather than a default sans.
- A product needs a wordmark or a type-led identity.
- A dense interface needs labels, indices, and numerals that read as a system.
- A page feels generic because every element uses the same face and weight.

## System

- One display voice: grotesk, serif, or hand. One body face. One utility face for code, numbers, or labels.
- Pair by contrast, not by similarity: a tight grotesk display with a quiet serif body, or a serif display with a mono utility.
- Use a variable font when possible; load only the axes you use.
- Keep body measure at 45-75ch; display lines can be shorter.
- Use `clamp()` for display; keep line-height below 1 for tight display, 1.45-1.65 for body.
- Use tabular numerals for data and aligned columns.

## Editorial Moves

- One oversized line, one small label, one paragraph. Let the line carry the page.
- A wordmark can be set, outlined, cropped, or repeated; pick one move.
- Put a small hand or italic accent only where a human voice belongs; never for body copy.
- Use a rule, index, or issue number as a typographic object.
- Align display text to the grid, then break it once with intent.

## Labels and Data

- Uppercase labels: 10-12px, tracking 0.12-0.2em, only for short labels.
- Metadata: 11-13px, muted, tabular; do not bold every value.
- Numbers: use a mono or tabular face; align decimals.
- Units: smaller and quieter than the number.
- Avoid all-caps paragraphs; they are hard to read and look like a template.

## Font Loading

- Use `font-display: swap`; provide a local fallback with similar metrics.
- Preload only the display face used above the fold.
- Reserve layout space; do not let a late font shift the hero.
- Subset if the face supports it; check the license before self-hosting.

## Accessibility

- Body text at least 16px; 18px is better for long copy.
- Contrast 4.5:1 for body; 3:1 for large display.
- Do not use letter-spacing or all-caps for essential long text.
- Respect user font scaling; avoid fixed-height text containers.
- Links need more than color: underline or weight change.

## Pitfalls

- Inter for everything is not a type system.
- A script face for body copy is unreadable at length.
- A gradient headline is not a brand; use it only if the words earn it.
- Negative tracking on small text closes counters and hurts legibility.
- Five weights of the same face is not hierarchy; size and space do more.

## Verification

- Screenshot the hero at 1440 and 390; the line breaks are intentional.
- Zoom to 200%; no clipped text or overlapping labels.
- Check tabular numerals in a data block.
- Confirm font fallback does not shift the first screen.
- Read one paragraph aloud; if you stumble, the measure or size is wrong.
