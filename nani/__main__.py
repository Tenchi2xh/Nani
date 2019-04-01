import json
import discord
import configparser

from .commands import command_manager


def serve(config):
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

        is_self = message.author == client.user
        on_homebase = message.guild.id != config["homebase"]
        not_whitelisted = not config["blacklist"] and message.author.id not in config["whitelist"]
        blacklisted = message.author.id in config["blacklist"]

        if is_self or not on_homebase and (not_whitelisted or blacklisted):
            return

        await command_manager.execute(info, client, message, config)

    print("%s logging in..." % config["name"])
    client.run(config["token"])


def main():
    config = configparser.ConfigParser()
    config.read("nani.conf")
    config = config["nani"]

    def load_list(name):
        if name in config:
            raw_lst = config[name]
            if raw_lst == "*":
                lst = []
            else:
                lst = json.loads(raw_lst)
            assert isinstance(lst, list)
            return lst
        return []

    def load_optional_int(name):
        raw_value = config.get(name, None)
        if raw_value is not None:
            return int(raw_value)

    config_dict = {
        "whitelist": load_list("whitelist"),
        "blacklist": load_list("blacklist"),
        "token": config["token"],
        "name": config["name"],
        "prefix": config.get("prefix", "."),
        "homebase": load_optional_int("homebase"),
    }

    serve(config_dict)


if __name__ == "__main__":
    main()
