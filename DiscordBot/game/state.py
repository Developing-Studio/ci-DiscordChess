from typing import List

from discord import Reaction

from Chess.chess import letter_to_name
from DiscordBot.utils import figure_to_emoji, letter_to_emoji, number_to_emoji


class Field:
    def __init__(self, name: str, value: str, inline: bool = False):
        self.name = name
        self.value = value
        self.inline = inline


class State:
    def __init__(self, game):
        self.game = game

        state_cls = self
        game.state = state_cls

    def next(self, *args, **kwargs):
        pass

    def get_embed_fields(self) -> List[Field]:
        return []

    def possible_emotes(self) -> list:
        return []

    def on_react(self, reaction: Reaction):
        pass


class SelectFigureState(State):
    def __init__(self, game):
        super().__init__(game)

    def next(self, selected_letter: str):
        SelectFigureRow(self.game, selected_letter)

    def get_embed_fields(self) -> List[Field]:
        return [Field(
            name="** **",
            value="Please select a figure to move"
        )]

    def possible_emotes(self) -> list:
        movable_letters = self.game.chess.get_remaining_movable_letters()
        return [figure_to_emoji(i, 3) for i in movable_letters]

    def on_react(self, reaction: Reaction):
        self.next(reaction.emoji.name[0])


class SelectFigureRow(State):
    def __init__(self, game, selected_letter: str):
        super().__init__(game)
        self.selected_letter = selected_letter
        self.rows = self.game.chess.get_rows_containing_movable_letter(selected_letter)

        if len(self.rows) == 1:
            self.next(self.rows[0])

    def next(self, selected_row: str):
        SelectFigureColumn(self.game, self.selected_letter, selected_row)

    def get_embed_fields(self) -> List[Field]:
        return [Field(
            name="** **",
            value="Please select the column, where your **" + letter_to_name(
                self.selected_letter).lower() + "** is located"
        )]

    def possible_emotes(self) -> list:
        return [letter_to_emoji(i) for i in self.rows]

    def on_react(self, reaction: Reaction):
        em = reaction.emoji
        self.next(
            "a" if em == "🇦" else "b" if em == "🇧" else "c" if em == "🇨" else "d" if em == "🇩" else "e" if em == "🇪" else "f" if em == "🇫" else "g" if em == "🇬" else "h"
        )


class SelectFigureColumn(State):
    def __init__(self, game, selected_letter: str, selected_row: str):
        super().__init__(game)
        self.selected_letter = selected_letter
        self.selected_row = selected_row

        self.cols = self.game.chess.get_lines_containing_movable_letter_in_row(selected_letter, selected_row)
        if len(self.cols) == 1:
            self.next(self.cols[0])

    def next(self, selected_col: str):
        SelectMovePosRow(self.game, self.selected_letter, self.selected_row + selected_col)

    def get_embed_fields(self) -> List[Field]:
        return [Field(
            name="** **",
            value="Please select the row, where your **" +
                  letter_to_name(self.selected_letter).lower() + "** is located on column **" + self.selected_row + "**"
        )]

    def possible_emotes(self) -> list:
        return [number_to_emoji(i) for i in self.cols]

    def on_react(self, reaction: Reaction):
        emotes = ["1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣"[i:i + 3] for i in range(0, 8 * 3, 3)]
        self.next(str(emotes.index(reaction.emoji) + 1))


class SelectMovePosRow(State):
    def __init__(self, game, selected_letter: str, position: str):
        super().__init__(game)
        self.selected_letter = selected_letter
        self.position = position

        self.rows = sorted(
            self.game.chess.get_figure_possible_moves_rows(self.selected_letter + self.position),
            key=ord
        )
        if len(self.rows) == 1:
            self.next(self.rows[0])

    def next(self, selected_row, castled: bool = False):
        if not castled:
            SelectMovePosColumn(self.game, self.selected_letter, self.position, selected_row)
            return
        SelectCastleMove(self.game, self.selected_letter, self.position)

    def get_embed_fields(self) -> List[Field]:
        l = [
            Field(
                name="Selected figure",
                value="**" + letter_to_name(self.selected_letter) + "** on **" + self.position + "**"
            ),
            Field(
                name="** **",
                value="Select the column, where you want your **" +
                      letter_to_name(self.selected_letter).lower() + "** to move to",
                inline=True
            )
        ]

        if "r" in map(lambda r: r.lower(), self.rows):
            l.append(Field("** **", "** **", True))
            l.append(Field(
                name="Castling",
                value="To castle, select 🇷",
                inline=True
            ))

        return l

    def possible_emotes(self) -> list:
        return [letter_to_emoji(i) for i in self.rows]

    def on_react(self, reaction: Reaction):
        em = reaction.emoji
        if em == "🇷":
            self.next("", True)
            return
        self.next(
            "a" if em == "🇦" else "b" if em == "🇧" else "c" if em == "🇨" else "d" if em == "🇩" else "e" if em == "🇪" else "f" if em == "🇫" else "g" if em == "🇬" else "h"
        )


