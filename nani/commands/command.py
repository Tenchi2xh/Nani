import time
import asyncio


class Context(object):
    def __init__(self, command_name, arguments, info, client, message, config, manager):
        self.command_name = command_name
        self.arguments = arguments
        self.info = info
        self.client = client
        self.message = message
        self.config = config
        self.manager = manager


class Command(object):
    def __init__(self, coroutine, names, shorten):
        self.names = names
        self.shorten = shorten
        self.coroutine = coroutine

    async def execute(self, context):
        return await self.coroutine(context)


def command(names=None, shorten=True):
    def decorator(coroutine):
        nonlocal names
        if names is None or not names:
            names = [coroutine.__name__]
        return Command(coroutine, names, shorten)
    return decorator


class CommandManager(object):
    def __init__(self):
        self.commands = []
        self.cooldowns = {}

    def add_command(self, command):
        self.commands.append(command)

    async def execute(self, info, client, message, config):
        parts = message.content.split(maxsplit=1)

        if not parts or not parts[0].startswith(config["prefix"]):
            return

        input_command_name = parts[0].lstrip(config["prefix"])
        arguments = "".join(parts[1:])

        command, command_name, _ = self.get_command(input_command_name)
        if not command:
            return

        context = Context(
            command_name=command_name,
            arguments=arguments,
            info=info,
            client=client,
            message=message,
            config=config,
            manager=self,
        )

        print("=> User %s is requesting command %s with args '%s'"
              % (message.author, command_name, arguments))

        elapsed = config["cooldown"]
        if message.author.id in self.cooldowns:
            elapsed = time.time() - self.cooldowns[message.author.id]

        if elapsed < config["cooldown"] and not message.author == info.owner:
            temp_message = await message.channel.send(
                "Cooldown still active, please wait %d seconds."
                % (config["cooldown"] - elapsed)
            )
            await asyncio.sleep(5)
            return await temp_message.delete()

        self.cooldowns[message.author.id] = time.time()
        return await command.execute(context)

    def get_command(self, input_command_name):
        mapping = {}

        for command in self.commands:
            names = command.names
            command_names = names() if callable(names) else names

            for name in command_names:
                for i in range(1, len(name)):
                    short = name[:i]
                    if short not in mapping:
                        mapping[name] = (command, name, short)
                        mapping[short] = (command, name, short)
                        break

        return mapping.get(input_command_name, (None, None, None))
