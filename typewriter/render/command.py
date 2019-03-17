from ..commands import Command


command_names = [".meme", ".m", ".template", ".t"]

class RenderTemplate(Command):
    @staticmethod
    async def execute(client, message):
        if any(message.content.startswith(n + " ") for n in command_names):
            await message.channel.send("Hello")
            return True
