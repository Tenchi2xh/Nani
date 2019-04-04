import random
from datetime import datetime
from num2words import num2words

from .html import HtmlTemplate
from .util import resource_path, css_position


class CalligraphyTemplate(HtmlTemplate):
    def __init__(self, template, text, author):
        super().__init__(
            template, text, author,
            stylesheet_names=["calligraphy.css.j2"],
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
        if len(self.lines) == 1:
            self.lines = [""] + self.lines
        self.lines = self.lines[:2] + [signature]

    def body(self, doc, tag, txt):
        parts = ["title", "main", "signature"]

        with tag("div", klass="scroll"):
            for i, part in enumerate(parts):

                text = ""
                if i < len(self.lines):
                    text = self.lines[i]

                with tag("div",
                         style=css_position(self.template[part]),
                         klass="text fit %s" % part):
                    with tag("p"):
                        doc.asis(text)
