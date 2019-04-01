from .command import command
from .util import send_template
from .. import templates

@command(names=lambda: [category for category in templates.categories])
async def category(context):
    channel = context.message.channel
    template_name, text = context.arguments.split(maxsplit=2)

    category = context.command_name

    if template_name not in templates.categories[category]:
        return await channel.send("Template '%s-%s' not found." % (category, template_name))

    template = templates.categories[category][template_name]
    return await send_template(context, channel, template, text)
