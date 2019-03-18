import os
import discord

from . import templates
from .render import render


command_names = [".meme", ".m", ".template", ".t"]


class RenderTemplate(object):
    @staticmethod
    async def execute(client, message):
        if any(message.content.startswith(n + " ") for n in command_names):

            _, template_name, text = message.content.split(maxsplit=2)

            if template_name not in templates.keys():
                await message.channel.send("Template '%s' not found." % template_name)

            template = templates[template_name]
            path = render(template, text)
            await message.channel.send(file=discord.File(path))
            os.remove(path)

            return True
