import os
import json


def read_templates():
    resources = os.path.join(os.path.dirname(__file__), "resources", "templates")
    templates = {}
    json_files = [f for f in os.listdir(resources) if f.endswith(".json")]
    for j in json_files:
        with open(os.path.join(resources, j)) as f:
            template = json.load(f)
        name = j[:-5]
        template["image"] = os.path.join(resources, name + ".png")
        template["name"] = name
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
