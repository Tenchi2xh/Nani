from .manga import MangaTemplate
from .calligraphy import CalligraphyTemplate
from .games import games_template


def html_template(template, text, author):
    template_types = {
        "manga": MangaTemplate,
        "calligraphy": CalligraphyTemplate,
        "games": games_template(template),
    }

    return template_types[template["type"]](template, text, author)
