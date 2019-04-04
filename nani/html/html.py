import os
import tempfile
from yattag import Doc
from jinja2 import Template
from abc import ABC, abstractmethod

from .util import resource_path


class HtmlTemplate(ABC):
    def __init__(self, template, text, author, stylesheet_names, resources):
        self.template = template
        self.lines = [l.strip() for l in text.split("\n") if l.strip()]
        self.author = author
        self.stylesheet_names = stylesheet_names
        self.resources = resources

    def __enter__(self):
        self.stylesheet = self.css()
        self.path = self.html()
        return self.path

    def __exit__(self, *args):
        # os.system("open file://%s" % self.path)
        os.remove(self.path)
        os.remove(self.stylesheet)
        return

    def css(self):
        sheets = []
        if isinstance(self.stylesheet_names, str):
            sheets.append(self.stylesheet_names)
        else:
            sheets.extend(self.stylesheet_names)

        template_aggregate = ""
        for sheet in sheets:
            with open(resource_path(sheet, file_protocol=False)) as f:
                template_aggregate += f.read() + "\n"
        stylesheet_template = Template(template_aggregate)

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
