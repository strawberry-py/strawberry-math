import io
import urllib
import aiohttp

import discord
from discord.ext import commands

from core import i18n

_ = i18n.Translator("modules/math").translate

PNG_HEADER = b"\x89PNG\r\n\x1a\n"


class Latex(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def latex(self, ctx, *, equation: str):
        async with ctx.typing():
            equation: str = urllib.parse.quote(equation)
            url: str = f"http://www.sciweavers.org/tex2img.php?eq={equation}&fc=White&im=png&fs=25&edit=0"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        return await ctx.send(_(
                            ctx,
                            "Couldn't convert equation to image (E{code}).".format(code=response.status)
                        ))

                    data = await response.read()
                    if not data.startswith(PNG_HEADER):
                        return await ctx.send(_(ctx, "Couldn't convert equation to image."))

                    await ctx.channel.send(file=discord.File(io.BytesIO(data), "latex.png"))


def setup(bot) -> None:
    bot.add_cog(Latex(bot))
