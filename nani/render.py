import atexit
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .html import html_template

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--high-dpi-support=1")
driver = webdriver.Chrome(options=chrome_options)
atexit.register(driver.quit)


def render(template, text, author):
    with html_template(template, text, author) as html_path:
        driver.set_window_size(template["w"], template["h"])
        driver.get("file://%s" % html_path)

        f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        f.close()
        driver.save_screenshot(f.name)
        return f.name
