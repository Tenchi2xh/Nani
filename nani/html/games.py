import random
import jaconv

from .html import HtmlTemplate
from .util import resource_path, css_position
from ..furigana import html_reverse_furigana


def games_template(template):
    template_type = {
        "famicom-dragonquest": DragonQuestTemplate
    }

    return template_type.get(template["name"], None)


class DragonQuestTemplate(HtmlTemplate):
    def __init__(self, template, text, author):
        super().__init__(
            template, text, author,
            stylesheet_name="retro_game.css.j2",
            resources={
                "font": resource_path("jackeyfont.ttf"),
                "width": template["w"] * template["scale"],
                "scale": template["scale"]
            }
        )
        self.author = author

    def body(self, doc, tag, txt):
        def random_wide(min, max):
            return jaconv.h2z(str(random.randint(min, max)), digit=True)

        with tag("div", klass="screen"):
                with tag("div",
                         style=css_position(self.template["main"]),
                         klass="text"):
                    with tag("p"):
                        for line in self.lines:
                            doc.asis(html_reverse_furigana(line))
                            doc.asis("<br>")

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
