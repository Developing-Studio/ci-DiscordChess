#!/bin/python
import os

from discord import Embed
from discord.ext.commands import AutoShardedBot, Context

from DiscordBot.cogs import COGS
from DiscordBot.color import Colors
from DiscordBot.utils import add_cogs

bot = AutoShardedBot(command_prefix="%")
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)


@bot.command()
async def help(ctx: Context):
    embed = Embed(
        title="DiscordChess",
        description="Description is a discord bot that allows you play chess with your friends",
        color=Colors.GAME_DARK
    )
    embed.add_field(
        name="Challenge a player",
        value="To play with another user run\n`%game create <member> [Game Title]`.\nThe other player does not accept your invitation and he will be always playing as black",
        inline=False
    )
    embed.add_field(
        name="Load custom game",
        value="To load a custom game, run\n`%game load <member> <\"fen string\"> [\"Game Title\"]`.\nThis command loads a game based on a FEN string.\n**Attention:** The FEN string and Game title need to be encapsulated in quotation signs!",
        inline=False
    )
    embed.add_field(
        name="List all your games",
        value="To list all games, run\n`%game`.\nTo jump to one of these Games, click on the name of the game.",
        inline=False
    )
    embed.add_field(name="** **", value="** **", inline=False)
    embed.add_field(name="Source Code", value="[Github page](https://github.com/DiscordChess/DiscordChess)")
    embed.add_field(name="** **", value="Used on `" + str(len(bot.guilds)) + "` server(s).")
    embed.set_footer(text="Bot by ce_phox#1259 and n.ooaa.h#7721")
    await ctx.send(embed=embed)


add_cogs(bot, COGS)
bot.run(os.environ["TOKEN"])
