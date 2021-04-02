from typing import List

from discord import Member, Embed, Message
from discord.ext.commands import Context

from Chess.chess import ChessGame, numbers_to_dashes
from DiscordBot.color import Colors
from DiscordBot.utils import figure_to_emoji


class Game:
    def __init__(self, member: Member, name: str):
        self.member = member
        self.name = name
        self.chess = ChessGame()

    def create_emojis(self):
        string = ""
        index = True
        for row in self.chess.game.split()[0].split("/"):
            row = numbers_to_dashes(row)
            for figure in row:
                string += figure_to_emoji(figure, index)
                index = not index
            string += "\n"
            index = not index

        return string

    async def create_message(self, ctx: Context):
        embed = Embed(title=self.name, color=Colors.GAME_DARK)
        embed.description = self.create_emojis()
        embed.add_field(name="Who's turn?", value="White" if self.chess.get_turn() == "w" else "Black")
        message: Message = await ctx.send(embed=embed)
        self.id = message.id
        self.url = message.jump_url

    @staticmethod
    async def create(ctx: Context, name: str) -> "Game":
        game: Game = Game(ctx.author, name)
        if ctx.author.id not in games.keys():
            games[ctx.author.id] = []

        games[ctx.author.id].append(game)
        await game.create_message(ctx)
        return game


games: dict = {}


def get_games(member: Member) -> List[Game]:
    return games[member.id] if member.id in games.keys() else []


def get_game(member: Member, name: str) -> Game:
    gms: List[Game] = get_games(member)
    l = [i for i in gms if i.name == name]
    return l[0] if l else None
