import discord
from event import Event
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

intents = discord.Intents.default()
intents.message_content = True

async def main():
    await bot.load_extension("event")
    await bot.load_extension("commands")
    await bot.load_extension("shop")
    await bot.load_extension("chatbot")
    await bot.start(token=os.environ['TOKEN'])

asyncio.run(main())