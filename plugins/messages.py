import asyncio
from datetime import datetime
from utils.db import db
from discord import utils
from discord.ext import commands

END_TIME = datetime.strptime("9999-12-31", "%Y-%m-%d")


class Messages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged in as")
        print(self.bot.user.name)
        print(self.bot.user.id)
        print("---------")
        for guild in self.bot.guilds:
            if not db.guild_exists(filters={"g_id": guild.id}):
                db.add_guild(
                    {
                        "g_id": guild.id,
                        "name": guild.name,
                        "start_time": datetime.now(),
                        "end_time": END_TIME,
                    }
                )
            for channel in guild.channels:
                if not db.channel_exists(filters={"c_id": channel.id}):
                    try:
                        db.add_channel(
                            {
                                "c_id": channel.id,
                                "g_id": guild.id,
                                "name": channel.name,
                                "topic": channel.topic,
                                "start_time": datetime.now(),
                                "end_time": END_TIME,
                            }
                        )
                    except AttributeError as e:
                        continue  # Channel was not a TextChannel, we don't want to index those
            for member in guild.members:
                if not db.user_exists(filters={"u_id": member.id}):
                    db.add_user(
                        {
                            "u_id": member.id,
                            "g_id": guild.id,
                            "username": member.name,
                            "discriminator": member.discriminator,
                            "nick": member.nick,
                            "left": False,
                            "start_time": datetime.now(),
                            "end_time": END_TIME,
                        }
                    )
            for emoji in guild.emojis:
                db.update_emoji(
                    {
                        "e_id": emoji.id,
                        "g_id": guild.id,
                        "name": emoji.name,
                        "animated": emoji.animated,
                        "created_time": emoji.created_at,
                    }
                )

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db.add_user(
            {
                "u_id": member.id,
                "g_id": guild.id,
                "username": member.name,
                "discriminator": member.discriminator,
                "nick": member.nick,
                "left": False,
                "start_time": datetime.now(),
                "end_time": END_TIME,
            }
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db.delete_user(filters={"u_id": member.id}, data={"left": True})

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        db.edit_user(
            filters={"u_id": before.id, "end_time": END_TIME},
            data={
                "u_id": after.id,
                "g_id": after.id,
                "username": after.name,
                "discriminator": after.discriminator,
                "nick": after.nick,
                "left": False,
                "start_time": datetime.now(),
                "end_time": END_TIME,
            },
        )

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        db.add_channel(
            {
                "c_id": channel.id,
                "g_id": channel.guild.id,
                "name": channel.name,
                "topic": channel.topic,
                "start_time": datetime.now(),
                "end_time": END_TIME,
            }
        )

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        now = datetime.now()
        db.delete_message(filters={"c_id": channel.id}, data={"deleted_time": now})
        db.delete_channel(
            filters={"c_id": channel.id, "end_time": END_TIME}, data={"end_time": now}
        )

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        db.edit_channel(
            filters={"c_id": before.id, "end_time": END_TIME},
            data={
                "c_id": after.id,
                "g_id": after.guild.id,
                "name": after.name,
                "topic": after.topic,
                "start_time": datetime.now(),
                "end_time": END_TIME,
            },
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        db.add_guild(
            {
                "g_id": guild.id,
                "name": guild.name,
                "start_time": datetime.now(),
                "end_time": END_TIME,
            }
        )
        for channel in guild.channels:
            db.add_channel(
                {
                    "c_id": channel.id,
                    "g_id": channel.guild.id,
                    "name": channel.name,
                    "topic": channel.topic,
                    "start_time": datetime.now(),
                    "end_time": END_TIME,
                }
            )

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        now = datetime.now()
        db.delete_message(filters={"g_id": guild.id}, data={"deleted_time": now})
        db.delete_channel(filters={"g_id": guild.id}, data={"end_time": now})
        db.delete_guild(
            filters={"g_id": guild.id, "end_time": END_TIME}, data={"end_time": now}
        )

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        db.edit_guild(
            filters={"g_id": before.id, "end_time": END_TIME},
            data={
                "name": after.name,
                "start_time": datetime.now(),
                "end_time": END_TIME,
            },
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        db.add_message(
            {
                "m_id": message.id,
                "sent_time": message.created_at,
                "content": message.clean_content,
                "u_id": message.author.id,
                "c_id": message.channel.id,
                "g_id": message.guild.id,
                "edited": False,
                "edited_count": 0,
                "edited_time": None,
                "deleted": False,
                "deleted_time": None,
            }
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        db.delete_message(filters={"m_id": message.id, "deleted_time": datetime.now()}, data={"deleted_time": datetime.now()})

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        db.edit_message(
            filters={"m_id": after.id},
            data={"content": after.clean_content, "edited_time": after.edited_at},
        )

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        try:
            emoji = reaction.emoji.id
            db.update_emoji(
                {
                    "e_id": emoji,
                    "g_id": reaction.message.guild.id,
                    "name": reaction.emoji.name,
                    "animated": reaction.emoji.animated,
                    "created_time": utils.snowflake_time(reaction.emoji.id),
                }
            )
        except AttributeError:
            emoji = reaction.emoji
            db.update_emoji(
                {
                    "e_id": emoji,
                    "g_id": reaction.message.guild.id,
                    "name": emoji,
                    "animated": False,
                    "created_time": END_TIME,
                }
            )
        db.update_reaction(
            data={
                "m_id": reaction.message.id,
                "e_id": emoji,
                "count": reaction.count,
            }
        )

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        try:
            emoji = reaction.emoji.id
        except AttributeError:
            emoji = reaction.emoji 
        db.update_reaction(
            data={
                "m_id": reaction.message.id,
                "e_id": emoji,
                "count": reaction.count,
            }
        )

    @commands.Cog.listener()
    async def on_reaction_clear(self, message, reactions):
        for reaction in reactions:
            try:
                emoji = reaction.emoji.id
            except AttributeError:
                emoji = reaction.emoji
            db.update_reaction(
                data={
                    "m_id": message.id,
                    "e_id": emoji,
                    "count": reaction.count,
                }
            )

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        for emoji in after:
            db.update_emoji(
                {
                    "e_id": emoji.id,
                    "g_id": guild.id,
                    "name": emoji.name,
                    "animated": emoji.animated,
                    "created_time": emoji.created_at,
                }
            )


def setup(bot):
    bot.add_cog(Messages(bot))
