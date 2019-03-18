import discord

from .command import RenderTemplate


commands = [RenderTemplate]


def serve():
    client = discord.Client()
    owner = None

    @client.event
    async def on_ready():
        nonlocal owner
        owner = (await client.application_info()).owner
        print("Logged in with ID: %s" % client.user.id)
        print("Bot owner ID:      %s" % owner.id)
        print(message)
        print("-" * len(message), flush=True)

    @client.event
    async def on_message(message):
        if message.author == client.user or message.author != owner:
            return

        for command in commands:
            executed = await command.execute(client, message)
            if executed:
                print("=> %s" % command.__name__, flush=True)
                break

    print("Typewriter logging in...", flush=True)
    client.run("NTU2ODMwNjgyMjc4Nzg5MTIz.D2_dxQ._ntIZeqyXr8ooISU9oecC8dr_Ic")


if __name__ == "__main__":
    serve()
