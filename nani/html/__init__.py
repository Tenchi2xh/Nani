from .manga import MangaTemplate
from .calligraphy import calligraphy_template
from .games import games_template


def html_template(template, text, author):
    template_types = {
        "manga": MangaTemplate,
        "calligraphy": calligraphy_template(template),
        "games": games_template(template),
    }

    return template_types[template["type"]](template, text, author)
