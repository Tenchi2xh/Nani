import atexit
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .html import html_template

chrome_options = Options()
chrome_options.add_argument("--headless")
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


if __name__ == "__main__":
    from .templates import templates
    import os
    path = render(templates["yotsuba-ask"], "ここは細菌禁止。逮捕する…‼︎")
    #path = render(templates["yotsuba-gun"], "何⁉️")
    os.system("imgcat " + path)
    os.remove(path)
