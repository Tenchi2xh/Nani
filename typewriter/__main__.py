import discord

from .command import execute


def serve():
    client = discord.Client()
    owner = None

    @client.event
    async def on_ready():
        nonlocal owner
        owner = (await client.application_info()).owner
        print("Bot ID:   %s" % client.user.id)
        print("Owner ID: %s" % owner.id)
        print("-" * 28, flush=True)

    @client.event
    async def on_message(message):
        if message.author == client.user or message.author != owner:
            return
        await execute(client, message)

    print("Typewriter logging in...", flush=True)
    client.run("NTU2ODMwNjgyMjc4Nzg5MTIz.D2_dxQ._ntIZeqyXr8ooISU9oecC8dr_Ic")


if __name__ == "__main__":
    serve()
