---
name: mosaic-select
description: Design segmented pickers and selection surfaces.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, interaction, select, segmented, picker]
    related_skills: [mosaic]
---

# Mosaic Select

Selection is a spatial promise: one option is active, the others are still reachable, and changing your mind is cheap. This skill covers segmented controls, pill pickers, tabs, and small menus.

## When to Use

- Two to five mutually exclusive options are visible at once.
- A tab set changes the content below it.
- A filter needs a compact, obvious state.
- A form needs a choice that is faster than a dropdown.

Do not use a segmented control for more than about five options, for multi-select, or for actions that submit immediately.

## Anatomy

- **Track**: a quiet container with one border or one inset shadow.
- **Options**: equal-height targets; labels short enough to scan.
- **Indicator**: one moving pill or underline; it shows state, not a second decoration.
- **Active**: darker text, solid surface, or one accent; do not use three cues at once.
- **Content change**: swap content without moving the control; preserve scroll where sensible.

## Build

Use a radio group for real form state, or a tablist with `role="tablist"` and `aria-selected` for panels. Keep the active value in the URL or a cookie only when it is useful to share or remember. For a sliding indicator, measure the active button and animate `transform`, not `left` and `width`. If the labels change width, animate the indicator with a spring or a 180ms ease-out.

## Content

- Keep option labels to one or two words.
- Put the count or unit in a quieter span; do not make every option a billboard.
- If the choice changes a chart or card, give the result a short title, not just a new number.
- Persist a choice only when it is a preference, not when it is a transient view.

## Accessibility

- Use native radios or a correct tablist; arrow keys move within a group.
- The active state must be programmatic, not only a color.
- A segmented control must still work at 320px; reduce to a scrollable row or a native select.
- Touch targets at least 44px; no tiny pills.
- Reduced motion: move the indicator instantly; keep the state change.

## Pitfalls

- A pill with a shadow on every option looks like five buttons, not one control.
- Changing the content before the control settles makes the page feel unstable.
- A tablist without panel associations is just a row of links.
- Using color alone for the active option fails color-blind users.
- A dropdown for three options hides the comparison the user came for.

## Verification

- Keyboard arrows change the active option and panel; focus is visible.
- The active option is announced; the panel has a label.
- 320px: no clipped labels; control remains usable.
- Reduced motion: indicator jumps; no content is lost.
- Refresh or share URL: the intended state is restored.
