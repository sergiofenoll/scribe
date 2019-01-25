import config
from utils.db import db
from discord.ext import commands

bot = commands.Bot(command_prefix=config.command_prefix)

if __name__ == "__main__":
    db.create_db()
    for plugin in config.plugins:
        bot.load_extension(plugin)
    bot.run(config.token)
