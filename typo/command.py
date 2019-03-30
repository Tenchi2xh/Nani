import re
import os
import discord
from PIL import Image
from num2words import num2words

from . import templates
from .render import render
from .util import circled_numbers

max_file_size = 2 * 1024 * 1024  # 2 MB

prefix = "."

template_command_names = ["t", "template"]
help_command_names = ["h", "help"]
refresh_command_names = ["refresh"]
non_template_commands = template_command_names + help_command_names + refresh_command_names


def refresh_category_commands():
    global category_commands, short_commands
    category_commands = {}
    short_commands = {}

    for category in templates.categories:
        for i in range(1, len(category)):
            short = category[:i]
            if short not in category_commands and short not in non_template_commands:
                category_commands[short] = templates.categories[category]
                short_commands[category] = short
                category_commands[category] = templates.categories[category]
                break

refresh_category_commands()


async def execute(info, client, message, homebase):
    content = message.content

    def is_command(names):
        if not content.strip():
            return False
        first_word = content.split()[0]
        return any(first_word == "%s%s" % (prefix, n) for n in names)

    async def send_template(channel, template, text, msg=None):
        print(
            "=> User %s is rendering template %s with text '%s'"
            % (message.author, template["name"], text),
            flush=True
        )
        path = render(template, text, message.author.display_name)

        if os.path.getsize(path) > max_file_size:
            print("Compressing large file", flush=True)
            image = Image.open(path)
            image = image.convert("RGB")
            path, old_path = path[:-3] + "jpg", path
            image.save(path)
            os.remove(old_path)

        await channel.send(file=discord.File(path), content=msg)
        os.remove(path)

    if is_command(template_command_names):
        _, template_name, text = content.split(maxsplit=2)
        if template_name not in templates.templates.keys():
            await message.channel.send("Template '%s' not found." % template_name)
            return
        template = templates.templates[template_name]
        return await send_template(message.channel, template, text)

    elif is_command(category_commands):
        command, short_template_name, text = content.split(maxsplit=2)
        command = command.lstrip(prefix)

        if short_template_name not in category_commands[command]:
            await message.channel.send("Template '%s-%s' not found." % (command, short_template_name))
            return

        template = category_commands[command][short_template_name]
        return await send_template(message.channel, template, text)

    elif is_command(help_command_names):
        embed = discord.Embed(
            title="Help for %s" % info.name,
            description="This bot can generate **manga panels** (and other templates).\n\nWhen generating templates with Japanese text, a language processor will annotate all *kanji* with **furigana**.\n\nThe command to generate a panel starts with a full stop, followed by the name of the category (the first letter is enough, for example `.y`). After the command name, specify the template name, and then the text to use.\n\nTry it out yourself:\n\n• `.yotsuba ask 何これ…？`\n• `.y gun 俺を誰だと思ってるんだ⁉️`\n• `.template yotsuba-pray ご馳走様〜！`\n\nTemplates denoted with a number contains that amount of speech bubbles. To fill them, each bubble must be provided on a separate line (Shift + Enter on desktop, carriage return on mobile). For example:\n\n```.gintama revolt This is bubble 1.\nAnd this is bubble 2!```\n\n**Available categories:**"
        )
        embed.set_thumbnail(url="https://i.imgur.com/mzYNzSN.png")

        categories = templates.categories

        for category in categories:
            names = []
            for template_name in categories[category]:
                name = "`%s`" % template_name
                if "bubbles" in categories[category][template_name]:
                    elements = len(categories[category][template_name]["bubbles"])
                else:
                    elements = categories[category][template_name]["elements"]
                if elements > 1:
                    name += " (%d)" % elements
                names.append(name)

            embed.add_field(
                name="%s (`.%s`, `.%s`):" % (category.capitalize(), short_commands[category], category),
                value=", ".join(names),
                inline=True
            )
        return await message.channel.send(embed=embed)

    elif is_command(refresh_command_names):
        if message.author != info.owner:
            return

        templates.refresh()
        refresh_category_commands()

        if not homebase:
            return

        server = client.get_guild(homebase)
        category_format = re.compile(r"^\[Typo\]\s.+$")

        for discord_category in server.categories:
            if category_format.match(discord_category.name):
                for channel in discord_category.channels:
                    await channel.delete(reason="Refreshing template galleries")
                await discord_category.delete(reason="Refreshing template galleries")

        overwrites = {
            server.default_role: discord.PermissionOverwrite(
                send_messages=False,
                add_reactions=False,
                attach_files=False,
            ),
        }

        category_names = ["Manga", "Calligraphy"]
        samples = {
            "manga": "\n".join(["何⁉【%s】" % num2words(i + 1, lang="ja") for i in range(10)]),
            "calligraphy": "書道の巻物を作るボット\n誤字"
        }


        discord_categories = {}
        for category_name in category_names:
            discord_categories[category_name] = await server.create_category("[Typo] %s" % category_name, overwrites=overwrites)

        for category in templates.categories:
            category_type = list(templates.categories[category].values())[0]["type"]

            channel = await discord_categories[category_type.capitalize()].create_text_channel(
                name=category
            )
            await channel.send(
                "**%s templates**\nUsage: `.%s [template] [lines]` or `.%s [template] [lines]`:"
                % (category.capitalize(), short_commands[category], category)
            )

            for i, (template_name, template) in enumerate(templates.categories[category].items()):
                await send_template(
                    channel,
                    template,
                    samples[category_type],
                    msg="%s `.%s %s [lines]`:" % (
                        circled_numbers[i + 1],
                        short_commands[category],
                        template_name
                    )
                )
