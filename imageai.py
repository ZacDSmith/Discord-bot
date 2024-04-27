import discord
from openai import OpenAI
from discord.ext import commands
import os
from dotenv import load_dotenv
import aiohttp
import json

load_dotenv()
apikey=os.environ['GPT']

class ImageGen(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def image(self,ctx:commands.Context, *, prompt:str):
        async with aiohttp.ClientSession() as session:
            payload={
                "model": "dall-e-3",
                "prompt": prompt,
                "size":"1024x1024",
                "quality":"standard",
                "n":1,
            }
            headers = {"Authorization": f"Bearer {apikey}"}
            async with session.post("https://api.openai.com/v1/images/generations", json=payload, headers=headers) as resp:
                response = await resp.json()
                embed = discord.Embed(description=response["data"][0]["revised_prompt"])
                embed.set_image(url=response["data"][0]["url"])
                #await ctx.send(response["data"][0]["url"])
                await ctx.send(embed=embed)
                

async def setup(bot):
    await bot.add_cog(ImageGen(bot))