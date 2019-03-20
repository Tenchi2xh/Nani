import os
import discord

from .templates import templates, categories
from .render import render

prefix = "."
template_command_names = ["t", "template"]
help_command_names = ["h", "help"]
category_commands = {}

for category in categories:
    for i in range(1, len(category)):
        if category[:i] not in category_commands:
            category_commands[category[:i]] = categories[category]
            category_commands[category] = categories[category]
            break



async def execute(info, client, message):
    content = message.content

    def is_command(names):
        return any(content.startswith("%s%s" % (prefix, n)) for n in names)

    async def send_template(template, text):
        print(
            "=> User %s is rendering template %s with text '%s'"
            % (message.author, template["name"], text),
            flush=True
        )
        path = render(template, text)
        await message.channel.send(file=discord.File(path))
        os.remove(path)

    if is_command(template_command_names):
        _, template_name, text = content.split(maxsplit=2)
        if template_name not in templates.keys():
            await message.channel.send("Template '%s' not found." % template_name)
            return
        template = templates[template_name]
        return await send_template(template, text)

    elif is_command(category_commands):
        command, short_template_name, text = content.split(maxsplit=2)
        command = command.lstrip(prefix)

        if short_template_name not in category_commands[command]:
            await message.channel.send("Template '%s-%s' not found." % (command, short_template_name))
            return

        template = category_commands[command][short_template_name]
        return await send_template(template, text)

    elif is_command(help_command_names):
        embed = discord.Embed(
            title="Help for %s" % info.name,
            description="This bot can generate **manga panels** (and other templates).\n\nWhen generating templates with Japanese text, a language processor will annotate all *kanji* with **furigana**.\n\nThe command to generate a panel starts with a full stop, followed by the name of the category (the first letter is enough, for example `.y`). After the command name, specify the template name, and then the text to use.\n\nTry it out yourself:\n\n• `.yotsuba ask 何これ…？`\n• `.y gun 俺を誰だと思ってるんだ⁉️`\n• `.template yotsuba-pray ご馳走様〜！`\n\nTemplates denoted with a number contains that amount of speech bubbles. To fill them, each bubble must be provided on a separate line (Shift + Enter on desktop, carriage return on mobile). For example:\n\n```.gintama revolt This is bubble 1.\nAnd this is bubble 2!```\n\n**Available categories:**"
        )
        embed.set_thumbnail(url="https://i.imgur.com/mzYNzSN.png")
        for category in categories:
            names = []
            for template_name in categories[category]:
                name = "`%s`" % template_name
                bubbles = len(categories[category][template_name]["bubbles"])
                if bubbles > 1:
                    name += " (%d)" % bubbles
                names.append(name)

            embed.add_field(
                name="%s (`.%s`, `.%s`):" % (category.capitalize(), category[0], category),
                value=", ".join(names),
                inline=True
            )
        await message.channel.send(embed=embed)

        return
