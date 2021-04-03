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
        self.id = 0
        self.url = ""

    def create_board(self):
        string = ":regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h:\n"
        white = True
        row_i = 8
        for row in self.chess.game.split()[0].split("/"):
            row = numbers_to_dashes(row)
            for figure in row:
                string += figure_to_emoji(figure, white)
                white = not white
            string += ":%s:\n" % (
                "eight" if row_i == 8 else "seven" if row_i == 7 else "six" if row_i == 6 else "five" if row_i == 5 else "four" if row_i == 4 else "three" if row_i == 3 else "two" if row_i == 2 else "one")
            row_i -= 1
            white = not white

        return string

    async def create_message(self, ctx: Context):
        embed = Embed(title=self.name, color=Colors.GAME_DARK)
        embed.description = self.create_board()
        embed.add_field(name="Who's turn?", value=self.chess.get_turn_name())
        embed.add_field(
            name=self.chess.get_turn_name() + " can castle",
            value="King Side: " + (":x:" if not self.chess.get_current_can_castle_kingside() else ":white_check_mark:") +
                  "\nQueen Side: " + (":x:" if not self.chess.get_current_can_castle_kingside() else ":white_check_mark:")
        )
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
