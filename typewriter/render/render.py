from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from .html import HtmlTemplate

chrome_options = Options()
chrome_options.add_argument("--headless")


def render(template, text):
    with HtmlTemplate(template, text) as html_path:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_window_size(1024, 768)  # FIXME: Must be size of image
        driver.get("file://%s" % html_path)
        driver.save_screenshot("screen.png")


if __name__ == "__main__":
    render("", "様々な質問は編集室に投稿できます。個々の項目に関しては、それぞれの項目のノートページに書くこともできます。よくある質問の答えはｆａｑに載っているかもしれません。細菌禁止。")
