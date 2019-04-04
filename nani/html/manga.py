from .html import HtmlTemplate
from .util import resource_path, css_position
from ..furigana import html_furigana


class MangaTemplate(HtmlTemplate):
    def __init__(self, template, text, author):
        super().__init__(
            template, text, author,
            stylesheet_names=["manga.css.j2"],
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
