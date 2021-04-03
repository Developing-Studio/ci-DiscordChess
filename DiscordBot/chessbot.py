#!/bin/python
import os

from discord.ext.commands import AutoShardedBot

from DiscordBot.cogs import COGS
from DiscordBot.utils import add_cogs

bot = AutoShardedBot(command_prefix="%")


@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)


add_cogs(bot, COGS)
bot.run(os.environ["TOKEN"])
