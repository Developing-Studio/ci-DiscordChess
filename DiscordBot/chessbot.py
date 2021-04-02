import os

from discord.ext.commands import AutoShardedBot

from DiscordBot.cogs import COGS
from DiscordBot.utils import add_cogs

bot = AutoShardedBot(command_prefix="%")


@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)
    print()
    for i in bot.guilds[0].emojis:
        ids = "<:{name}:{id}>".format(name=i.name, id=i.id)

        post = i.name[0]
        name = "r" if "rook" in ids else "q" if "queen" in ids else "p" if "pawn" in ids else "n" if "knight" in ids else "k" if "king" in ids else "b" if "bishop" in ids else "t"
        if i.name[-1] == "w":
            name = name.upper()
        print("\"{}\": \"{}\",".format(name + post, ids))


add_cogs(bot, COGS)
bot.run(os.environ["TOKEN"])
