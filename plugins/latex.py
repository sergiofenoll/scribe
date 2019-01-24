import discord
import subprocess
import os
import io
from discord.ext import commands



class Latex:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def latex(self, ctx, *, content):
        if content[:3] == content[-3:] == "```":
            if len(content.split()) == 1:
                text = content[3:-3]
            else:
                text = content[:-3].split(maxsplit=1)[1].rstrip()
        elif content[0] == content[-1] == "`":
            text = content[1:-1]
        else:
            text = content
        latex_output_dir = os.path.join(__file__.rsplit("/", maxsplit=1)[0], "..", "__latex_output") 
        if not os.path.exists(latex_output_dir):
            os.mkdir(latex_output_dir)

        tex = r"""\documentclass[preview, border={10pt, 10pt, 10pt, 10pt}]{standalone}
\usepackage{amsmath}
\usepackage{euler}
\usepackage{fontspec}
\newfontfamily\emoji{DejaVu Sans}
\begin{document}
\fontsize{20}{22}\selectfont
%s
\end{document}
""" % text
        
        with open(os.path.join(latex_output_dir, "temp.tex"), "w") as tex_file:
            tex_file.write(tex)
        subprocess.call(["xelatex", "-interaction=nonstopmode", "-output-directory", latex_output_dir, tex_file.name])
        img = subprocess.check_output(["pdftoppm", os.path.join(latex_output_dir, "temp.pdf"), "-png"])
        await ctx.send(file=discord.File(io.BytesIO(img), "tex.png"))


def setup(bot):
    bot.add_cog(Latex(bot))
