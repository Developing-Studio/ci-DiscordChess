#!/bin/python
import os
from datetime import datetime

from discord import Embed, ActivityType, Activity
from discord.ext.commands import AutoShardedBot, Context

from DiscordBot.cogs import COGS
from DiscordBot.color import Colors
from DiscordBot.utils import add_cogs, delete_folder_contents

delete_folder_contents("dist")


async def prefix(_, message):
    if message.guild is None:
        return ""
    return "%", f"<@!{bot.user.id}> ", f"<@{bot.user.id}> "


bot = AutoShardedBot(command_prefix=prefix, case_insensitive=True)
bot.remove_command("help")


@bot.event
async def on_ready():
    print("Logged in as " + bot.user.name)
    await bot.change_presence(activity=Activity(type=ActivityType.watching, name="chess games ♟️ %help️"))


@bot.command()
async def help(ctx: Context):
    embed = Embed(
        title="DiscordChess",
        description="Description is a discord bot that allows you play chess with your friends",
        color=Colors.GAME_DARK,
        timestamp=datetime.now()
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
    embed.add_field(name="Giving up and offering a draw",
                    value="To give up (it has to be your own turn), click :x:\nTo offer a draw, click on :handshake:. Both players have to react with :handshake: before the game goes along, otherwise, it is automatically denied.")
    embed.add_field(name="** **", value="** **", inline=False)
    embed.add_field(name="Source Code", value="[Github page](https://github.com/DiscordChess/DiscordChess)")
    embed.add_field(name="Support", value="[DiscordChess Server](https://discord.gg/mbTm2Uruk4)")
    embed.add_field(name="Invite this Bot",
                    value="[Invite Link](https://discord.com/oauth2/authorize?client_id=827207000005541909&permissions=272448&scope=bot)")
    embed.add_field(name="** **", value="Used on `" + str(len(bot.guilds)) + "` servers.", inline=False)
    embed.set_footer(text="Bot by ce_phox#1259 and n.ooaa.h#7721", icon_url=bot.user.avatar_url)
    await ctx.send(embed=embed)


add_cogs(bot, COGS)
bot.run(os.environ["TOKEN"])
