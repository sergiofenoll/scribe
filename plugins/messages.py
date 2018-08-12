import asyncio
from plugins.db import db

class Messages():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        db.add_message({"m_id": message.id, "sent_time": message.created_at, "content": message.clean_content, "author": message.author.name + str(message.author.id), "channel": message.channel.name + str(message.channel.id), "guild": message.guild.name + str(message.guild.id), "edited": False, "deleted": False})
    
    async def on_message_delete(self, message):
        db.remove_message(filters={"m_id": message.id})

    async def on_message_edit(self, before, after):
        db.edit_message(filters={"m_id": after.id}, replacement={"content": after.clean_content, "edited": True})

    async def on_reaction_add(self, reaction, user):
        db.add_reaction(filters={"m_id": reaction.message.id, "reaction_name": str(reaction.emoji), "reaction_count": reaction.count})

    async def on_reaction_remove(self, reaction, user):
        db.remove_reaction(filters={"m_id": reaction.message.id, "reaction_name": str(reaction.emoji), "reaction_count": reaction.count})

    async def on_reaction_clear(self, message, reactions):
        for reaction in reactions:
            db.remove_reaction(filters={"m_id": message.id, "reaction_name": str(reaction.emoji), "reaction_count": reaction.count})

def setup(bot):
    bot.add_cog(Messages(bot))
