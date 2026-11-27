#!/usr/bin/env python3
"""Render a page and return measured visual gates.

Run by ``mosaic_visual.py`` in a Python that has Playwright. It writes two
viewport screenshots and returns compact JSON. No model, no network calls are
made by the gate itself; a page may load its own fonts.
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from pathlib import Path

try:
    from PIL import Image
    from playwright.sync_api import sync_playwright
except ImportError as exc:  # pragma: no cover - host-specific
    print(json.dumps({"ok": False, "status": "needs_browser", "error": str(exc)}))
    raise SystemExit(2)


MEASURE_JS = r"""
() => {
  const seen = new Set();
  const parseColor = (value) => {
    if (!value || value === 'transparent') return [0, 0, 0, 0];
    const match = value.match(/rgba?\(([^)]+)\)/);
    if (!match) return null;
    const parts = match[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    if (parts.length < 3 || parts.some((n) => Number.isNaN(n))) return null;
    return [parts[0], parts[1], parts[2], parts.length > 3 ? parts[3] : 1];
  };
  const over = (fg, bg) => {
    const a = fg[3] + bg[3] * (1 - fg[3]);
    if (!a) return [255, 255, 255, 1];
    return [
      (fg[0] * fg[3] + bg[0] * bg[3] * (1 - fg[3])) / a,
      (fg[1] * fg[3] + bg[1] * bg[3] * (1 - fg[3])) / a,
      (fg[2] * fg[3] + bg[2] * bg[3] * (1 - fg[3])) / a,
      a,
    ];
  };
  const lum = (c) => {
    const channel = (v) => {
      v /= 255;
      return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4);
    };
    return 0.2126 * channel(c[0]) + 0.7152 * channel(c[1]) + 0.0722 * channel(c[2]);
  };
  const ratio = (a, b) => {
    const l1 = lum(a), l2 = lum(b);
    return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
  };
  const visible = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 1 && r.height > 1 && s.display !== 'none' && s.visibility !== 'hidden' &&
      Number(s.opacity) > 0.05 && !el.closest('[aria-hidden="true"], .bg-doodle, [data-visual-ignore]');
  };
  const directText = (el) => [...el.childNodes]
    .filter((node) => node.nodeType === 3)
    .map((node) => node.nodeValue || '')
    .join(' ')
    .replace(/\s+/g, ' ')
    .trim();
  const pick = (selector) => [...document.querySelectorAll(selector)].filter(visible);
  const textNodes = pick('h1,h2,h3,h4,p,li,a,button,label,small,span,strong,em,blockquote,figcaption,code')
    .map((el) => {
      const text = directText(el) || (el.children.length === 0 ? (el.textContent || '').trim() : '');
      return { el, text };
    })
    .filter((row) => row.text.length > 0);

  const backgrounds = new Map();
  const background = (el) => {
    if (backgrounds.has(el)) return backgrounds.get(el);
    let node = el, bg = [255, 255, 255, 1], image = false;
    while (node && node.nodeType === 1) {
      const s = getComputedStyle(node);
      if (s.backgroundImage && s.backgroundImage !== 'none') image = true;
      const c = parseColor(s.backgroundColor);
      if (c && c[3] > 0) {
        bg = over(c, bg);
        if (c[3] >= 0.99) break;
      }
      node = node.parentElement;
    }
    const result = { bg, image };
    backgrounds.set(el, result);
    return result;
  };

  const contrastFailures = [];
  const ambiguousContrast = [];
  const typefaces = new Set();
  let largeText = 0;
  for (const { el, text } of textNodes) {
    const s = getComputedStyle(el);
    const fg = parseColor(s.color);
    if (!fg) continue;
    typefaces.add(s.fontFamily);
    const size = parseFloat(s.fontSize) || 16;
    const weight = Number(s.fontWeight) || 400;
    const large = size >= 24 || (size >= 18.66 && weight >= 700);
    if (large) largeText += 1;
    const { bg, image } = background(el);
    const r = ratio(fg, bg);
    const expected = large ? 3 : 4.5;
    if (r + 0.01 < expected) {
      const row = { text: text.slice(0, 80), tag: el.tagName.toLowerCase(), ratio: Math.round(r * 100) / 100, expected, image };
      if (image) ambiguousContrast.push(row);
      else contrastFailures.push(row);
    }
  }

  const boxes = textNodes.map(({ el, text }) => {
    const r = el.getBoundingClientRect();
    return { el, text, box: { left: r.left, top: r.top, right: r.right, bottom: r.bottom }, tag: el.tagName.toLowerCase() };
  });
  const overlaps = [];
  for (let i = 0; i < boxes.length; i += 1) {
    for (let j = i + 1; j < boxes.length; j += 1) {
      const a = boxes[i], b = boxes[j];
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
      const left = Math.max(a.box.left, b.box.left), top = Math.max(a.box.top, b.box.top);
      const right = Math.min(a.box.right, b.box.right), bottom = Math.min(a.box.bottom, b.box.bottom);
      const area = Math.max(0, right - left) * Math.max(0, bottom - top);
      const smaller = Math.min(
        (a.box.right - a.box.left) * (a.box.bottom - a.box.top),
        (b.box.right - b.box.left) * (b.box.bottom - b.box.top)
      );
      if (area > 24 && smaller > 0 && area / smaller > 0.08) {
        overlaps.push({ a: a.text.slice(0, 55), b: b.text.slice(0, 55), area: Math.round(area) });
      }
    }
  }

  const clipped = (el) => {
    let parent = el.parentElement;
    while (parent && parent !== document.documentElement) {
      const s = getComputedStyle(parent);
      if (['hidden', 'clip', 'auto', 'scroll'].includes(s.overflowX)) return true;
      parent = parent.parentElement;
    }
    return false;
  };
  const doc = document.documentElement;
  const viewport = { width: window.innerWidth, height: window.innerHeight };
  const overflow = [];
  for (const el of pick('body *')) {
    const r = el.getBoundingClientRect();
    if (r.right > doc.clientWidth + 1 || r.left < -1) {
      const s = getComputedStyle(el);
      if (s.position !== 'fixed' && s.pointerEvents !== 'none' && !clipped(el) && !el.closest('[aria-hidden="true"], .skip, .sr-only, .visually-hidden, [data-visual-ignore]')) {
        overflow.push({ tag: el.tagName.toLowerCase(), right: Math.round(r.right), left: Math.round(r.left) });
      }
    }
  }

  const controls = pick('a[href],button,input,select,textarea,[role="button"],[role="tab"]')
    .filter((el) => !el.disabled)
    .map((el) => {
      const r = el.getBoundingClientRect();
      return { tag: el.tagName.toLowerCase(), text: (el.getAttribute('aria-label') || directText(el) || el.textContent || '').trim().slice(0, 55), width: Math.round(r.width), height: Math.round(r.height) };
    });

  const focusable = controls.filter((el) => true).length;
  const hero = document.querySelector('h1');
  const heroRect = hero ? hero.getBoundingClientRect() : null;
  const heroVisible = Boolean(hero && directText(hero).length > 0 && heroRect.width > 1 && heroRect.height > 1 && heroRect.bottom > 0 && heroRect.top < viewport.height * 0.92);
  const slots = document.querySelectorAll('[data-slot]').length;
  const images = [...document.querySelectorAll('img')].map((img) => ({
    src: (img.currentSrc || img.src || '').slice(0, 120),
    loaded: img.complete && img.naturalWidth > 0
  }));

  return {
    title: document.title,
    viewport,
    document: { width: doc.scrollWidth, height: doc.scrollHeight, clientWidth: doc.clientWidth, clientHeight: doc.clientHeight },
    text_count: textNodes.length,
    large_text_count: largeText,
    typefaces: [...typefaces],
    contrast_failures: contrastFailures.slice(0, 8),
    contrast_ambiguous: ambiguousContrast.slice(0, 8),
    overlaps: overlaps.slice(0, 8),
    overflow_elements: overflow.slice(0, 8),
    controls,
    focusable_count: focusable,
    hero_visible: heroVisible,
    content_slots: slots,
    images,
  };
}
"""

MOTION_JS = r"""
() => {
  const rows = [...document.querySelectorAll('*')].map((el) => {
    const s = getComputedStyle(el);
    return {
      tag: el.tagName.toLowerCase(),
      animation: parseFloat(s.animationDuration) || 0,
      transition: parseFloat(s.transitionDuration) || 0,
    };
  }).filter((row) => row.animation > 0.02 || row.transition > 0.02);
  return {
    reduced: matchMedia('(prefers-reduced-motion: reduce)').matches,
    moving: rows.slice(0, 12),
    moving_count: rows.length,
    has_rule: [...document.styleSheets].some((sheet) => {
      try { return [...sheet.cssRules].some((rule) => (rule.cssText || '').includes('prefers-reduced-motion')); }
      catch { return false; }
    }),
  };
}
"""

FOCUS_JS = r"""
() => {
  const el = document.activeElement;
  if (!el || el === document.body) return { active: false };
  const s = getComputedStyle(el);
  return {
    active: true,
    tag: el.tagName.toLowerCase(),
    text: (el.getAttribute('aria-label') || el.textContent || '').trim().slice(0, 55),
    outline: s.outlineStyle,
    outlineWidth: parseFloat(s.outlineWidth) || 0,
    shadow: s.boxShadow !== 'none',
    background: s.backgroundColor,
  };
}
"""


def image_stats(path: Path) -> dict:
    with Image.open(path) as img:
        rgb = img.convert("RGB").resize((160, 160))
        data = rgb.tobytes()
        counts = rgb.getcolors(maxcolors=160 * 160) or []
        counts.sort(reverse=True)
        top = counts[0][0] / (160 * 160) if counts else 0
        grey = [sum(data[i:i + 3]) / 3 for i in range(0, len(data), 3)]
        return {
            "width": img.width,
            "height": img.height,
            "dominant_share": round(top, 3),
            "colors": len(counts),
            "spread": round(statistics.pstdev(grey), 1),
            "blank": top > 0.985,
        }


def check(checks: list, name: str, ok: bool, severity: str, detail: str) -> None:
    checks.append({"name": name, "ok": bool(ok), "severity": severity, "detail": detail})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    viewports = [{"name": "desktop", "width": 1440, "height": 900, "mobile": False},
                 {"name": "mobile", "width": 390, "height": 844, "mobile": True}]
    report = {"ok": True, "target": args.url, "screenshots": {}, "viewports": [], "checks": [], "warnings": []}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        for viewport in viewports:
            errors: list[str] = []
            failed: list[str] = []
            context = browser.new_context(
                viewport={"width": viewport["width"], "height": viewport["height"]},
                device_scale_factor=1,
                is_mobile=viewport["mobile"],
                has_touch=viewport["mobile"],
                reduced_motion="no-preference",
            )
            page = context.new_page()
            page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
            page.on("pageerror", lambda exc: errors.append(f"pageerror: {exc}"))
            page.on("requestfailed", lambda req: failed.append(req.url[:160]))
            try:
                page.goto(args.url, wait_until="load", timeout=20_000)
                page.wait_for_timeout(650)
                metrics = page.evaluate(MEASURE_JS)
                shot = out / f"{viewport['name']}-{viewport['width']}.png"
                page.screenshot(path=str(shot), full_page=False, animations="disabled")
                stats = image_stats(shot)
                report["screenshots"][viewport["name"]] = str(shot)

                focus_steps = []
                for _ in range(6):
                    page.keyboard.press("Tab")
                    step = page.evaluate(FOCUS_JS)
                    if step.get("active"):
                        focus_steps.append(step)
                focus_visible = any(
                    step.get("outline") not in ("none", "") and step.get("outlineWidth", 0) > 0
                    or step.get("shadow")
                    for step in focus_steps
                )

                page.emulate_media(reduced_motion="reduce")
                page.wait_for_timeout(120)
                motion = page.evaluate(MOTION_JS)

                hard_failures = []
                if errors:
                    hard_failures.append(f"{len(errors)} console/page errors")
                if metrics["document"]["width"] > metrics["document"]["clientWidth"] + 1:
                    hard_failures.append("horizontal overflow")
                if metrics["overflow_elements"]:
                    hard_failures.append("elements outside the viewport")
                if not metrics["hero_visible"]:
                    hard_failures.append("no visible h1 in the first screen")
                if metrics["overlaps"]:
                    hard_failures.append(f"{len(metrics['overlaps'])} text overlaps")
                if metrics["contrast_failures"]:
                    hard_failures.append(f"{len(metrics['contrast_failures'])} contrast failures")
                if viewport["mobile"]:
                    small = [c for c in metrics["controls"] if c["width"] < 24 or c["height"] < 24]
                    if small:
                        hard_failures.append(f"{len(small)} controls below 24px")
                if metrics["focusable_count"] and not focus_visible:
                    hard_failures.append("focus is not visible")
                if not metrics["focusable_count"]:
                    hard_failures.append("no focusable controls")
                if motion["moving_count"] and not motion["has_rule"]:
                    hard_failures.append(f"{motion['moving_count']} moving elements without a reduced-motion rule")
                if stats["blank"]:
                    hard_failures.append("screenshot is blank")

                view = {
                    "name": viewport["name"],
                    "width": metrics["viewport"]["width"],
                    "height": metrics["viewport"]["height"],
                    "document": metrics["document"],
                    "text_count": metrics["text_count"],
                    "large_text_count": metrics["large_text_count"],
                    "typefaces": metrics["typefaces"],
                    "contrast_failures": metrics["contrast_failures"],
                    "contrast_ambiguous": metrics["contrast_ambiguous"],
                    "overlaps": metrics["overlaps"],
                    "overflow_elements": metrics["overflow_elements"],
                    "controls_count": len(metrics["controls"]),
                    "small24": [c for c in metrics["controls"] if c["width"] < 24 or c["height"] < 24][:8],
                    "small44_count": len([c for c in metrics["controls"] if c["width"] < 44 or c["height"] < 44]),
                    "focusable_count": metrics["focusable_count"],
                    "focus_steps": focus_steps[:4],
                    "focus_visible": focus_visible,
                    "motion": motion,
                    "hero_visible": metrics["hero_visible"],
                    "content_slots": metrics["content_slots"],
                    "images": metrics["images"],
                    "errors": errors[:8],
                    "failed_requests": failed[:8],
                    "screenshot": str(shot),
                    "image": stats,
                    "blockers": hard_failures,
                }
                report["viewports"].append(view)
                check(report["checks"], f"{viewport['name']}-load", not errors, "hard", f"{len(errors)} errors")
                check(report["checks"], f"{viewport['name']}-overflow", not metrics["overflow_elements"] and metrics["document"]["width"] <= metrics["document"]["clientWidth"] + 1, "hard", "no horizontal overflow" if not hard_failures else "; ".join(hard_failures))
                check(report["checks"], f"{viewport['name']}-hero", metrics["hero_visible"], "hard", "visible h1 in first screen")
                check(report["checks"], f"{viewport['name']}-overlap", not metrics["overlaps"], "hard", f"{len(metrics['overlaps'])} overlaps")
                check(report["checks"], f"{viewport['name']}-contrast", not metrics["contrast_failures"], "hard", f"{len(metrics['contrast_failures'])} failures, {len(metrics['contrast_ambiguous'])} image-ambiguous")
                check(report["checks"], f"{viewport['name']}-focus", bool(metrics["focusable_count"]) and focus_visible, "hard", f"{metrics['focusable_count']} focusables")
                check(report["checks"], f"{viewport['name']}-reduced-motion", not (motion["moving_count"] and not motion["has_rule"]), "hard", f"{motion['moving_count']} moving, rule={motion['has_rule']}")
                check(report["checks"], f"{viewport['name']}-screenshot", not stats["blank"], "hard", f"dominant {stats['dominant_share']:.3f}")
                if viewport["mobile"]:
                    small = [c for c in metrics["controls"] if c["width"] < 44 or c["height"] < 44]
                    check(report["checks"], "mobile-44", not small, "soft", f"{len(small)} controls under 44px")
                check(report["checks"], f"{viewport['name']}-density", stats["colors"] >= 6 and stats["spread"] >= 3, "soft", f"{stats['colors']} colors / {stats['spread']} spread")
            except Exception as exc:
                report["ok"] = False
                report["error"] = f"render failed: {type(exc).__name__}: {exc}"
                check(report["checks"], f"{viewport['name']}-render", False, "hard", str(exc)[:200])
            finally:
                context.close()
        browser.close()

    hard = [c for c in report["checks"] if c["severity"] == "hard"]
    soft = [c for c in report["checks"] if c["severity"] == "soft"]
    report["gates_total"] = len(hard)
    report["gates_passed"] = sum(1 for c in hard if c["ok"])
    report["soft_total"] = len(soft)
    report["soft_passed"] = sum(1 for c in soft if c["ok"])
    report["blockers"] = [c["detail"] for c in hard if not c["ok"]]
    report["warnings"] = [c["detail"] for c in soft if not c["ok"]]
    report["status"] = "pass" if not report["blockers"] and report.get("ok") else "fail"
    report["visual_guarantee"] = report["status"] == "pass"
    report["strict_visual_guarantee"] = report["visual_guarantee"] and not report["warnings"]
    report["note"] = ("Hard visual gates only: rendered layout, text contrast, overlap, first-screen h1, "
                      "focus visibility, reduced-motion, control size and a non-blank screenshot. "
                      "This is not a judgement of taste or originality.")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())