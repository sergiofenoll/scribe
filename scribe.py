import config
from discord.ext import commands

bot = commands.Bot(command_prefix=config.command_prefix)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('---------')

if __name__ == "__main__":
    for plugin in config.plugins:
        bot.load_extension(plugin)
    bot.run(config.token)
