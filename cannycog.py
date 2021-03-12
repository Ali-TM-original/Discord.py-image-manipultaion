import cv2 as cv
from urllib.request import Request, urlopen
import numpy as np
from discord.ext import commands
import discord

class custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def url_to_image(self,url, readFlag=cv.IMREAD_COLOR):
        # download the image, convert it to a NumPy array, and then read
        # it into OpenCV format
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        resp = urlopen(req).read()
        image = np.asarray(bytearray(resp), dtype="uint8")
        image = cv.imdecode(image, readFlag)

        # return the image
        return image

    @commands.command()
    async def canny(self,ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        else:
            member = member
        img = self.url_to_image(member.avatar_url)    
        canny = cv.Canny(img, 125, 175)
        cv.imwrite("new_image.jpg", canny)
        file=discord.File('new_image.jpg')
        await ctx.send(file=file)

def setup(bot):
    bot.add_cog(custom(bot))
