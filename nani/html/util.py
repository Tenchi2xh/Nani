import os
from .. import __file__ as root_module


def resource_path(path, file_protocol=True):
    protocol = "file://" if file_protocol else ""
    return "%s%s/resources/%s" % (protocol, os.path.dirname(root_module), path)


def css_position(box):
    return "left: %d; top: %d; width: %dpx; height: %dpx;" % (
        box["x"], box["y"], box["w"], box["h"]
    )
