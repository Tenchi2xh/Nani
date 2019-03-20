import os
import math
import tempfile
from yattag import Doc
from jinja2 import Template

from .furigana import html_furigana


def resource_path(path, file_protocol=True):
    protocol = "file://" if file_protocol else ""
    return "%s%s/resources/%s" % (protocol, os.path.dirname(__file__), path)


resources = {
    "font": {
        "main": resource_path("FOT-RodinWanpakuPro-EB.otf"),
        "furigana": resource_path("yumin.ttf")
    },
    "texture": resource_path("texture.png")
}

with open(resource_path("style.css.j2", file_protocol=False)) as f:
    stylesheet_template = Template(f.read())


class HtmlTemplate(object):
    def __init__(self, template, text):
        self.template = template
        self.lines = [l.strip() for l in text.split("\n") if l.strip()]

    def __enter__(self):
        self.stylesheet = self.css()
        self.path = self.html()
        return self.path

    def __exit__(self, *args):
        os.remove(self.path)
        os.remove(self.stylesheet)
        return

    def css(self):
        stylesheet = stylesheet_template.render(
            image="file://" + self.template["image"],
            **resources
        )

        f = tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False)
        f.write(stylesheet)
        return f.name

    def html(self):
        doc, tag, txt = Doc().tagtext()

        with tag("html"):
            with tag("head"):
                doc.stag("meta", charset="UTF-8")
                doc.stag("link", rel="stylesheet", href=self.stylesheet)

            with tag("body"):
                for i, bubble in enumerate(self.template["bubbles"]):
                    text = ""
                    if i < len(self.lines):
                        text = self.lines[i]
                    style = "left: %d; top: %d; width: %dpx; height: %dpx;" % (
                        bubble["x"], bubble["y"], bubble["w"], bubble["h"]
                    )
                    with tag("div", style=style, klass="bubble"):
                        with tag("p"):
                            doc.asis(html_furigana(text))

                with tag("script", src=resource_path("textFit.js")):
                    pass
                with tag("script"):
                    txt("document.querySelectorAll('.bubble').forEach(textFit);")

        f = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False)
        f.write(doc.getvalue())
        return f.name
