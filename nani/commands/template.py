from .command import command
from .util import send_template
from .. import templates


@command()
async def template(context):
    channel = context.message.channel
    template_name, text = context.arguments.split(maxsplit=2)

    if template_name not in templates.templates.keys():
        return await channel.send("Template '%s' not found." % template_name)

    template = templates.templates[template_name]
    return await send_template(context, channel, template, text)
