---
name: palimpsest-cards
description: Build layered card objects with physical depth.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, cards, depth, interaction]
    related_skills: [palimpsest]
---

# Palimpsest Cards

Cards are small objects with edges, weight, and a front and back. This skill covers stacks, fans, arcs, pockets, and hover lift. It is about objecthood, not putting every piece of content in a rounded rectangle.

## When to Use

- A page needs a collectible, a hand, a deck, a ticket, a wallet, or a layered preview.
- A flat grid needs one physical object as the focal point.
- You need depth without glassmorphism.

Do not use for ordinary content cards that have no interaction or hierarchy.

## Anatomy

1. **Silhouette**: one radius family, one border weight, one aspect ratio.
2. **Face**: image or type first; metadata on a quiet rail.
3. **Edge**: a 1px light line on the top-left, a darker line on the bottom-right.
4. **Shadow**: two layers, a tight contact shadow and a wide ambient shadow.
5. **Depth cue**: overlap, scale, rotation, or blur. Pick one primary cue.

## Composition Patterns

- **Stack**: 3-7 cards, 8-14px offsets, one card forward; use for a deck or history.
- **Fan**: rotate around a point below the cards; angle step 3-6 degrees; use for a hand.
- **Arc**: place cards on a shallow curve; use for a hero or collection.
- **Pocket**: a sleeve or slot holds the card; use for saved or owned items.
- **Hover lift**: translateY(-6 to -12px), rotate 0-3 degrees, shadow grows. One card at a time.

## Build

```css
.card {
  border-radius: var(--card-radius);
  border: 1px solid var(--line);
  box-shadow: 0 1px 1px rgb(0 0 0 / .12), 0 18px 40px -24px rgb(0 0 0 / .45);
  transform: translateZ(0);
  transition: transform 180ms var(--ease-out), box-shadow 180ms var(--ease-out);
}
.card:hover, .card:focus-visible {
  transform: translateY(-8px) rotate(-1deg);
  box-shadow: 0 2px 2px rgb(0 0 0 / .12), 0 28px 56px -28px rgb(0 0 0 / .5);
}
```

Use a wrapper with `perspective` only when you tilt in 3D. Keep the tilt small: 4-8 degrees. Do not tilt on touch. Do not animate `width`, `height`, or `top`.

## Content Hierarchy

- One dominant element: portrait, number, or title.
- One quiet label row: set, role, rarity, or date.
- One action or stat block; not both at equal weight.
- Keep metadata in tabular numerals.
- Use a short serial or index; it makes the object feel catalogued.

## Accessibility

- The card must be usable with keyboard if it is interactive. Use a real button or link, not a div with a click handler.
- Do not put essential text only in an image.
- Keep text contrast at 4.5:1; decorative foil may be lower contrast but cannot carry meaning.
- Reduced motion: remove lift and tilt; preserve focus ring.
- Touch: no hover-only actions; reveal actions in a visible row.

## Pitfalls

- Ten identical glass cards is a grid, not an object.
- A huge blur behind every card kills text and frame rate.
- `overflow: hidden` on the stack clips the lifted card; give the stage padding.
- Rotating cards with text can make it fuzzy; keep text on a separate unrotated layer when needed.

## Verification

- Screenshot the stack at rest and one card lifted.
- Tab through all interactive cards; focus is visible and order is logical.
- Emulate reduced motion; no transform and no lost content.
- Check the first card still reads at 390px.
