import io
import urllib
import aiohttp

import nextcord
from nextcord.ext import commands

from core import i18n

_ = i18n.Translator("modules/math").translate

PNG_HEADER = b"\x89PNG\r\n\x1a\n"


class Latex(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def latex(self, ctx, *, equation: str):
        equation: str = urllib.parse.quote(equation)
        url: str = (
            "http://www.sciweavers.org/tex2img.php?"
            f"eq={equation}&fc=White&im=png&fs=25&edit=0"
        )
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        await ctx.send(
                            _(
                                ctx,
                                "Couldn't convert equation to image (E{code}).",
                            ).format(code=response.status)
                        )
                        return

                    data = await response.read()
                    if not data.startswith(PNG_HEADER):
                        await ctx.send(_(ctx, "Couldn't convert equation to image."))
                        return

                    await ctx.channel.send(
                        file=nextcord.File(io.BytesIO(data), "latex.png")
                    )


def setup(bot) -> None:
    bot.add_cog(Latex(bot))
