import cv2 as cv
from urllib.request import Request, urlopen
import numpy as np
from discord.ext import commands
import discord
from qrcode import make
from utils.aioreq import aioreq


class custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def url_to_image(self, url, readFlag=cv.IMREAD_COLOR):
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
        url = member.avatar_url
        img = aioreq()
        byte = await img.magic(str(url))
        #image = cv.imdecode(byte, cv.IMREAD_COLOR)
        canny = cv.Canny(byte, 125, 175)
        cv.imwrite("canny_image.jpg", canny)
        file=discord.File('canny_image.jpg')
        await ctx.send(file=file)


    @commands.command()
    async def lap(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        else:
            member = member
        url = member.avatar_url
        img = aioreq()
        byte = await img.magic(str(url))                    
        gray = cv.cvtColor(byte, cv.COLOR_BGR2GRAY)
        lap = cv.Laplacian(gray, None)
        lap = np.uint8(np.absolute(lap))
        cv.imwrite("lap_image.jpg", lap)
        file = discord.File('lap_image.jpg')
        await ctx.send(file=file)        

    @commands.command()
    async def thresh(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        else:
            member= member
        url = member.avatar_url
        img = aioreq()
        byte = await img.magic(str(url))
        try:
            threshold, thresh = cv.threshold(byte, 50, 255, cv.THRESH_BINARY)
            cv.imwrite("thresh_image.jpg", thresh)
            file=discord.File('thresh_image.jpg')
            await ctx.send(file=file)
        except Exception:
           await ctx.send("Animated pics not allowed for this command")

    @commands.command()
    async def qr(self,ctx,text=None):
        if text is None:
            text = str(ctx.message.author.avatar_url)
        else:
            text = text
        qr = make(text)
        qr.save("qrcode.jpg")
        file=discord.File('qrcode.jpg')
        await ctx.send(file=file)               



def setup(bot):
    bot.add_cog(custom(bot))
