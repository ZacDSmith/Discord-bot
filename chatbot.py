import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv
#import json

"""
Add a command that lets you input a prompt and it generates a picture
Add a commamd that uses image recognition for screenshots.
"""
load_dotenv()
apikey=os.environ['GPT']

class Chatbot(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def chat(self, ctx: commands.Context, *, prompt:str):
        async with aiohttp.ClientSession() as session:
            payload= {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5,
                "max_tokens": 50,
                "presence_penalty": 0,
                "frequency_penalty": 0
            }
            headers = {"Authorization": f"Bearer {apikey}"}
            async with session.post("https://api.openai.com/v1/chat/completions", json=payload, headers=headers) as resp:
                response = await resp.json()
                #print(json.dumps(response,indent=4))
                embed = discord.Embed(title="Chat GPT's Response:", description=response["choices"][0]["message"]["content"])
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Chatbot(bot))