import openai 
import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
apikey=os.environ['GPT']

class Chatbot(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def gpt(self, ctx: commands.Context, *, prompt:str):
        async with aiohttp.ClientSession() as session:
            payload= {
                "model": "gpt-3.5-turbo",
                "prompt": prompt,
                "temperature": 0.5,
                "max_tokens": 50,
                "presence_penalty": 0,
                "frequency_penalty": 0,
                "best_of": 1,
            }
            headers = {"Authorization": f"Bearer {apikey}"}
            async with session.post("https://api.openai.com/v1/completions", json=payload, headers=headers) as resp:
                response = await resp.json()
                print(response)
                embed = discord.Embed(title="Chat GPT's Response:", description=response["choices"][0]["text"])
                await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Chatbot(bot))