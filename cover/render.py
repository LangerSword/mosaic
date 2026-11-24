from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path('/home/lakshaya/projects/mosaic')
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-gpu'])
    page = browser.new_page(viewport={'width': 1200, 'height': 600}, device_scale_factor=1)
    page.goto((ROOT / 'cover/catalog.html').as_uri(), wait_until='networkidle')
    page.evaluate('document.fonts.ready')
    page.wait_for_timeout(300)
    page.screenshot(path=str(ROOT / 'docs/banner.png'), full_page=False)
    print(page.evaluate('({w: document.documentElement.scrollWidth, h: document.documentElement.scrollHeight})'))
    browser.close()
print(ROOT / 'docs/banner.png')
