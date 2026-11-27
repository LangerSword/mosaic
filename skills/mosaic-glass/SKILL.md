---
name: mosaic-glass
description: Use one glass object with a real fallback.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, glass, material, depth, translucency, fallback]
    related_skills: [mosaic, mosaic-cards, mosaic-shader]
---

# Mosaic Glass

Glass is a material decision, not a border preset. One object, one strong thing behind it, one readable layer of ink, and a solid fallback that preserves the hierarchy when blur is unavailable.

## When to Use

- A single floating artifact needs depth over a strong image, field or dark room.
- A control floats above content but must remain legible.
- A calendar, card or lens benefits from a translucent surface.

Do not glass every panel. Do not put body copy on a blur. Do not use glass when the ground behind it is flat or empty; there is nothing to refract.

## Material Rules

- **One glass family per page.** One radius, one blur, one edge recipe.
- **Contrast first.** Measure ink against the blended glass colour, not the raw ground. Body text needs 4.5:1; large text 3:1.
- **One specular edge.** Use a light top-left border and a darker lower edge; avoid a rainbow border.
- **A solid fallback.** `backdrop-filter` is optional. The fallback must keep the object, its edge and its text hierarchy.
- **No blur behind body copy.** Put prose on an opaque surface.
- **Reduced motion.** Remove tilt and parallax; keep the material and selection state.
- **Performance.** Blur is expensive; one small object, no full-screen glass, no nested filters.

## Recipe

```css
.glass {
  --glass-ink: #f7f1e7;
  --glass-fill: rgba(20, 28, 40, .58);
  --glass-edge: rgba(255,255,255,.28);
  background: var(--glass-fill);
  color: var(--glass-ink);
  border: 1px solid var(--glass-edge);
  box-shadow: inset 0 1px 0 rgba(255,255,255,.34), 0 24px 60px rgba(0,0,0,.28);
  backdrop-filter: blur(18px) saturate(1.1);
}
@supports not (backdrop-filter: blur(1px)) {
  .glass { background: #141c28; }
}
@media (prefers-reduced-motion: reduce) {
  .glass { transform: none !important; }
}
```

Pair the object with a strong field behind it. A glass card on a flat cream page reads as a grey rectangle; a glass lens over a deep field, image or ASCII field reads as a material.

## Interaction

- Pointer movement may tilt or shift the specular edge, but the object must remain still for keyboard users.
- Selection is a real state: active edge, label, and an `aria-pressed` / selected value.
- The glass object never becomes the only route to information.
- Touch gets the same object without tilt.

## Verification

- Fallback path renders without `backdrop-filter`.
- Text contrast measured against the blended fill.
- One object, one blur, no body copy on glass.
- 390px: no clipped text or horizontal overflow.
- Reduced motion keeps the object and removes tilt.
- The object is still understandable in a still screenshot.