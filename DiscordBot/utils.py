from discord.ext.commands import AutoShardedBot

from DiscordBot.cogs import COGS


def add_cogs(bot: AutoShardedBot):
    for cog in COGS:
        bot.add_cog(cog)
