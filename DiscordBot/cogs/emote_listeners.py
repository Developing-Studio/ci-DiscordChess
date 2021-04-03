from typing import Union

from discord import Reaction, Member, User, Message
from discord.ext.commands import Cog, AutoShardedBot

from DiscordBot.game.game import Game, get_game_by_message_id, MoveState


class EmoteCog(Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @Cog.listener()
    async def on_reaction_add(self, reaction: Reaction, member: Union[Member, User]):
        if isinstance(member, User) or member.id == self.bot.user.id:
            return

        message: Message = reaction.message
        game: Game = get_game_by_message_id(message.id)

        if game.get_current_member().id != member.id:
            await message.remove_reaction(reaction, member)
            return

        if game.move_state == MoveState.SELECT_FIGURE:
            game.move_state = MoveState.SELECT_FIGURE_ROW
            await game.update_reactions(selected_figure=reaction.emoji.name[0])
