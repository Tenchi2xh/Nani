import os
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


def generate_html(text):
    doc, tag, txt = Doc().tagtext()

    with tag("html"):
        with tag("head"):
            doc.stag("meta", charset="UTF-8")
            doc.stag("link", rel="stylesheet", href=resource_path("style.css"))
            with tag("style"):
                txt(font_faces)
        with tag("body"):
            # wrap in div for the text zone (absolute, px)
            with tag("p"):
                doc.asis(html_furigana(text))

    return doc.getvalue()


class HtmlTemplate(object):
    def __init__(self, template, text):
        self.template = template
        self.text = text

    def __enter__(self):
        f = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False)
        self.path = f.name
        f.write(generate_html(self.text))
        f.close()
        return self.path

    def __exit__(self, *args):
        os.remove(self.path)
        return
