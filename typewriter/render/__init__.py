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
        templates[name] = template

    return templates


templates = read_templates()
