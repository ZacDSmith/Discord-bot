import discord
from event import Event
from discord.ext import commands
import sqlite3
import random
import asyncio

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

intents = discord.Intents.default()
intents.message_content = True


##bot.run('OTg3MTQ4ODMxOTk5Mjk1NDg4.GF9qCx._yoIk8w7XsCTd4Nn5z-ShCe8ylxc-qUc3QkLko')

async def main():
    await bot.load_extension("event")
    await bot.load_extension("commands")
    await bot.start('OTg3MTQ4ODMxOTk5Mjk1NDg4.GF9qCx._yoIk8w7XsCTd4Nn5z-ShCe8ylxc-qUc3QkLko')

asyncio.run(main())