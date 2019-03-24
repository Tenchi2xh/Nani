import json
import discord
import configparser

from .command import execute


def serve(token, whitelist, blacklist):
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
        if (message.author == client.user
            or not blacklist and message.author.id not in whitelist
            or message.author.id in blacklist):
            return
        await execute(info, client, message)

    print("Typo logging in...", flush=True)
    client.run(token)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("typo.conf")

    def load_list(name):
        if name in config["typo"]:
            raw_lst = config["typo"][name]
            if raw_lst == "*":
                lst = []
            else:
                lst = json.loads(raw_lst)
            assert isinstance(lst, list)
            return lst
        return []

    whitelist = load_list("whitelist")
    blacklist = load_list("blacklist")
    token = config["typo"]["token"]

    serve(token, whitelist, blacklist)
