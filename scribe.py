import config
import discord
from utils.db import db
from utils.plugin_cache import plugin_cache
from discord.ext import commands

bot = commands.Bot(command_prefix=config.command_prefix)

@bot.check
def guild_has_plugin(ctx):
    return isinstance(ctx.channel, discord.DMChannel) or ctx.cog.qualified_name in plugin_cache.cache[ctx.guild.id]

if __name__ == "__main__":
    db.create_db()

    for plugin in config.plugins:
        bot.load_extension(plugin)
    bot.run(config.token)
