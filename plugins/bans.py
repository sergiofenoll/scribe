import asyncio
from utils.db import db
from discord.ext import commands
from discord import Embed, Colour, utils as dutils

BANNED = 273572358202064897
GREEN_TICK = 538422115334881290
RED_TICK = 538422123660836891
BAN_MSG_TEMPLATE = """Ban-count of **{0}** has been updated to **{1}**
React to this message with <:greentick:538422115334881290> if you want to help swing the banhammer or <:redtick:538422123660836891> if you stand alongside **{0}**."""

UNBAN_MSG_TEMPLATE = """Ban-count of **{0}** has been updated to **{1}**
React to this message with <:greentick:538422115334881290> if you agree with this momentous decision or <:redtick:538422123660836891> if you think **{0}** deserves a good banning."""

def create_ban_embed(banner, bannee, ban_count, ban=True):
    if ban:
        title = "Ban!"
        colour = 0xF04947
        banner_field_name = "Banner"
        bannee_field_name = "Bannee"
        description = BAN_MSG_TEMPLATE.format(bannee.name, ban_count)
    else:
        title = "Unban!"
        colour = 0x43B581
        banner_field_name = "Unbanner"
        bannee_field_name = "Unbannee"
        description = UNBAN_MSG_TEMPLATE.format(bannee.name, ban_count)

    embed = Embed(title=title, description=description, colour=colour)
    embed.set_thumbnail(url=bannee.avatar_url)
    embed.add_field(name=banner_field_name, value=f"{banner.name}#{banner.discriminator}")    
    embed.add_field(name=bannee_field_name, value=f"{bannee.name}#{bannee.discriminator}")
    return embed

class Bans:
    def __init__(self, bot):
        self.bot = bot
        self.embed_edit_tasks = {}

    # Internal functions
    def increment_ban(self, bannee):
        cur_bans = db.get_bans({"user_id": bannee.id})[0]
        db.update_bans({"count": cur_bans + 1, "u_id": bannee.id})

    def decrement_ban(self, bannee):
        cur_bans = db.get_bans({"user_id": bannee.id})[0]
        db.update_bans({"count": cur_bans - 1, "u_id": bannee.id})
        
    async def edit_embed(self, msg, embed):
        try:
            await asyncio.sleep(2)
            await msg.edit(embed=embed)
        except asyncio.CancelledError:
            pass

    @commands.command()
    async def ban(self, ctx, user_mention):
        banner = ctx.message.author
        bannee = ctx.message.guild.get_member(int(user_mention.strip("<>@!")))

        if banner == bannee:
            return

        self.increment_ban(bannee)
        ban_count = db.get_bans({"user_id": bannee.id})[0]
        
        ban_msg = await ctx.send(embed=create_ban_embed(banner, bannee, ban_count))
        await ban_msg.add_reaction(self.bot.get_emoji(GREEN_TICK))
        await ban_msg.add_reaction(self.bot.get_emoji(RED_TICK))

    @commands.command()
    async def unban(self, ctx, user_mention):
        banner = ctx.message.author
        bannee = ctx.message.guild.get_member(int(user_mention.strip("<>@!")))
        
        if banner == bannee:
            return

        self.dtimerecrement_ban(bannee)
        ban_count = db.get_bans({"user_id": bannee.id})[0]

        ban_msg = await ctx.send(embed=create_ban_embed(banner, bannee, ban_count, ban=False))
        await ban_msg.add_reaction(self.bot.get_emoji(GREEN_TICK))
        await ban_msg.add_reaction(self.bot.get_emoji(RED_TICK))

    async def on_reaction_add(self, reaction, user):
        if user == self.bot.user:
            return
        try:
            bannee = reaction.message.author
            banner = user
            if banner == bannee:
                return

            msg = reaction.message
            if reaction.emoji == "🙏":
                self.decrement_ban(bannee)
            elif reaction.emoji.id == BANNED:
                self.increment_ban(bannee)
            elif msg.author == self.bot.user:
                embed = msg.embeds[0]
                bannee_name = embed.fields[1].value.split("#")[0]
                bannee_disc = embed.fields[1].value.split("#")[1]
                bannee = dutils.get(msg.guild.members, name=bannee_name, discriminator=bannee_disc)
                og_banner = dutils.get(msg.guild.members,
                                       name=embed.fields[0].value.split("#")[0],
                                       discriminator=embed.fields[0].value.split("#")[1])
                if banner == bannee:
                    return
                if banner == og_banner:
                    return

                if embed.title == "Ban!":
                    embed_desc = BAN_MSG_TEMPLATE
                    green_tick_func = self.increment_ban
                    red_tick_func = self.decrement_ban
                elif embed.title == "Unban!":
                    embed_desc = UNBAN_MSG_TEMPLATE
                    green_tick_func = self.decrement_ban
                    red_tick_func = self.increment_ban
                
                if reaction.emoji.id == GREEN_TICK:
                    green_tick_func(bannee)
                elif reaction.emoji.id == RED_TICK:
                    red_tick_func(bannee)

                new_bans = db.get_bans({"user_id": bannee.id})[0]
                embed.description = embed_desc.format(bannee_name, new_bans)
                if msg in self.embed_edit_tasks:
                    self.embed_edit_tasks[msg].cancel()
                self.embed_edit_tasks[msg] = asyncio.create_task(self.edit_embed(msg, embed))
        except AttributeError:
            # The emoji was a unicode emoji, we don't care about it
            pass
        except IndexError:
            # Message did not contain any embeds
            pass
                
    async def on_reaction_remove(self, reaction, user):
        if user == self.bot.user:
            return
        try:
            bannee = reaction.message.author
            banner = user
            if banner == bannee:
                return
            msg = reaction.message
            if reaction.emoji == "🙏":
                self.increment_ban(bannee)
            elif reaction.emoji.id == BANNED:
                self.decrement_ban(bannee)
            elif msg.author == self.bot.user:
                embed = msg.embeds[0]
                bannee_name = embed.fields[1].value.split("#")[0]
                bannee_disc = embed.fields[1].value.split("#")[1]
                bannee = dutils.get(msg.guild.members, name=bannee_name, discriminator=bannee_disc)
                og_banner = dutils.get(msg.guild.members,
                                       name=embed.fields[0].value.split("#")[0],
                                       discriminator=embed.fields[0].value.split("#")[1])
                if banner == bannee:
                    return
                if banner == bannee:
                    return
                
                if embed.title == "Ban!":
                    embed_desc = BAN_MSG_TEMPLATE
                    green_tick_func = self.decrement_ban
                    red_tick_func = self.increment_ban
                elif embed.title == "Unban!":
                    embed_desc = UNBAN_MSG_TEMPLATE
                    green_tick_func = self.increment_ban
                    red_tick_func = self.decrement_ban
                
                if reaction.emoji.id == GREEN_TICK:
                    green_tick_func(bannee)
                elif reaction.emoji.id == RED_TICK:
                    red_tick_func(bannee)

                new_bans = db.get_bans({"user_id": bannee.id})[0]
                embed.description = embed_desc.format(bannee_name, new_bans)
                if msg in self.embed_edit_tasks:
                    self.embed_edit_tasks[msg].cancel()
                self.embed_edit_tasks[msg] = asyncio.create_task(self.edit_embed(msg, embed))
        except AttributeError:
            # The emoji was a unicode emoji, we don't care about it
            pass
        except IndexError:
            # Message did not contain any embeds
            pass

def setup(bot):
    bot.add_cog(Bans(bot))
