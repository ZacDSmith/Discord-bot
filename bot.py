import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
from datetime import datetime
import json

load_dotenv()

intents = discord.Intents.all()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)


async def main():
    join_times = {}

    @bot.event
    async def on_voice_state_update(member, before, after):
        # Check if the user has joined a voice channel
        if before.channel is None and after.channel is not None:
            join_times[member.name] = datetime.now()

        # Check if the user has left a voice channel
        elif before.channel is not None and after.channel is None:
            if member.name in join_times:
                join_duration = datetime.now() - join_times[member.name]
                print(f"User {member.name} was in the voice channel for {join_duration}")
                total_time = {f"{join_duration}": {"name": member.name}}
                with open('time.json', 'w') as f:
                    json.dump(total_time, f, indent=4)
                del join_times[member.name]

    await bot.load_extension("event")
    await bot.load_extension("commands")
    await bot.load_extension("shop")
    await bot.load_extension("chatbot")
    #await bot.load_extension("music")
    #await bot.load_extension("imageai")
    await bot.load_extension("ticket")
    await bot.start(token=os.environ['TOKEN'])


asyncio.run(main())
