from typing import List

from discord import Member, Embed, Message, File
from discord.ext.commands import Context

from Chess.chess import ChessGame
from DiscordBot.color import Colors
from DiscordBot.game.state import SelectFigureState
from DiscordBot.image.generator import create_embed_image


class Game:
    def __init__(self, m1: Member, m2: Member, name: str):
        self.m1 = m1
        self.m2 = m2
        self.name = name
        self.chess = ChessGame()
        self.id = 0
        self.url = ""
        self.img_url = ""

        game_cls = self
        self.state = SelectFigureState(game_cls)

    async def on_state(self):
        if isinstance(self.state, SelectFigureState):
            await self.create_board_image()

        await self.update_message(
            [{"name": i.name, "value": i.value, "inline": i.inline} for i in self.state.get_embed_fields()]
        )
        await self.update_emotes(self.state.possible_emotes())
        await self.message.add_reaction("❌")
        await self.message.add_reaction("🤝")

    async def update_emotes(self, emotes: list):
        await self.message.clear_reactions()
        for em in emotes:
            await self.message.add_reaction(em)

    async def remis(self):
        await self.message.clear_reactions()
        game: Game = self
        remove_game(game)
        await self.update_message([
            {
                "name": "Game over!",
                "value": "__Cause__: Remis",
                "inline": False
            }
        ])

    async def give_up(self):
        await self.message.clear_reactions()
        game: Game = self
        remove_game(game)
        await self.update_message([
            {
                "name": "Game over!",
                "value": "__Cause__: Surrendered by " + self.get_current_member().mention,
                "inline": False
            }
        ])

    def delete(self):
        game: Game = self
        remove_game(game)

    async def create_board_image(self):
        create_embed_image(self.chess.game, self.id)
        file: File = File("./dist/" + str(self.id) + ".png")
        board: Message = (await self.ctx.bot.get_channel(829727313130291200).send(file=file))
        self.img_url = board.attachments[0].url

    async def create_embed(self, additional_fields=None, on_create: bool = True):
        embed = Embed(title=self.name, color=Colors.GAME_DARK)

        if not on_create:
            if self.img_url == "":
                await self.create_board_image()
            embed.set_image(url=self.img_url)

        embed.add_field(name="Contestants", value="White: " + self.m1.mention + "\nBlack: " + self.m2.mention,
                        inline=False)
        embed.add_field(name="Who's turn?", value=self.chess.get_turn_name())
        embed.add_field(name="** **", value="** **")
        embed.add_field(
            name=self.chess.get_turn_name() + " can castle",
            value="King Side: " + (
                ":x:" if not self.chess.get_current_can_castle_kingside() else ":white_check_mark:") +
                  "\nQueen Side: " + (
                      ":x:" if not self.chess.get_current_can_castle_kingside() else ":white_check_mark:")
        )

        if additional_fields:
            for i in additional_fields:
                embed.add_field(name=i["name"], value=i["value"], inline=i["inline"])

        return embed

    async def update_message(self, additional_fields=None):
        await self.message.edit(embed=await self.create_embed(additional_fields, False))

    async def create_message(self, ctx: Context):
        self.ctx = ctx
        self.message: Message = await ctx.send(embed=await self.create_embed())
        self.id = self.message.id
        self.url = self.message.jump_url
        await self.on_state()

    def get_current_member(self):
        return self.m1 if self.chess.get_turn() == "w" else self.m2

    @staticmethod
    async def create(ctx: Context, challenge: Member, name: str, fen: str = ""):
        game: Game = Game(ctx.author, challenge, name)

        if ctx.author.id not in games.keys():
            games[ctx.author.id] = []

        if len(list(filter(lambda x: x.m1.id == ctx.author.id or x.m2.id == ctx.author.id, games[ctx.author.id]))):
            return None

        games[ctx.author.id].append(game)

        if challenge.id not in games.keys():
            games[challenge.id] = []
        games[challenge.id].append(game)

        if fen != "":
            game.chess.game = fen

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


def remove_game(game: Game):
    for m in games.keys():
        games[m].remove(game)
