"""
setup ticket command:
    create text channel for create_ticket
    change where no one can message in channel

ticket system:
    Basic embed with information and create ticket button
    button creates text channel thats only visble to button clicker and admins
    ping user in ticket channel with basic embed that says ticket has been created.
"""


"""
NEED THE BOT VARIABLE TO MAKE THIS WORK PROPERLY BUT IT THROWS ERROR:
RuntimeError: asyncio.run() cannot be called from a running event loop
tried from bot import bot
"""
from discord.ext import commands
import discord
class Ticket(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context):
        try:
            guild = ctx.message.guild
            ticket_channel_create = await guild.create_text_channel('ticket-channel')
            channel = discord.utils.get(ctx.guild.channels, name=f"{ticket_channel_create}")
            channel_id = channel.id
            ticket_channel = bot.get_channel(channel_id)
            await ticket_channel.send("test")
        except Exception as e:
            print(e)
async def setup(bot):
    await bot.add_cog(Ticket(bot))