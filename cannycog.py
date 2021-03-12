import cv2 as cv
from urllib.request import Request, urlopen
import numpy as np
from discord.ext import commands
import discord
from utils.asyncstuff import asyncfunc

class custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @asyncexe()
    def to_image(self, bytes, readFlag):
        image = np.asarray(bytearray(bytes), dtype="uint8")
        image = cv.imdecode(image, readFlag)
        return image
    
    async def url_to_image(self, url, readFlag=cv.IMREAD_COLOR):
        # download the image, convert it to a NumPy array, and read the numpy array
        async with self.bot.session.get(url) as resp:
            image_bytes = await resp.read()
        image = await self.to_image(image_bytes, readFlag)
        # return the image
        return image   
    @asyncexe()
    def _canny(self, image):
        canny = cv.Canny(image, 125, 175)
        is_success, image_buffer = cv2.imencode(".png", canny)
        buffer = BytesIO(image_buffer)
        return discord.File(buffer, "canny.png")

    @commands.command()
    async def canny(self,ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        else:
            member = member
        img = await self.url_to_image(member.avatar_url)    
        file = await self._canny(img)
        await ctx.send(file=file) 

def setup(bot):
    bot.add_cog(custom(bot))
