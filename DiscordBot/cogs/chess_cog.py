from discord import Embed
from discord.ext.commands import Cog, AutoShardedBot, Context, group

from DiscordBot.color import Colors
from DiscordBot.game.game import Game, get_games, get_game


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
    async def show(self, ctx: Context, *, name: str):
        game: Game = get_game(ctx.author, name)
        if not game:
            embed = Embed(description="The game `{}` does not exists!".format(name), color=Colors.ERROR)
            await ctx.send(embed=embed)
            return

        embed = Embed(title="Game information", color=Colors.GAME_LIGHT)
        embed.add_field(name="Name", value=game.name)
        embed.add_field(name="Jump url", value="[Click here](" + game.url + ")")
        await ctx.send(embed=embed)

    @game.command()
    async def create(self, ctx: Context, *, name: str = "Chess Game"):
        game: Game = Game.create(ctx.author, name)

        embed = Embed(color=Colors.GAME)
        embed.description = "Created a new chess game"
        embed.add_field(name="Name", value=game.name)
        embed.add_field(name="Jump url", value="[Click here](" + game.url + ")")

        await ctx.send(embed=embed)
