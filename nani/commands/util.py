import os
import discord
from PIL import Image

from ..render import render

max_file_size = 2 * 1024 * 1024  # 2 MB


async def send_template(context, channel, template, text, msg=None):
    print(
        "=> User %s is rendering template %s with text '%s'"
        % (context.message.author, template["name"], text)
    )
    path = render(template, text, context.message.author.display_name)

    if os.path.getsize(path) > max_file_size:
        print("Compressing large file")
        image = Image.open(path)
        image = image.convert("RGB")
        path, old_path = path[:-3] + "jpg", path
        image.save(path)
        os.remove(old_path)

    message = await channel.send(file=discord.File(path), content=msg)
    os.remove(path)
    return message


circled_numbers = ["⓪"] + [
    "①", "②", "③", "④", "⑤", "⑥", "⑦", "⑧", "⑨", "⑩",
    "⑪", "⑫", "⑬", "⑭", "⑮", "⑯", "⑰", "⑱", "⑲", "⑳",
    "㉑", "㉒", "㉓", "㉔", "㉕", "㉖", "㉗", "㉘", "㉙", "㉚",
    "㉛", "㉜", "㉝", "㉞", "㉟", "㊱", "㊲", "㊳", "㊴", "㊵",
    "㊶", "㊷", "㊸", "㊹", "㊺", "㊻", "㊼", "㊽", "㊾", "㊿",
]
