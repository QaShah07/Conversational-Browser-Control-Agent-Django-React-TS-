import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

class BrowserController:
    def __init__(self, conv_id:str, screenshot_dir:Path):
        self.conv_id = conv_id
        self.sdir = screenshot_dir
        self.page = None
        self.browser = None
        self.pw = None

    def launch(self, headless=True):
        self.pw = sync_playwright().start()
        self.browser = self.pw.chromium.launch(headless=headless)
        ctx = self.browser.new_context()
        self.page = ctx.new_page()

    def snap(self, tag:str):
        self.sdir.mkdir(parents=True, exist_ok=True)
        path = self.sdir / f"{int(time.time()*1000)}_{tag}.png"
        self.page.screenshot(path=str(path), full_page=True)
        return str(path)

    def goto(self, url:str):
        self.page.goto(url, wait_until='networkidle')
        return self.snap('goto')

    def fill(self, selector:str, text:str):
        self.page.fill(selector, text)
        return self.snap('fill')

    def click(self, selector:str):
        self.page.click(selector)
        return self.snap('click')

    def wait_for(self, selector:str, timeout=15000):
        self.page.wait_for_selector(selector, timeout=timeout)
        return self.snap('wait')

    def close(self):
        if self.browser:
            self.browser.close()
        if self.pw:
            self.pw.stop()