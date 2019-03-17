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
                with tag("div", style=style, klass="bubble"):
                    with tag("p", style="line-height: 1.5"):
                        doc.asis(html_furigana(self.text))

                with tag("script", src="https://s3-us-west-2.amazonaws.com/s.cdpn.io/3/textFit.js"):
                    pass
                with tag("script"):
                    txt("""
                        document.querySelectorAll(".bubble").forEach(textFit);
                    """)

        return doc.getvalue()
