import discord

from .command import command
from .. import templates


help_message = """
This bot can generate **manga panels** (and other templates).

To browse all available templates with examples,\
 ask for an invite with the `.gallery` command.

When generating templates with Japanese text,\
 a language processor will annotate all *kanji* with **furigana**.

The command to generate a panel starts with a full stop,\
 followed by the name of the category\
 (the first letter is enough, for example `.y`).\
 After the command name, specify the template name, and then the text to use.

Try it out yourself:

• `.yotsuba ask 何これ…？`
• `.y gun 俺を誰だと思ってるんだ⁉️`
• `.template yotsuba-pray ご馳走様〜！`

Templates denoted with a number contains that amount of speech bubbles.\
 To fill them, each bubble must be provided on a separate line\
 (Shift + Enter on desktop, carriage return on mobile). For example:

```
.gintama revolt This is bubble
1.And this is bubble 2!
```

**Available categories:**
""".strip()


@command()
async def help(context):
    embed = discord.Embed(
        title="Help for %s" % context.info.name,
        description=help_message
    )
    embed.set_thumbnail(url="https://i.imgur.com/mzYNzSN.png")

    categories = templates.categories

    for category in categories:
        names = []
        for template_name in categories[category]:
            name = "`%s`" % template_name
            if "bubbles" in categories[category][template_name]:
                elements = len(categories[category][template_name]["bubbles"])
            else:
                elements = categories[category][template_name]["elements"]
            if elements > 1:
                name += " (%d)" % elements
            names.append(name)

        embed.add_field(
            name="%s (`.%s`, `.%s`):" % (
                category.capitalize(),
                context.manager.get_command(category)[2],
                category
            ),
            value=", ".join(names),
            inline=True
        )

    return await context.message.author.send(embed=embed)
