import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .html import HtmlTemplate

chrome_options = Options()
chrome_options.add_argument("--headless")


def render(template, text):
    with HtmlTemplate(template, text) as html_path:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(template["w"], template["h"])
        driver.get("file://%s" % html_path)

        f = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        f.close()
        driver.save_screenshot(f.name)
        return f.name


if __name__ == "__main__":
    from . import templates
    #print(render(templates["yotsuba-gun"], "ここは細菌禁止。逮捕する…‼︎"))
    print(render(templates["yotsuba-gun"], "何⁉️"))
