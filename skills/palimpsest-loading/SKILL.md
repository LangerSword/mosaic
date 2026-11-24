---
name: palimpsest-loading
description: Design agents that show thinking, not spinners.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, loading, agent, status, shimmer]
    related_skills: [palimpsest]
---

# Palimpsest Loading

Loading is a promise about what the system is doing. A spinner says "wait"; a good thinking state says "here is the work." This skill covers agent progress, skeletons, shimmer, and slow states.

## When to Use

- An AI or long-running process needs a waiting state.
- A page fetches data that changes the layout.
- A multi-step job needs orientation.
- A slow network or cold render needs an honest status.

Do not fake a percentage, animate a progress bar that is not tied to work, or show a spinner for more than a moment without context.

## Anatomy

1. **What is happening**: one short verb phrase, not "Loading...".
2. **Where we are**: a step list with done/current/pending states.
3. **How long**: a measured elapsed time or a real estimate; omit if unknown.
4. **What you can do**: cancel, retry, or leave; do not trap the user.
5. **What comes next**: the first piece of real content, as soon as it exists.

## Build

- Use a real status model: idle, working, slow, done, error, cancelled. Do not map everything to `isLoading`.
- A skeleton mirrors the final layout; it is not a gray rectangle soup.
- Shimmer is a slow, low-contrast highlight; it must stop for reduced motion.
- If a step completes, mark it done and move the current marker; do not reset the list.
- After 8-10 seconds, show a slower-state message and a way out.
- Stream partial content when you can; a blank page is the worst skeleton.

## Accessibility

- Use `role="status"` and `aria-live="polite"` for the current step; do not announce every frame.
- Give the region an accessible name tied to the task.
- Reduced motion: static skeleton, no shimmer, no pulse.
- Keep a visible focus target and a cancel path.
- On error, announce the error and the next action.

## Pitfalls

- A fake percentage is worse than no percentage.
- An infinite shimmer with no timeout makes the page feel dead.
- A spinner centered in a huge empty page hides the product.
- Loading states that shift the final layout cause a second wait.
- A cancelled job that still reports success destroys trust.

## Verification

- Fast path: content appears without a flash of skeleton.
- Slow path: step advances, slow message appears, cancel works.
- Reduced motion: no shimmer; status still announces.
- Error: message is specific and retry is reachable.
- Screen reader: one status announcement per step, not per frame.
