from .command import command


@command(names=["gallery", "invite"], shorten=False)
async def gallery(context):
    homebase = context.config["homebase"]
    if homebase is None:
        return

    server = context.client.get_guild(homebase)
    invite = await server.text_channels[0].create_invite(max_age=3600, max_uses=1)
    return await context.message.author.send(
        content="**Templates Gallery**\nYou can browse the template gallery on my official server:\n%s" % invite.url
    )
