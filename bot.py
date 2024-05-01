import discord
from event import Event
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=discord.Intents.all())

intents = discord.Intents.all()
intents.message_content = True

async def main():
    await bot.load_extension("event")
    await bot.load_extension("commands")
    await bot.load_extension("shop")
    await bot.load_extension("chatbot")
    await bot.load_extension("music")
    await bot.load_extension("imageai")
    await bot.load_extension("ticket")
    await bot.start(token=os.environ['TOKEN'])

asyncio.run(main())