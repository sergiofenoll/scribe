from matplotlib import rcParams, pyplot as plt
from matplotlib.text import Text
from matplotlib.figure import Figure
from discord.ext import commands

class Latex():
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def latex(self, ctx, *, content):
        try:
            text = content[:-3].split(maxsplit=1)[1].rstrip()
        except IndexError as e:
            # content = ```xxx```, can't render
            await ctx.send("I can't render nothing, my dude.")

        plt.rc('text', usetex=True)
        plt.rc('font', family='serif')
        rcParams['text.latex.preamble'] = [r'\usepackage{amsmath}']
        # rcParams['figure.figsize'] = 2, 2
        plt.axis('off')
        
        plt.text(0.5, 0.5, text, verticalalignment='center', horizontalalignment='center', size='xx-large')
        plt.tight_layout(pad=0)
        plt.savefig('a', bbox_inches='tight', pad_inches=0)
        plt.close()

        await ctx.send(file=discord.File('a.png'))
def setup(bot):
    bot.add_cog(Latex(bot))
