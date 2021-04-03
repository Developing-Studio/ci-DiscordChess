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
        elif game.move_state == MoveState.SELECT_FIGURE_ROW:
            game.move_state = MoveState.SELECT_FIGURE_COLUMN
            em = reaction.emoji
            print(em)
            row = "a" if em == "🇦" else "b" if em == "🇧" else "c" if em == "🇨" else "d" if em == "🇩" else "e" if em == "🇪" else "f" if em == "🇫" else "g" if em == "🇬" else "h"
            await game.update_reactions(select_figure_row=row)
        elif game.move_state == MoveState.SELECT_FIGURE_COLUMN:
            game.move_state = MoveState.SELECT_MOVE_POSITION
            em = reaction.emoji
            emotes = ["1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣7️⃣8️⃣"[i:i + 3] for i in range(0, 8 * 3, 3)]
            await game.update_reactions(selected_figure_col=str(emotes.index(em) + 1))
