import os
import math
import random
import tempfile
from yattag import Doc
from jinja2 import Template
from datetime import datetime
from num2words import num2words
from abc import ABC, abstractmethod

from .furigana import html_furigana


def resource_path(path, file_protocol=True):
    protocol = "file://" if file_protocol else ""
    return "%s%s/resources/%s" % (protocol, os.path.dirname(__file__), path)


def css_position(box):
    return "left: %d; top: %d; width: %dpx; height: %dpx;" % (
        box["x"], box["y"], box["w"], box["h"]
    )

def html_template(template, text, author):
    template_types = {
        "manga": MangaTemplate,
        "calligraphy": CalligraphyTemplate,
    }

    return template_types[template["type"]](template, text, author)


class HtmlTemplate(ABC):
    def __init__(self, template, text, author, stylesheet_name, resources):
        self.template = template
        self.lines = [l.strip() for l in text.split("\n") if l.strip()]
        self.author = author
        self.stylesheet_name = stylesheet_name
        self.resources = resources

    def __enter__(self):
        self.stylesheet = self.css()
        self.path = self.html()
        return self.path

    def __exit__(self, *args):
        #os.system("open file://%s" % self.path)
        os.remove(self.path)
        os.remove(self.stylesheet)
        return

    def css(self):
        with open(resource_path(self.stylesheet_name, file_protocol=False)) as f:
            stylesheet_template = Template(f.read())

        stylesheet = stylesheet_template.render(
            image="file://" + self.template["image"],
            **self.resources
        )

        f = tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False)
        f.write(stylesheet)
        return f.name

    @abstractmethod
    def body(self, doc, tag, txt):
        pass

    def html(self):
        doc, tag, txt = Doc().tagtext()

        with tag("html"):
            with tag("head"):
                doc.stag("meta", charset="UTF-8")
                doc.stag("link", rel="stylesheet", href=self.stylesheet)

            with tag("body"):
                self.body(doc, tag, txt)

                with tag("script", src=resource_path("textFit.js")):
                    pass
                with tag("script", src=resource_path("doFit.js")):
                    pass

        f = tempfile.NamedTemporaryFile(mode="w", suffix=".html", delete=False)
        f.write(doc.getvalue())
        return f.name


class MangaTemplate(HtmlTemplate):
    def __init__(self, template, text, author):
        super().__init__(
            template, text, author,
            stylesheet_name="manga.css.j2",
            resources={
                "font": {
                    "main": resource_path("FOT-RodinWanpakuPro-EB.otf"),
                    "furigana": resource_path("yumin.ttf")
                },
                "texture": resource_path("texture.png")
            }
        )

    def body(self, doc, tag, txt):
        for i, bubble in enumerate(self.template["bubbles"]):
            text = ""
            if i < len(self.lines):
                text = self.lines[i]
            with tag("div", style=css_position(bubble), klass="bubble fit"):
                with tag("p"):
                    doc.asis(html_furigana(text))


class CalligraphyTemplate(HtmlTemplate):
    def __init__(self, template, text, author):
        super().__init__(
            template, text, author,
            stylesheet_name="calligraphy.css.j2",
            resources={
                "font": resource_path(template["font"]),
                "bg": resource_path("templates/calligraphy/%s" % template["bg"]),
                "fg": resource_path("templates/calligraphy/calligraphy-scroll-fg.png"),
                "hue": random.randint(0, 17) * 20
            }
        )
        now = datetime.now()
        signature = "%s　%s年%s月%s日　天地" % (
            self.author,
            num2words(now.year, lang="ja"),
            num2words(now.month, lang="ja"),
            num2words(now.day, lang="ja")
        )
        self.lines = self.lines[:2] + [signature]

    def body(self, doc, tag, txt):
        parts = ["title", "main", "signature"]
        with tag("div", klass="scroll"):
            for i, part in enumerate(parts):
                text = ""
                if i < len(self.lines):
                    text = self.lines[i]
                with tag("div", style=css_position(self.template[part]), klass="text fit %s" % part):
                    with tag("p"):
                        doc.asis(text)
