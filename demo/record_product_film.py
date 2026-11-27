#!/usr/bin/env python3
"""Record the 26-second Mosaic product film from its real product capture."""
from __future__ import annotations

import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path("/home/lakshaya/projects/mosaic")
RAW = ROOT / "demo" / "raw" / "product"
RAW.mkdir(parents=True, exist_ok=True)
FILM = (ROOT / "demo" / "product-film.html").as_uri()
OUT = RAW / "film.webm"


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        context = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            record_video_dir=str(RAW),
            record_video_size={"width": 1920, "height": 1080},
        )
        page = context.new_page()
        page.goto(FILM, wait_until="load", timeout=30000)
        page.wait_for_function("() => window.__filmReady === true")
        page.wait_for_function("() => { const v=document.getElementById('reel'); return v && v.readyState >= 2; }", timeout=15000)
        page.evaluate("document.fonts.ready")
        page.wait_for_timeout(500)
        page.evaluate("window.__startFilm()")
        page.wait_for_timeout(26_400)
        video = page.video
        context.close()
        source = Path(video.path())
        shutil.copy2(source, OUT)
        browser.close()
    print(f"recorded {OUT} ({OUT.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())