import os
import random
import jaconv
from abc import ABC, abstractmethod

from .html import HtmlTemplate
from .util import resource_path, css_position
from ..furigana import html_reverse_furigana


def games_template(template):
    template_type = {
        "famicom-dragonquest": DragonQuestTemplate
    }

    return template_type.get(template["name"], None)


def random_wide(min, max):
    return jaconv.h2z(str(random.randint(min, max)), digit=True)


def get_image(template):
    if "images" in template:
        return resource_path(os.path.join(
            "templates",
            "games",
            random.choice(template["images"])
        ))
    else:
        return template["image"]


class ScaledTemplate(HtmlTemplate):
    def __init__(self, template, text, author, stylesheet_names, resources):
        super().__init__(
            template, text, author,
            stylesheet_names=["scaled.css.j2"] + stylesheet_names,
            resources={
                "bg": get_image(template),
                "width": template["w"] * template["scale"],
                "scale": template["scale"],
                **resources
            }
        )


class FamicomTemplate(ScaledTemplate):
    def __init__(self, template, text, author):
        super().__init__(
            template, text, author,
            stylesheet_names=["retro_game.css.j2"],
            resources={
                "font": resource_path("jackeyfont.ttf")
            }
        )
        self.author = author

    def body(self, doc, tag, txt):
        with tag("div", klass="screen"):
                with tag("div",
                         style=css_position(self.template["main"]),
                         klass="text"):
                    with tag("p"):
                        for line in self.lines:
                            doc.asis(html_reverse_furigana(line))
                            doc.asis("<br>")

                self.template_specific(doc, tag, txt)

    @abstractmethod
    def template_specific(self, doc, tag, txt):
        pass


class DragonQuestTemplate(FamicomTemplate):
    def template_specific(self, doc, tag, txt):
        with tag("div",
                 style=css_position(self.template["nickname"]),
                 klass="text"):
            with tag("p"):
                doc.asis(jaconv.h2z(self.author[:4].upper(), ascii=True, digit=True))

        with tag("div",
                 style=css_position(self.template["stats"]),
                 klass="text"):
            with tag("p"):
                doc.asis("""
                    <span style="clear: both; float: left">レベル</span><span style="float: right">%s</span>
                    <span style="clear: both; float: left">ＨＰ</span><span style="float: right">%s</span>
                    <span style="clear: both; float: left">ＭＰ</span><span style="float: right">%s</span>
                    <span style="clear: both; float: left">Ｇ</span><span style="float: right">%s</span>
                    <span style="clear: both; float: left">Ｅ</span><span style="float: right">%s</span>
                """.strip() % (
                    random_wide(1, 99),
                    random_wide(1, 999),
                    random_wide(1, 999),
                    random_wide(1, 9999),
                    random_wide(1, 9999),
                ))
