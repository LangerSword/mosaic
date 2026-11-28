#!/usr/bin/env python3
"""Record one clean clip per working forge component on the Mosaic site."""
from __future__ import annotations

import shutil
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path("/home/lakshaya/projects/mosaic/demo/raw/components")
URL = "http://127.0.0.1:4322/#lab"


def cursor(context) -> None:
    context.add_init_script(
        "window.addEventListener('DOMContentLoaded',()=>{"
        "const c=document.createElement('div');"
        "c.style.cssText='position:fixed;left:-100px;top:-100px;width:18px;height:18px;border:1px solid #c64a2e;border-radius:50%;z-index:999999;pointer-events:none;transform:translate(-50%,-50%);box-shadow:0 0 0 1px rgba(10,11,10,.35)';"
        "document.body.appendChild(c);"
        "window.addEventListener('pointermove',e=>{c.style.left=e.clientX+'px';c.style.top=e.clientY+'px';});"
        "});"
    )


def shot(browser, name: str, body) -> None:
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=str(OUT),
        record_video_size={"width": 1920, "height": 1080},
    )
    cursor(context)
    page = context.new_page()
    page.goto(URL, wait_until="load", timeout=30000)
    page.wait_for_timeout(900)
    body(page)
    page.wait_for_timeout(500)
    video = page.video
    context.close()
    src = Path(video.path())
    dest = OUT / f"{name}.webm"
    shutil.copy2(src, dest)
    print(name, dest.stat().st_size // 1024, "KB")


def scroll_panel(page, selector: str, offset: int = -120) -> None:
    page.locator(selector).first.scroll_into_view_if_needed()
    page.wait_for_timeout(350)
    page.evaluate(f"window.scrollBy(0, {offset})")
    page.wait_for_timeout(350)


def bounds(page, selector: str) -> dict:
    return page.locator(selector).first.evaluate(
        "el => { const r=el.getBoundingClientRect(); return {x:r.x,y:r.y,w:r.width,h:r.height}; }"
    )


def paper(page) -> None:
    scroll_panel(page, "mosaic-paper-plane")
    b = bounds(page, "mosaic-paper-plane button")
    page.mouse.move(b["x"] + b["w"] / 2, b["y"] + b["h"] / 2)
    page.wait_for_timeout(250)
    page.locator("mosaic-paper-plane button").click()
    page.wait_for_timeout(3000)


def swipe(page) -> None:
    scroll_panel(page, "mosaic-swipe-confirm")
    el = page.locator("mosaic-swipe-confirm").first
    geo = el.evaluate(
        "el => { const h=el.shadowRoot.querySelector('.handle').getBoundingClientRect();"
        " const t=el.shadowRoot.querySelector('.track').getBoundingClientRect();"
        " return {x:h.x+h.width/2,y:h.y+h.height/2,w:t.width}; }"
    )
    page.mouse.move(geo["x"], geo["y"])
    page.mouse.down()
    page.mouse.move(geo["x"] + geo["w"] * 0.9, geo["y"], steps=15)
    page.mouse.up()
    page.wait_for_timeout(900)


def ring(page) -> None:
    scroll_panel(page, "[data-demo-download]")
    b = bounds(page, "[data-demo-download]")
    for _ in range(5):
        page.mouse.click(b["x"] + b["w"] / 2, b["y"] + b["h"] / 2)
        page.wait_for_timeout(240)
    page.wait_for_timeout(900)


def checklist(page) -> None:
    scroll_panel(page, "mosaic-checklist")
    page.locator("mosaic-checklist input").nth(1).check()
    page.wait_for_timeout(300)
    page.locator("mosaic-checklist input").nth(2).check()
    page.wait_for_timeout(800)


def pointer(page) -> None:
    scroll_panel(page, "mosaic-magnetic-link")
    b = bounds(page, "mosaic-magnetic-link")
    page.mouse.move(b["x"] + b["w"] / 2 - 90, b["y"] + b["h"] / 2)
    page.mouse.move(b["x"] + b["w"] / 2, b["y"] + b["h"] / 2, steps=18)
    page.wait_for_timeout(700)
    scroll_panel(page, "mosaic-cursor-lens")
    b = bounds(page, "mosaic-cursor-lens")
    page.mouse.move(b["x"] + b["w"] / 2 - 70, b["y"] + b["h"] / 2 - 20)
    page.mouse.move(b["x"] + b["w"] / 2, b["y"] + b["h"] / 2, steps=18)
    page.wait_for_timeout(900)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
        shot(browser, "seg-paper", paper)
        shot(browser, "seg-swipe", swipe)
        shot(browser, "seg-ring", ring)
        shot(browser, "seg-checklist", checklist)
        shot(browser, "seg-pointer", pointer)
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())