class SelectCastleMove(State):
    def __init__(self, game, letter, position):
        super().__init__(game)
        self.letter = letter
        self.position = position

    def next(self, side):
        ExecuteSelectedMove(
            self.game,
            self.letter,
            self.position,
            "r" + (side.lower() if self.game.chess.get_turn() == "b" else side.upper())
        )

    def get_embed_fields(self) -> List[Field]:
        return [
            Field(
                name="Selected figure",
                value="**" + letter_to_name(self.letter) + "** on **" + self.position + "**"
            ),
            Field(
                name="** **",
                value="To castle on the **kingside**, select 🇰.\nTo castle on the queenside, select 🇶.",
                inline=True
            )
        ]

    def possible_emotes(self) -> list:
        return ["🇰", "🇶"]

    def on_react(self, reaction: Reaction):
        self.next("q" if reaction.emoji == "🇶" else "k")


class SelectMovePosColumn(State):
    def __init__(self, game, selected_letter, position, selected_row):
        super().__init__(game)
        self.letter = selected_letter
        self.position = position
        self.selected_row = selected_row

        self.cols = self.game.chess.get_figure_possible_moves_lines_in_row(
            self.letter + self.position, self.selected_row
        )

        if len(self.cols) == 1:
            if self.letter.lower() != "p":
                self.next(str(self.cols[0]))
            else:
                self.next(str(self.cols[0]), True if self.cols[0] in ["1", "8"] else False)

    def next(self, selected_col, transform=False):
        if not transform:
            ExecuteSelectedMove(self.game, self.letter, self.position, self.selected_row + selected_col)
            return
        PawnTransformationSelection(self.game, self.letter, self.position, self.selected_row + selected_col)

    def get_embed_fields(self) -> List[Field]:
        return [
            Field(
                name="Selected figure",
                value="**" + letter_to_name(self.letter) + "** on **" + self.position + "**"
            ),
            Field(
                name="** **",
                value="Select the row, where you want your **" +
                      letter_to_name(
                          self.letter).lower() + "** to move to (Selected column: **" + self.selected_row + "**)",
                inline=True
            )
        ]

    def possible_emotes(self) -> list:
        return [number_to_emoji(i) for i in self.cols]

    def on_react(self, reaction: Reaction):
        emotes = ["1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣"[i:i + 3] for i in range(0, 8 * 3, 3)]
        col = emotes.index(reaction.emoji) + 1
        if self.letter.lower() != "p":
            self.next(str(col))
        else:
            self.next(str(col), True if col in ["1", "8"] else False)


class PawnTransformationSelection(State):
    def __init__(self, game, letter, position, move):
        super().__init__(game)
        self.letter = letter
        self.position = position
        self.move = move

        self.transforms = self.game.chess.get_figure_transormation_options(letter + position)

        if len(self.transforms) == 1:
            self.next(self.transforms[0])

    def next(self, transform):
        ExecuteSelectedMove(
            self.game,
            self.letter,
            self.position,
            self.move,
            transform.lower() if self.game.chess.get_turn() == "b" else transform.upper()
        )

    def get_embed_fields(self) -> List[Field]:
        return [
            Field(
                name="Selected figure",
                value="**" + letter_to_name(self.letter) + "** on **" + self.position + "**"
            ),
            Field(
                name="** **",
                value="Select the figure type your pawn shall become. "
                      "Only those figures, which can move your next turn, are selectable",
                inline=True
            )
        ]

    def possible_emotes(self) -> list:
        return [figure_to_emoji(i, 3) for i in self.transforms]

    def on_react(self, reaction: Reaction):
        self.next(reaction.emoji.name[0])


class ExecuteSelectedMove(State):
    def __init__(self, game, letter, position, move, option=""):
        super().__init__(game)
        self.game.chess.move(letter + position + move + option)
        self.gameover = self.game.chess.get_game_is_over()
        self.next(self.gameover)

    def next(self, end=False):
        if not end:
            SelectFigureState(self.game)
            return

    async def end_game(self):
        self.game.delete()
        await self.game.update_message([
            {
                "name": "Game Over!",
                "value": "Cause: " + self.game.chess.get_game_is_over_messsage(),
                "inline": False
            }
        ])
