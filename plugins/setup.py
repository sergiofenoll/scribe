import asyncio
from datetime import datetime
from discord.ext import commands
from utils.db import db


class Setup:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def populate_db(self, ctx, *args):
        date_format = "%Y-%m-%d"
        if len(args) > 3 or len(ctx.channel_mentions) == 0:
            return  # Send msg about wrong formatting

        try:
            if args[0] == "before":
                before = datetime.strptime(arg[1], date_format)
                after = None
            elif args[0] == "after":
                after = datetime.strptime(arg[1], date_format)
                before = None
            else:
                after = datetime.strptime(arg[0], date_format)
                before = datetime.strptime(arg[1], date_format)
        except ValueError as e:
            return  # Send msg about wrong formatting

        for channel in ctx.channel_mentions:
            async for message in channel.history(
                limit=None, before=before, after=after
            ):
                continue  # Write message to DB


def setup(bot):
    bot.add_cog(Setup(bot))
