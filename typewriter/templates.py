import os
import json


def read_templates():
    templates_path = os.path.join(os.path.dirname(__file__), "resources", "templates")
    templates = {}

    template_types = [f for f in os.listdir(templates_path) if os.path.isdir(os.path.join(templates_path, f))]
    for template_type in template_types:
        path = os.path.join(templates_path, template_type)
        json_files = [f for f in os.listdir(path) if f.endswith(".json")]
        for j in json_files:
            with open(os.path.join(templates_path, template_type, j)) as f:
                template = json.load(f)
            name = j[:-5]
            template["image"] = os.path.join(templates_path, template_type, name + ".png")
            template["name"] = name
            template["type"] = template_type
            templates[name] = template

    return templates


def categorize(templates):
    categories = {}
    for full_name, template in templates.items():
        if "-" not in full_name:
            category = "misc"
            name = full_name
        else:
            category, name = full_name.split("-", 1)
        if category not in categories:
            categories[category] = {}
        categories[category][name] = template
    return categories


templates = read_templates()
categories = categorize(templates)
