"""
setup ticket command:
    create text channel for create_ticket
    change where no one can message in channel

ticket system:
    Basic embed with information and create ticket button
    button creates text channel thats only visble to button clicker and admins
    ping user in ticket channel with basic embed that says ticket has been created.
"""
from discord.ext import commands
import discord

class buttons(discord.ui.View):
    def __init__(self): 
        super().__init__()
        self.ticket_number = 0

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.blurple)
    async def ticketbtn(self, interations: discord.Interaction, button: discord.ui.Button):
        try:
            guild = interations.guild
            user = guild.get_member(interations.user.id)
            ticket_channel_create = await guild.create_text_channel(f'{user} Ticket {self.ticket_number}')
            self.ticket_number +=1
            channel = discord.utils.get(guild.channels, name=f"{ticket_channel_create}")
            channel_id = channel.id
            ticket_channel = guild.get_channel(channel_id)
            await ticket_channel.set_permissions(guild.default_role, send_messages=False, view_channel=False)
            await ticket_channel.set_permissions(user, send_messages=True, view_channel=True)
            await ticket_channel.send(user.mention)
            await ticket_channel.send("What is the problem you are having?")
            
        except Exception as e:
            print(e)

class Ticket(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot:commands.Bot = bot
    #
    @commands.command(name="setuptick", help="Sets up the channel that holds the embed for tickets")
    async def setuptick(self, ctx: commands.Context):
        try:
            guild = ctx.message.guild
            ticket_channel_create = await guild.create_text_channel('🎫TICKETS🎫')
            channel = discord.utils.get(ctx.guild.channels, name=f"{ticket_channel_create}")
            channel_id = channel.id
            ticket_channel = self.bot.get_channel(channel_id)
            await ticket_channel.set_permissions(ctx.guild.default_role, send_messages=False)
            embed = discord.Embed(title=f"TICKETS", color= discord.Color.green())
            await ticket_channel.send(embed=embed, view=buttons())


        except Exception as e:
            print(e)


async def setup(bot):
    await bot.add_cog(Ticket(bot))