#!/usr/bin/env python3
"""Record the live Mosaic site at 1920x1080 for the 60s demo."""
from __future__ import annotations

import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path('/home/lakshaya/projects/mosaic')
RAW = ROOT / 'demo' / 'raw'
RAW.mkdir(parents=True, exist_ok=True)
OUT = RAW / 'ui.webm'
PORT = 4180
URL = f'http://127.0.0.1:{PORT}/'

CURSOR = r"""
() => {
  if (window.__mosaicCursor) return;
  window.__mosaicCursor = true;
  const c = document.createElement('div');
  c.id = 'mosaic-demo-cursor';
  c.innerHTML = '<svg width="30" height="30" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M5 3L19 12L12 13L9 20L5 3Z" fill="#f3efe6" stroke="#15130f" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  c.style.cssText = 'position:fixed;left:0;top:0;z-index:999999;pointer-events:none;width:30px;height:30px;filter:drop-shadow(1px 2px 3px rgba(0,0,0,.35));transition:left .11s ease,top .11s ease';
  document.body.appendChild(c);
  document.addEventListener('mousemove', (e) => {
    const x = Math.min(innerWidth - 34, Math.max(0, e.clientX));
    const y = Math.min(innerHeight - 34, Math.max(0, e.clientY));
    c.style.left = x + 'px'; c.style.top = y + 'px';
  });
}
"""


def wait_server(url: str) -> None:
    for _ in range(80):
        try:
            if urllib.request.urlopen(url, timeout=1).status == 200:
                return
        except Exception:
            time.sleep(.1)
    raise RuntimeError('local site did not start')


def glide_to(page, selector: str, wait: int = 1200) -> None:
    page.evaluate("(s) => document.querySelector(s)?.scrollIntoView({behavior:'smooth', block:'start'})", selector)
    page.wait_for_timeout(wait)


def main() -> int:
    server = subprocess.Popen(
        [sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1',
         '--directory', str(ROOT / 'site')],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        wait_server(URL)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                record_video_dir=str(RAW),
                record_video_size={'width': 1920, 'height': 1080},
            )
            page = context.new_page()
            page.goto(URL, wait_until='networkidle', timeout=30000)
            page.evaluate('document.fonts.ready')
            page.evaluate(CURSOR)
            page.wait_for_timeout(1200)

            # Hero: let the type land, then move toward the forge.
            page.mouse.move(930, 500, steps=24)
            page.wait_for_timeout(800)
            glide_to(page, '#forge', 1500)
            page.mouse.move(1180, 480, steps=20)

            # Forge playground: choose Svelte and GSAP, then read the real files.
            page.select_option('#forge-stack', 'svelte')
            page.wait_for_timeout(400)
            page.select_option('#forge-motion', 'gsap')
            page.wait_for_timeout(900)
            page.mouse.move(1280, 430, steps=16)
            page.wait_for_timeout(1200)
            glide_to(page, '#forge-lab', 1400)

            # Forge lab: send, swipe, and advance the ring.
            paper = page.locator('mosaic-paper-plane')
            paper.evaluate("el => { const b=el.shadowRoot.querySelector('button'); if(b) b.click(); }")
            page.mouse.move(760, 610, steps=16)
            page.wait_for_timeout(1800)
            ring = page.locator('mosaic-download-ring')
            for _ in range(2):
                page.locator('[data-demo-download]').click()
                page.wait_for_timeout(300)
            ring.evaluate("el => el.progress = 60")
            page.mouse.move(1240, 680, steps=16)
            page.wait_for_timeout(1300)

            # Taste lab: switch the brief and read the candidates.
            glide_to(page, '#taste', 1400)
            page.select_option('#taste-brief', '1')
            page.wait_for_timeout(900)
            page.mouse.move(720, 540, steps=18)
            page.wait_for_timeout(1500)
            glide_to(page, '#components', 1400)
            page.mouse.move(1060, 530, steps=18)
            page.wait_for_timeout(1200)
            glide_to(page, '#install', 1500)
            page.mouse.move(960, 620, steps=18)
            page.wait_for_timeout(1200)

            video = page.video
            context.close()
            source = Path(video.path())
            if not source.exists():
                raise RuntimeError('Playwright did not produce a video')
            shutil.copy2(source, OUT)
            browser.close()
        print(f'recorded {OUT} ({OUT.stat().st_size // 1024} KB)')
        return 0
    finally:
        server.terminate()
        try:
            server.wait(timeout=4)
        except Exception:
            server.kill()


if __name__ == '__main__':
    raise SystemExit(main())
