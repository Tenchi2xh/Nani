import re
import discord
from num2words import num2words

from .. import templates
from .command import command
from .util import send_template, circled_numbers


@command(shorten=False)
async def refresh(context):
    if context.message.author != context.info.owner:
        return

    templates.refresh()

    homebase = context.config["homebase"]
    bot_name = context.config["name"]

    if homebase is None:
        return
    server = context.client.get_guild(homebase)

    category_format = re.compile(r"^\[(%s)\]\s.+$" % bot_name)

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
        discord_categories[category_name] = await server.create_category(
            "[%s] %s" % (bot_name, category_name),
            overwrites=overwrites
        )

    for category in templates.categories:
        category_type = list(templates.categories[category].values())[0]["type"]

        channel = await discord_categories[category_type.capitalize()].create_text_channel(
            name=category
        )
        short_command = context.manager.get_command(category)[2]
        await channel.send(
            "**%s templates**\nUsage: `.%s [template] [lines]` or `.%s [template] [lines]`:"
            % (category.capitalize(), short_command, category)
        )

        for i, (template_name, template) in enumerate(templates.categories[category].items()):
            await send_template(
                context,
                channel,
                template,
                samples[category_type],
                msg="%s `.%s %s [lines]`:" % (
                    circled_numbers[i + 1],
                    short_command,
                    template_name
                )
            )
