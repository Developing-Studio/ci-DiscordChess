from discord.ext.commands import AutoShardedBot

from ChessBot.cogs import COGS


def add_cogs(bot: AutoShardedBot):
    for cog in COGS:
        bot.add_cog(cog)
