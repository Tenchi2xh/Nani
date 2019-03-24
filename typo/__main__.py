import discord

from .command import execute


def serve():
    client = discord.Client(activity=discord.Game("Manga editor! Type .help"))
    info = None

    @client.event
    async def on_ready():
        nonlocal info
        info = await client.application_info()
        print("Bot ID:   %s" % client.user.id)
        print("Owner ID: %s" % info.owner.id)
        print("-" * 28, flush=True)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        await execute(info, client, message)

    print("Typewriter logging in...", flush=True)
    client.run("NTU2ODMwNjgyMjc4Nzg5MTIz.D2_dxQ._ntIZeqyXr8ooISU9oecC8dr_Ic")


if __name__ == "__main__":
    serve()
