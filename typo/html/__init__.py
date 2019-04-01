from .manga import MangaTemplate
from .calligraphy import CalligraphyTemplate


def html_template(template, text, author):
    template_types = {
        "manga": MangaTemplate,
        "calligraphy": CalligraphyTemplate,
    }

    return template_types[template["type"]](template, text, author)
