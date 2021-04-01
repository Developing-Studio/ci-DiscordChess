from discord.ext.commands import AutoShardedBot
import os
bot = AutoShardedBot(command_prefix="%")

bot.run(os.environ["TOKEN"])
