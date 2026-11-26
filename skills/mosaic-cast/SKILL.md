---
name: mosaic-cast
description: Design random cast peeks behind section rules.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, interaction, characters, mascot, pixel-art, cast]
    related_skills: [mosaic, mosaic-scroll, mosaic-hover]
---

# Mosaic Cast

A cast is not a redesign. It is one or two characters who occasionally appear in a section, then leave. The page must work without them, and the characters must never cover the thing they are meant to make warmer.

## When to Use

- A portfolio or product has one or two authored characters, mascots or recurring figures.
- A section wants a small moment of personality without a popup, modal or card.
- The characters are decorative-adjacent: they add voice, not information.
- There is a safe edge, rule or paper band to hide the lower body behind.

Do not use this for primary navigation, actions, prices, empty states or anything the user must interact with. Do not place the cast in the hero, the footer or every section by default; the repeated entrance belongs to **one** chosen section unless the brief says otherwise.

## Shape

- One wrapper inside the chosen section, absolutely positioned above the section head.
- One button per character, each with an accessible name. The image is `alt=""` inside the button.
- The button clips its sprite (`overflow: hidden`) and has a paper bar at the bottom so the character rises from behind the section rule.
- Sprite starts at `translateY(110%)`; `.is-up` moves to `0`. Use 380–480ms and one ease.
- Show one character at a time, or both together as a scroll-synced pair.
- Randomness can select the next character in a solitary rhythm, or the pair can share
  one scroll progress so both rise and fall together. Do not mix the two rhythms on
  one section.
- Hide when the section leaves the viewport; pause the timer or scroll listener, do
  not keep a hidden loop running.

## Placement

- Reserve a quiet strip between the section's top edge and its heading. Verify
  `peek.bottom <= sectionHead.top`.
- Keep the cast out of every doodle's bounding box. Measure both rects at 1440
  and 390, not by eye.
- On mobile, shrink the peek or remove the paper label; never let it cover the
  heading. If there is no safe strip, hide the cast on that breakpoint.
- Never use `position: fixed`, and never use a corner card for a section-native
  cast.

## Art

- Match the page's existing medium. For pixel art, use a small logical canvas,
  transparent background, a 1–2px dark outline, hard cel shading and a limited
  palette; display with `image-rendering: pixelated`.
- A head-and-shoulders bust is enough for a peek. Full bodies are for the footer
  walker, not for a section rule.
- Give each character a readable silhouette and one signature cue. The name is
  in the paper bar, not drawn into the sprite.
- Do not copy a copyrighted sprite sheet. Build original silhouettes from
  references and keep the identity cues (hair, garment, colour) original.

## Scroll-synced pair

When the cast belongs to a section rule, both characters can share one progress value:

```js
const start = sectionTop - innerHeight * 0.96;
const end = sectionTop - innerHeight * 0.50;
const p = clamp((scrollY - start) / (end - start), 0, 1);
peeks.style.setProperty('--peek-y', `${(1 - p) * 108}%`);
peeks.style.setProperty('--peek', p);
```

- The buttons sit on the section rule and extend upward; use `overflow: visible` on
  the host section and a local z-index below the fixed header.
- Drive both characters from the same progress, but stagger each character by a small
  offset (for example `index * innerHeight * 0.08`) so they do not lock to one frame.
- Put the speech bubble outside the clipped image wrapper; a bubble inside the image
  clip disappears exactly when the character peeks out.
- Add a boop: click squishes the sprite, throws a tiny spark and reveals a bubble.
- On mobile, hide labels before shrinking the art; keep the boop bubble above the
  head and inside the viewport.

## Minimal Build

```html
<div class="cast" data-cast>
  <button class="cast-member" data-cast-member="anya" aria-label="Anya peeks out">
    <img src="/cast/anya.png" alt="" aria-hidden="true" />
    <span class="cast-label"><b>anya</b><span>peek</span></span>
  </button>
  <button class="cast-member" data-cast-member="ichigo" aria-label="Ichigo peeks out">
    <img src="/cast/ichigo.png" alt="" aria-hidden="true" />
    <span class="cast-label"><b>ichigo</b><span>peek</span></span>
  </button>
</div>
```

```css
.cast { position: absolute; inset: 6px 0 auto; z-index: 4; height: 88px; pointer-events: none; }
.cast-member { position: absolute; bottom: 0; width: 84px; height: 88px; overflow: hidden; pointer-events: auto; }
.cast-member img { position: absolute; bottom: 8px; left: 50%; height: calc(100% - 8px); transform: translate(-50%, 110%); transition: transform .42s var(--ease); }
.cast-member.is-up img { transform: translate(-50%, 0); }
.cast-label { position: absolute; inset: auto 0 0; z-index: 2; background: var(--paper); border-top: 1px solid var(--line-strong); }
```

```js
const section = document.querySelector('.work-section');
const members = [...document.querySelectorAll('[data-cast-member]')];
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
let visible = false, active = -1, timer = 0;
const show = (i) => members.forEach((m, j) => m.classList.toggle('is-up', j === i));
const hide = () => members.forEach((m) => m.classList.remove('is-up'));
const cycle = () => {
  if (!visible) return;
  clearTimeout(timer);
  const next = active < 0 ? (Math.random() > .5 ? 1 : 0) : active === 0 ? 1 : 0;
  show(next); active = next;
  timer = setTimeout(() => { hide(); active = -1; timer = setTimeout(cycle, 1200); }, 2600);
};
const io = new IntersectionObserver(([e]) => {
  visible = e.isIntersecting;
  if (visible) cycle(); else { clearTimeout(timer); hide(); active = -1; }
}, { threshold: .12 });
if (!reduced) io.observe(section); else show(0);
```

## Accessibility

- Real `<button>`s with accessible names; images are decorative.
- `focus-visible` parity; clicking a member shows it without stealing focus.
- Reduced motion: one static peek or no peek; never a loop.
- Do not announce every random cycle to a screen reader; the name lives in the paper bar and the button label.
- Pause timers when the section leaves the viewport.

## Pitfalls

- Fixed corner cards drift into the content. Section-native cast does not.
- A character that covers a doodle, heading or CTA is a bug, not charm.
- Hiding a section's only useful control behind a random character is an accessibility failure.
- Too many characters at once turns a quiet site into a sticker sheet.
- `setInterval` without a visibility gate keeps waking a hidden page.
- A bust with no identity cue is a generic face; use one specific hair, garment or colour cue.

## Verification

- Both character names are reachable by click and keyboard.
- Only one member is visible at a time.
- `peek.bottom <= sectionHead.top` at 1440x900 and 390x844.
- `intersection(peekRect, doodleRect) === null` for every background doodle.
- Offscreen: no timers, no movement, no DOM leaks.
- Reduced motion: one static member, no transitions, no random loop.
- No console errors and no horizontal overflow.
