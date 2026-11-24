---
name: mosaic-forge
description: Forge a component starter for any frontend stack.
version: 0.1.0
author: Lakshaya Sharma (LangerSword), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [design, components, forge, react, next, svelte, vue, astro, gsap]
    related_skills: [mosaic, mosaic-components]
---

# Mosaic Forge

Mosaic Forge turns a one-line brief and a component family into an original starter for HTML, React, Next, Svelte, Vue or Astro. The shared core is a custom element; the framework files are thin event adapters. Motion can be CSS or GSAP.

It is a starter generator, not an autonomous product designer. It optimises for a correct state machine, accessible markup, and a clean handoff to the target framework. It does not copy a reference's implementation.

## When to Use

- You need a component family with the same behaviour across several stacks.
- You want a working state machine before designing the final page.
- A model needs a bounded, inspectable starting point instead of a blank file.
- You need CSS and GSAP variants of the same component.

Do not use for a whole page, a design system replacement, or a reference clone.

## Inputs

- `kind`: `hold`, `segmented`, `thinking`, `paper-plane`, `swipe-confirm`, `download-ring`, `checklist`.
- `stack`: `html`, `react`, `next`, `svelte`, `vue`, `astro`, or `all`.
- `motion`: `css` or `gsap`.
- `brief`: one sentence about the product; optional but useful.

Call `mosaic_forge` when the plugin is installed, or `mosaic_cli.py forge` for a local file.

## Stack Matrix

`mosaic_stacks` returns the current matrix. The short version:

| Stack | Adapter | Pair with |
|---|---|---|
| HTML/CSS/JS | `demo.html` | `web-workflow`, `frontend-design`, `accessibility` |
| React | `index.tsx` | `react-patterns`, `react-ui-patterns`, `gsap-react` |
| Next.js | `index.tsx` with `use client` | `nextjs-app-router-patterns`, `nextjs-best-practices` |
| Svelte 5 | `index.svelte` | `sveltekit`, `gsap-frameworks` |
| Vue 3 | `index.vue` | `nuxt4-patterns`, `gsap-frameworks` |
| Astro | `index.astro` | `astro`, `gsap-frameworks` |

Load at most three skills per phase; the matrix is a route, not a reading list.

## Procedure

1. Pick one kind and write the one-sentence behaviour. Completion: the brief names the action and the result.
2. Call `mosaic_forge(kind, stack, motion, brief)`. Completion: files are returned, not just a description.
3. Inspect the core file. Completion: the state machine has a cancel path, keyboard path and event name.
4. Inspect the adapter. Completion: it imports the core, subscribes to the event and renders the tag.
5. Run the target framework's build. Completion: no new global CSS, no hydration warning, no missing custom-element registration.
6. Test pointer, keyboard, reduced motion and the error/cancel path. Completion: screenshots or test output.

## GSAP

Use GSAP where it earns its weight: paper-plane flight, swipe spring, segmented indicator, staged loading. Keep the state machine plain JavaScript; GSAP should animate, not own truth. Import `gsap` as a package in the target app; do not use a CDN in production. Respect `prefers-reduced-motion`: finish the state instantly and keep the content.

## Verification

- The core is a valid custom element and registers exactly once.
- Framework adapter imports the core and compiles.
- Keyboard and pointer reach the same action.
- Reduced motion removes transforms, not the result.
- Labels use `textContent`; no user text is injected as HTML.
- The generated component is original; the reference map is not a skin.

## Pitfalls

- A custom element in React needs a stable ref and an effect cleanup; otherwise listeners leak.
- Next needs `"use client"` for the adapter; the core itself has no server render.
- Svelte/Vue custom-element events are DOM events, not framework events; bridge them explicitly.
- GSAP plus a custom element can double-register a timeline on re-render; create it in `connectedCallback` and revert on disconnect.
- A forge starter is not a finished page. Typography, composition and content still belong to the master skill.
