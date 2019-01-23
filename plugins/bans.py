from plugins.db import db
from discord.ext import commands


class Bans:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ban(self, ctx, user):
        u_id = int(user.strip("<>@!"))
        username = ctx.message.guild.get_member(u_id).name
        cur_bans = db.get_bans({"user_id": u_id})[0]
        db.update_bans({"count": cur_bans + 1, "u_id": u_id})
        await ctx.send(f"Ban-count of **{username}** has been updated to **{cur_bans + 1}**")

    @commands.command()
    async def banned(self, ctx, user):
        u_id = int(user.strip("<>@!"))
        username = ctx.message.guild.get_member(u_id).name
        cur_bans = db.get_bans({"user_id": u_id})[0]
        await ctx.send(f"Ban-count of **{username}**: **{cur_bans}**")

    async def on_reaction_add(self, reaction, user):
        try:
            if reaction.emoji.id == 273572358202064897: # :banned: emoji
                msg = reaction.message
                cur_bans = db.get_bans({"user_id": msg.author.id})[0]
                db.update_bans({"count": cur_bans + 1, "u_id": msg.author.id})
                await msg.add_reaction("✅") # :white_check_mark: emoji
        except AttributeError:
            # The emoji was a unicode emoji, we don't care about it
            pass
                
    async def on_reaction_remove(self, reaction, user):
        try:
            if reaction.emoji.id == 273572358202064897: # :banned: emoji
                msg = reaction.message
                cur_bans = db.get_bans({"user_id": msg.author.id})[0]
                db.update_bans({"count": cur_bans - 1, "u_id": msg.author.id})
                await msg.add_reaction("✅") # :white_check_mark: emoji
        except AttributeError:
            # The emoji was a unicode emoji, we don't care about it
            pass


def setup(bot):
    bot.add_cog(Bans(bot))
