import os
import discord

from .templates import templates, categories
from .render import render

prefix = "."
command_names = ["t", "template"]
category_commands = {}

for category in categories:
    for i in range(1, len(category)):
        if category[:i] not in category_commands:
            category_commands[category[:i]] = categories[category]
            category_commands[category] = categories[category]
            break


async def execute(client, message):
    content = message.content

    if any(content.startswith("%s%s " % (prefix, n)) for n in command_names):
        _, template_name, text = content.split(maxsplit=2)
        if template_name not in templates.keys():
            await message.channel.send("Template '%s' not found." % template_name)
            return
        template = templates[template_name]

    elif any(content.startswith("%s%s " % (prefix, n)) for n in category_commands):
        command, short_template_name, text = content.split(maxsplit=2)
        command = command.lstrip(prefix)

        if short_template_name not in category_commands[command]:
            await message.channel.send("Template '%s-%s' not found." % (command, short_template_name))
            return

        template = category_commands[command][short_template_name]
    else:
        return

    print(
        "=> User %s is rendering template %s with text '%s'"
        % (message.author, template["name"], text),
        flush=True
    )

    path = render(template, text)
    await message.channel.send(file=discord.File(path))
    os.remove(path)
