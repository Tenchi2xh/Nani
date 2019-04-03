import atexit
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

from .html import html_template

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--hide-scrollbars")
chrome_options.add_argument("--force-device-scale-factor=1")
chrome_options.add_argument("--high-dpi-support=1")
driver = webdriver.Chrome(options=chrome_options)
atexit.register(lambda: driver.quit)


def render(template, text, author):
    with html_template(template, text, author) as html_path:
        check_session()
        scale = template["scale"] if "scale" in template else 1
        driver.set_window_size(template["w"] * scale, template["h"] * scale)
        driver.get("file://%s" % html_path)

        f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        f.close()
        driver.save_screenshot(f.name)
        return f.name


def check_session():
    global driver
    try:
        driver.title
    except WebDriverException:
        driver = webdriver.Chrome(options=chrome_options)
