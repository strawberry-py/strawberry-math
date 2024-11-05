import io
import re

import aiohttp

import discord
from discord.ext import commands

from pie import check, i18n

_ = i18n.Translator("modules/math").translate


class Latex(commands.Cog):
    """Special thanks to solumath.
    Created / maintained with help of vutfitdiscord/rubbergod authors.
    """

    def __init__(self, bot):
        self.bot = bot

    @check.acl2(check.ACLevel.MEMBER)
    @commands.command()
    async def latex(self, ctx: commands.Context, *, equation: str):
        base_url: str = "https://www.sciweavers.org/"
        payload = {
            "eq_latex": equation,
            "eq_forecolor": "White",
            "eq_bkcolor": "Transparent",
            "eq_font_family": "iwona",
            "eq_font": "25",
            "eq_imformat": "PNG",
        }
        async with ctx.typing():
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    base_url + "process_form_tex2img", data=payload
                ) as response:
                    if response.status != 200:
                        await ctx.send(
                            _(
                                ctx,
                                "Couldn't convert equation to image (E{code}).",
                            ).format(code=response.status)
                        )
                        return
                    image_url: str = self._get_image_url(await response.text())

                if not image_url:
                    await ctx.send(_(ctx, "Couldn't convert equation to image."))
                    return

                async with session.get(base_url + image_url) as response:
                    data = io.BytesIO(await response.read())

                    await ctx.channel.send(file=discord.File(data, "latex.png"))

    def _get_image_url(self, text: str) -> str:
        """Extract the image URL from the response text."""
        pattern = r"/upload/Tex2Img_\w+\/\w+\.png"
        matches = re.findall(pattern, text)
        return matches[0]


async def setup(bot) -> None:
    await bot.add_cog(Latex(bot))
