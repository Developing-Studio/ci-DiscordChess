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

        embed = Embed(title="Games", color=Colors.GAME)

        embed.add_field(
            name=":chess_pawn: Your Games",
            value="\n".join(["[{}]({})".format(i.name, i.url) for i in get_games(ctx.author)]) if get_games(
                ctx.author) else "No games so far",
            inline=False
        )
        embed.add_field(name=":boom: Score", value="42", inline=False)
        await ctx.send(embed=embed)

    @game.command()
    async def create(self, ctx: Context, challenge: Member, *, name: str = "Chess Game"):
        await Game.create(ctx, challenge, name)

    @game.command()
    async def load(self, ctx: Context, challenge: Member, fen: str, name: str = "Chess Game"):
        await Game.create(ctx, challenge, name, fen)
