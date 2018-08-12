from db import db

class Messages():
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        db.add_message(message.id, created_at, message.clean_content, message.author)
        print("A message was received!")
    
    async def on_message_delete(self, message):
        print("A message was deleted!")

    async def on_message_edit(self, before, after):
        print("A message was edited!")

    async def on_reaction_add(self, reaction, user):
        print("A reaction was added!")

    async def on_reaction_remove(self, reaction, user):
        print("A reaction was removed!")

    async def on_reaction_clear(self, message, reactions):
        print("A message was cleared of reactions!")

def setup(bot):
    bot.add_cog(Messages(bot))
