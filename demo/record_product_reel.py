#!/usr/bin/env python3
"""Capture a real Mosaic product reel at 1920x1080 for the 26s film."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/home/lakshaya/projects/mosaic")
RAW = ROOT / "demo" / "raw" / "product"
RAW.mkdir(parents=True, exist_ok=True)
OUT = RAW / "ui.webm"
URL = "http://127.0.0.1:4322/"

CURSOR = r"""
() => {
  if (window.__reelCursor) return;
  window.__reelCursor = true;
  const c = document.createElement('div');
  c.id = 'reel-cursor';
  c.innerHTML = '<svg width="28" height="28" viewBox="0 0 24 24"><path d="M5 3L19 12L12 13L9 20L5 3Z" fill="#f3efe6" stroke="#15130f" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  c.style.cssText = 'position:fixed;left:0;top:0;z-index:999999;pointer-events:none;width:28px;height:28px;filter:drop-shadow(1px 2px 3px rgba(0,0,0,.35))';
  document.body.appendChild(c);
  document.addEventListener('mousemove', (e) => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; });
}
"""


def glide(page, selector: str, pause: int = 900) -> None:
    page.evaluate("(s) => document.querySelector(s)?.scrollIntoView({behavior:'smooth', block:'start'})", selector)
    page.wait_for_timeout(pause)


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(RAW),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        page.goto(URL, wait_until="networkidle", timeout=30000)
        page.evaluate("document.fonts.ready")
        page.evaluate(CURSOR)
        page.wait_for_timeout(1200)

        # 0-3s: hero. The film's stage carries the title; capture the real page.
        page.mouse.move(980, 520, steps=18)
        page.wait_for_timeout(1600)

        # 3-7s: the visual gate.
        glide(page, "#visual", 1100)
        page.mouse.move(720, 560, steps=18)
        page.wait_for_timeout(1600)
        page.mouse.move(1320, 660, steps=18)
        page.wait_for_timeout(700)

        # 7-11s: director, one brief, real concept switch.
        glide(page, "#director", 1000)
        try:
            page.select_option("#director-brief", "type-practice")
        except Exception:
            pass
        page.wait_for_timeout(700)
        page.locator(".director-concept").nth(1).click()
        page.wait_for_timeout(900)
        page.mouse.move(890, 620, steps=16)

        # 11-15s: forge lab, magnetic link and lens.
        glide(page, "#forge-lab", 900)
        mag = page.locator("mosaic-magnetic-link")
        mag.scroll_into_view_if_needed()
        page.wait_for_timeout(250)
        box = mag.locator("button").bounding_box()
        if box:
            page.mouse.move(box["x"] + box["width"] * .8, box["y"] + box["height"] * .3, steps=14)
            page.wait_for_timeout(450)
            page.mouse.move(box["x"] + box["width"] * .35, box["y"] + box["height"] * .7, steps=14)
        page.wait_for_timeout(700)
        lens = page.locator("mosaic-cursor-lens")
        lens.scroll_into_view_if_needed()
        page.wait_for_timeout(250)
        sb = lens.locator(".stage").bounding_box()
        if sb:
            page.mouse.move(sb["x"] + sb["width"] * .7, sb["y"] + sb["height"] * .5, steps=14)
        page.wait_for_timeout(900)

        # 15-19s: component ledger.
        glide(page, "#components", 900)
        page.locator(".component-row").nth(9).click()
        page.wait_for_timeout(900)
        page.mouse.move(1080, 640, steps=16)
        page.wait_for_timeout(700)

        # 19-23s: install / close.
        glide(page, "#install", 1000)
        page.mouse.move(980, 650, steps=16)
        page.wait_for_timeout(1400)

        video = page.video
        context.close()
        source = Path(video.path())
        shutil.copy2(source, OUT)
        browser.close()
    print(f"recorded {OUT} ({OUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())