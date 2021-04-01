from discord import Embed
from discord.ext.commands import Cog, AutoShardedBot, Context, group

from DiscordBot.color import Colors


class ChessCog(Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @group()
    async def game(self, ctx: Context):
        if ctx.invoked_subcommand:
            return

        embed = Embed(title="Games", color=Colors.GAME)
        embed.add_field(
            name=":chess_pawn: Your Games",
            value="[One game](https://www.youtube.com/watch?v=dQw4w9WgXcQ)\n"
                  "[The other game](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
        )
        embed.add_field(name=":boom: Score", value="42")
        await ctx.send(embed=embed)

    @game.command()
    async def create(self, ctx: Context):
        embed = Embed(title="Create a chess game", color=Colors.GAME)
        await ctx.send(embed=embed)
