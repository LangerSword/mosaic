#!/usr/bin/env python3
"""Record the real failing and fixed candidate pages for the Redline film."""
from __future__ import annotations

import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/home/lakshaya/projects/mosaic")
OUT = ROOT / "demo" / "raw" / "redline"
OUT.mkdir(parents=True, exist_ok=True)

CURSOR = r"""
() => {
  if (window.__redlineCursor) return;
  window.__redlineCursor = true;
  const c = document.createElement('div');
  c.innerHTML = '<svg width="26" height="26" viewBox="0 0 24 24"><path d="M5 3L19 12L12 13L9 20L5 3Z" fill="#f3efe6" stroke="#15130f" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  c.style.cssText = 'position:fixed;left:0;top:0;z-index:999999;pointer-events:none;width:26px;height:26px;filter:drop-shadow(1px 2px 3px rgba(0,0,0,.35))';
  document.body.appendChild(c);
  document.addEventListener('mousemove', (e) => { c.style.left = e.clientX + 'px'; c.style.top = e.clientY + 'px'; });
}
"""


def record(page, out: Path) -> None:
    page.goto(f"file://{out.with_suffix('.html')}", wait_until="load", timeout=30000)
    page.evaluate("document.fonts.ready")
    page.evaluate(CURSOR)
    page.wait_for_timeout(500)
    page.mouse.move(980, 520, steps=16)
    page.wait_for_timeout(900)
    page.evaluate("document.querySelector('#signature')?.scrollIntoView({behavior:'smooth',block:'start'})")
    page.wait_for_timeout(1600)
    page.mouse.move(760, 620, steps=16)
    page.wait_for_timeout(700)
    page.evaluate("document.querySelector('.specimen-controls')?.scrollIntoView({behavior:'smooth',block:'center'})")
    page.wait_for_timeout(1300)
    page.mouse.move(1080, 650, steps=16)
    page.wait_for_timeout(900)


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        for name in ("fail", "fixed"):
            context = browser.new_context(
                viewport={"width": 1920, "height": 1080},
                record_video_dir=str(OUT),
                record_video_size={"width": 1920, "height": 1080},
            )
            page = context.new_page()
            record(page, ROOT / "demo" / "redline" / name)
            video = page.video
            context.close()
            source = Path(video.path())
            shutil.copy2(source, OUT / f"{name}.webm")
            page.close()
        browser.close()
    print(f"recorded {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())