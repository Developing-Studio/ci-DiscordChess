from enum import Enum
from typing import List

from discord import Member, Embed, Message
from discord.ext.commands import Context

from Chess.chess import ChessGame, numbers_to_dashes, letter_to_name
from DiscordBot.color import Colors
from DiscordBot.utils import figure_to_emoji, letter_to_emoji, number_to_emoji


class MoveState(Enum):
    SELECT_FIGURE = 0
    SELECT_FIGURE_ROW = 1
    SELECT_FIGURE_COLUMN = 2
    SELECT_MOVE_POSITION_ROW = 3
    SELECT_MOVE_POSITION_COLUMN = 4
    EXEC_MOVE = 1000


class Game:
    def __init__(self, m1: Member, m2: Member, name: str):
        self.m1 = m1
        self.m2 = m2
        self.name = name
        self.chess = ChessGame()
        self.id = 0
        self.url = ""

        self.move_state = MoveState.SELECT_FIGURE
        self.selected_figure = ""
        self.selected_position = ""
        self.move_to = ""

    async def update_reactions(self, *, selected_figure: str = "", select_figure_row: str = "",
                               selected_figure_col: str = "", select_move_row: str = "", select_move_col: str = ""):
        await self.message.clear_reactions()
        await self.update_message()
        if self.move_state == MoveState.SELECT_FIGURE:
            await self.update_message([
                {
                    "name": "** **",
                    "value": "Please select a figure to move",
                    "inline": False
                }
            ])
            for i in self.chess.get_remaining_movable_letters():
                await self.message.add_reaction(figure_to_emoji(i, 3))

        elif self.move_state == MoveState.SELECT_FIGURE_ROW:
            rows = self.chess.get_rows_containing_movable_figure(selected_figure)
            self.selected_figure = selected_figure
            if len(rows) == 1:
                self.move_state = MoveState.SELECT_FIGURE_COLUMN
                await self.update_reactions(select_figure_row=rows[0])
                return

            await self.update_message([
                {
                    "name": "** **",
                    "value": "Please select the row, where your **" + letter_to_name(
                        self.selected_figure).lower() + "** is located",
                    "inline": False
                }
            ])
            for row in rows:
                await self.message.add_reaction(letter_to_emoji(row))

        elif self.move_state == MoveState.SELECT_FIGURE_COLUMN:
            self.selected_position = select_figure_row
            cols = self.chess.get_lines_containing_movable_figure_in_row(self.selected_figure, self.selected_position)

            if len(cols) == 1:
                self.move_state = MoveState.SELECT_MOVE_POSITION_ROW
                await self.update_reactions(selected_figure_col=cols[0])
                return

            await self.update_message([
                {
                    "name": "** **",
                    "value": "Please select the column, where your **" + letter_to_name(
                        self.selected_figure).lower() + "** is located on row **" + self.selected_position + "**",
                    "inline": False
                }
            ])
            for col in cols:
                await self.message.add_reaction(number_to_emoji(col))

        elif self.move_state == MoveState.SELECT_MOVE_POSITION_ROW:
            self.selected_position += selected_figure_col
            print(self.selected_figure + self.selected_position)
            rows = self.chess.get_figure_possible_moves_rows(self.selected_figure + self.selected_position)
            if len(rows) == 1:
                self.move_state = MoveState.SELECT_MOVE_POSITION_COLUMN
                await self.update_reactions(select_move_row=rows[0])
                return

            await self.update_message([
                {
                    "name": "Selected figure and position",
                    "value": "**" + letter_to_name(self.selected_figure) + "** on **" + self.selected_position + "**",
                    "inline": False
                },
                {
                    "name": "** **",
                    "value": "Select the row, where you want your **" + letter_to_name(
                        self.selected_figure) + "** to go.",
                    "inline": False
                }
            ])
            for row in rows:
                await self.message.add_reaction(letter_to_emoji(row))
        elif self.move_state == MoveState.SELECT_MOVE_POSITION_COLUMN:
            self.move_to += select_move_row
            cols = self.chess.get_figure_possible_moves_lines_in_row(self.selected_figure + self.selected_position,
                                                                     self.move_to)
            if len(cols) == 1:
                self.move_state = MoveState.EXEC_MOVE
                await self.update_reactions(select_move_col=cols[0])
                return
            await self.update_message([
                {
                    "name": "Selected figure and position",
                    "value": "**" + letter_to_name(self.selected_figure) + "** on **" + self.selected_position + "**",
                    "inline": False
                },
                {
                    "name": "** **",
                    "value": "Select the column, where you want your **" + letter_to_name(
                        self.selected_figure) + "** to go on row **" + self.move_to + "**",
                    "inline": False
                }
            ])
            for col in cols:
                await self.message.add_reaction(number_to_emoji(col))
        elif self.move_state == MoveState.EXEC_MOVE:
            self.move_to += select_move_col
            self.chess.move(self.selected_figure + self.selected_position + self.move_to)
            self.move_state = MoveState.SELECT_FIGURE
            self.move_to = ""
            self.selected_position = ""
            self.selected_figure = ""
            await self.update_reactions()

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

    def create_embed(self, additional_fields=None):
        embed = Embed(title=self.name, color=Colors.GAME_DARK)
        embed.description = self.create_board()
        embed.add_field(name="Contestants", value="White: " + self.m1.mention + "\nBlack: " + self.m2.mention,
                        inline=False)
        embed.add_field(
            name=self.chess.get_turn_name() + " can castle",
            value="King Side: " + (
                ":x:" if not self.chess.get_current_can_castle_kingside() else ":white_check_mark:") +
                  "\nQueen Side: " + (
                      ":x:" if not self.chess.get_current_can_castle_kingside() else ":white_check_mark:")
        )
        embed.add_field(name="Who's turn?", value=self.chess.get_turn_name())

        if additional_fields:
            for i in additional_fields:
                embed.add_field(name=i["name"], value=i["value"], inline=i["inline"])

        return embed

    async def update_message(self, additional_fields=None):
        await self.message.edit(embed=self.create_embed(additional_fields))

    async def create_message(self, ctx: Context):
        self.message: Message = await ctx.send(embed=self.create_embed())
        await self.update_reactions()
        self.id = self.message.id
        self.url = self.message.jump_url

    def get_current_member(self):
        return self.m1 if self.chess.get_turn() == "w" else self.m2

    @staticmethod
    async def create(ctx: Context, challenge: Member, name: str) -> "Game":
        game: Game = Game(ctx.author, challenge, name)
        if ctx.author.id not in games.keys():
            games[ctx.author.id] = []
        games[ctx.author.id].append(game)

        if challenge.id not in games.keys():
            games[challenge.id] = []
        games[challenge.id].append(game)
        await game.create_message(ctx)
        return game


games: dict = {}


def get_games(member: Member) -> List[Game]:
    return games[member.id] if member.id in games.keys() else []


def get_game_by_message_id(id: int) -> Game:
    for l in games.values():
        for game in l:
            if game.id == id:
                return game


def get_game(member: Member, name: str) -> Game:
    gms: List[Game] = get_games(member)
    l = [i for i in gms if i.name == name]
    return l[0] if l else None
