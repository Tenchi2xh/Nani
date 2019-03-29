#!/usr/bin/env python3

import os
import json
import click
import numpy
from PIL import Image
import matplotlib.pyplot as plot
from matplotlib.widgets import RectangleSelector

plot.switch_backend("Qt4Agg")


def bubble_selector(image_path):
    image = Image.open(image_path)
    width, height = image.size

    figure = plot.imshow(numpy.asarray(image))
    figure.axes.get_xaxis().set_visible(False)
    figure.axes.get_yaxis().set_visible(False)

    bubbles = []

    def onselect(event0, event1):
        x0, x1 = sorted([event0.xdata, event1.xdata])
        y0, y1 = sorted([event0.ydata, event1.ydata])
        bubbles.append({
            "x": int(x0),
            "y": int(y0),
            "w": int(x1 - x0),
            "h": int(y1 - y0),
        })

    RectangleSelector(figure.axes, onselect)

    manager = plot.get_current_fig_manager()
    manager.resize(width, height)
    plot.show()

    return {
        "w": width,
        "h": height,
        "bubbles": bubbles
    }


@click.command()
@click.argument("image_path", type=click.Path(exists=True))
def add_manga(image_path):
    file_name = os.path.basename(image_path)
    base_path = os.path.join("typo", "resources", "templates", "manga")
    dest = os.path.join(base_path, file_name)
    data_dest = os.path.join(base_path, "%s.json" % os.path.splitext(file_name)[0])

    if os.path.isfile(dest):
        raise click.UsageError("Template already exists: '%s'" % dest)

    data = bubble_selector(image_path)
    os.rename(file_name, dest)
    with open(data_dest, "w") as f:
        json.dump(data, f, indent=4)


if __name__ == "__main__":
    add_manga()
