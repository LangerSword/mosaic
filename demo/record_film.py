#!/usr/bin/env python3
"""Record the kinetic intro and end card for the Mosaic demo."""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path('/home/lakshaya/projects/mosaic')
RAW = ROOT / 'demo' / 'raw'
RAW.mkdir(parents=True, exist_ok=True)


def record(browser, html: str, seconds: float, out: Path, has_clock: bool) -> None:
    context = browser.new_context(
        viewport={'width': 1920, 'height': 1080},
        record_video_dir=str(RAW),
        record_video_size={'width': 1920, 'height': 1080},
    )
    page = context.new_page()
    page.goto((ROOT / 'demo' / html).as_uri(), wait_until='load')
    page.evaluate('document.fonts.ready')
    if has_clock:
        page.wait_for_function('window.__filmReady === true', timeout=10000)
        page.evaluate('window.__startFilm()')
    page.wait_for_timeout(int(seconds * 1000))
    video = page.video
    context.close()
    source = Path(video.path())
    shutil.copy2(source, out)
    print(f'wrote {out} ({out.stat().st_size // 1024} KB)')


def main() -> int:
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--allow-file-access-from-files', '--no-sandbox', '--disable-dev-shm-usage'],
        )
        record(browser, 'kinetic.html', 8.35, RAW / 'kinetic.webm', True)
        record(browser, 'endcard.html', 8.35, RAW / 'endcard.webm', False)
        browser.close()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
