from typing import Union

from discord import Reaction, Member, User, Message
from discord.ext.commands import Cog, AutoShardedBot

from DiscordBot.game.game import Game, get_game_by_message_id


class EmoteCog(Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, member: Union[Member, User]):
        if isinstance(member, User) or member.id == self.bot.user.id:
            return

        message: Message = reaction.message
        game: Game = get_game_by_message_id(message.id)
        if game is None:
            return

        if member.id != game.m1.id and member.id != game.m2.id:
            return

        if game.get_current_member().id != member.id:
            await message.remove_reaction(reaction, member)
            return

        if str(reaction.emoji) not in map(str, game.state.possible_emotes()):
            await message.remove_reaction(reaction, member)
            return

        game.state.on_react(reaction)
        await game.on_state()
