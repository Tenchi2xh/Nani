import os
import math
import tempfile
from yattag import Doc

from .furigana import html_furigana


def resource_path(path):
    return "file://%s/resources/%s" % (os.path.dirname(__file__), path)


font_faces = """
    @font-face {
        font-family: "Manga Main";
        src: url(%s);
    }
    @font-face {
        font-family: "Manga Furigana";
        src: url(%s);
    }
""" % (resource_path("FOT-RodinWanpakuPro-EB.otf"), resource_path("yumin.ttf"))


class HtmlTemplate(object):
    def __init__(self, template, text):
        self.template = template
        self.text = text

    def __enter__(self):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False)
        self.path = f.name
        f.write(self.html)
        f.close()
        return self.path

    def __exit__(self, *args):
        os.remove(self.path)
        return

    @property
    def html(self):
        doc, tag, txt = Doc().tagtext()

        with tag("html"):
            with tag("head"):
                doc.stag("meta", charset="UTF-8")
                doc.stag("link", rel="stylesheet", href=resource_path("style.css"))
                with tag("style"):
                    txt(font_faces)
                    txt("body { background-image: url(%s); }" % self.template["image"])
            with tag("body"):
                bubble = self.template["bubbles"][0]
                style = "position: absolute; left: %d; top: %d; width: %dpx; height: %dpx;" % (
                    bubble["x"], bubble["y"], bubble["w"], bubble["h"]
                )
                font_size = self.optimal_font_size(bubble)
                line_height = font_size * 1.5
                with tag("div", style=style, klass="bubble"):
                    with tag("p", style="font-size: %fpx; line-height: %fpx;" % (font_size, line_height)):
                        doc.asis(html_furigana(self.text))

        return doc.getvalue()

    def optimal_font_size(self, bubble):
        x, y = bubble["w"], bubble["h"]
        n = len(self.text)

        # https://math.stackexchange.com/a/466248
        # We'll pretend our font characters are squares
        px = math.ceil(math.sqrt(n * x / y))
        if math.floor(px * y / x) * px < n:
            sx = y / math.ceil(px * y / x)
        else:
            sx = x / px
        py = math.ceil(math.sqrt(n * y / x))
        if math.floor(py * x / y) * py < n:
                sy = x / math.ceil(x * py / y)
        else:
                sy = y / py

        optimal_char_width = max(sx, sy)
        return optimal_char_width / 1.5  # Line height is 1.5x the char height
