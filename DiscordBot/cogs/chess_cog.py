from discord import Embed, Member
from discord.ext.commands import Cog, AutoShardedBot, Context, group

from DiscordBot.color import Colors
from DiscordBot.game.game import Game, get_games


class ChessCog(Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @group()
    async def game(self, ctx: Context):
        if ctx.subcommand_passed:
            return

        embed = Embed(title="Chess Games", color=Colors.GAME)

        embed.add_field(
            name=":chess_pawn: Your Games",
            value="\n".join(
                ["[{}]({}) against {}".format(i.name, i.url, (i.m1 if i.m2 == ctx.author else i.m2).mention) for i in
                 get_games(ctx.author)]) if get_games(
                ctx.author) else "No games so far",
            inline=False
        )
        await ctx.send(embed=embed)

    @game.command()
    async def create(self, ctx: Context, challenge: Member, *, name: str = "Chess Game"):
        if challenge == ctx.author:
            embed = Embed(description="You can't play against yourself!", color=Colors.ERROR)
            await ctx.send(embed=embed)
            return

        res = await Game.create(ctx, challenge, name)
        if res is None:
            embed = Embed(description="You can't create another game with this player!", color=Colors.ERROR)
            await ctx.send(embed=embed)

    @game.command()
    async def load(self, ctx: Context, challenge: Member, fen: str, name: str = "Chess Game"):
        if challenge == ctx.author:
            embed = Embed(description="You can't play against yourself!", color=Colors.ERROR)
            await ctx.send(embed=embed)
            return

        res = await Game.create(ctx, challenge, name, fen)
        if res is None:
            embed = Embed(description="You can't create another game with this player!", color=Colors.ERROR)
            await ctx.send(embed=embed)
