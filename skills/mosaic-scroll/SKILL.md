---
name: mosaic-scroll
description: Design scroll-driven narrative and pinned scenes.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, scroll, narrative, motion, performance]
    related_skills: [mosaic]
---

# Mosaic Scroll

Scroll is pacing. This skill covers reveal-on-scroll, pinned scenes, progress rails, and horizontal chapters. The page must remain a document, not a hostage.

## When to Use

- A story needs chapters, not one long stack.
- A product needs a scroll-linked demonstration.
- A gallery benefits from reveal and pause.
- A timeline needs progress and orientation.

Do not hijack the wheel, hide content behind animation, or make the user scroll through a fake loading sequence.

## Patterns

- **Reveal**: opacity + 8-16px translate; 400-600ms; one-time; never hide the first screen.
- **Pinned scene**: a sticky visual with copy changing beside it; one scene at a time; release after two or three beats.
- **Progress rail**: a thin line or index; it must reflect real scroll position.
- **Horizontal chapter**: only for short sequences; provide a vertical fallback and keyboard.
- **Depth**: background layer moves slower; keep text stable; cap parallax to 10-20%.

## Build

- Use CSS `position: sticky` for pinning; use `IntersectionObserver` for reveal; use `scroll-timeline` where supported and a JS fallback only when needed.
- Animate `transform` and `opacity`, not layout; use `will-change` only during the animation.
- Use `requestAnimationFrame` for scroll-linked values; clamp and throttle.
- Make every chapter reachable with the keyboard and anchor links.
- Test with a trackpad, a mouse wheel, and touch.

## Accessibility

- Reduced motion: no pinning, no parallax, no reveal delay; all content is visible in normal flow.
- Never trap the scroll; Escape should not be needed to read.
- Provide a skip link and a table of contents for long narratives.
- Avoid scroll-jacking; native scroll momentum is a feature.
- Keep focus visible when a pinned scene changes.

## Performance

- One scroll listener; passive; no layout reads per frame.
- Prefer CSS scroll-driven animations for simple reveals.
- Lazy-load below-fold media; reserve dimensions.
- Pause video and shaders when offscreen.
- On low-end mobile, degrade to static sections.

## Pitfalls

- A 100vh hero followed by another 100vh hero is a slideshow, not a page.
- Pinning every section makes the page feel broken.
- Reveal animations that hide content on slow devices are an accessibility failure.
- A progress bar that jumps backward destroys trust.
- Horizontal scroll with no keyboard path traps users.

## Verification

- Keyboard: Tab and anchors reach every chapter; focus is visible.
- Reduced motion: all content visible without pinning or parallax.
- 390px: no horizontal overflow; text remains readable.
- Scroll to the end and back; progress matches position.
- Disable JS: the document still reads in order.
