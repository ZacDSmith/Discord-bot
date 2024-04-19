import asyncio
import discord
from discord.ext import commands
import sqlite3
import random
import datetime


class Commands(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def balance(self, ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author

        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT wallet, bank FROM main WHERE user_id = {member.id}")
        bal = cursor.fetchone()
        try:
            wallet = bal[0]
            bank = bal[1]
        except:
            wallet = 0
            bank = 0

        await ctx.send(f"Wallet -- {wallet}\nBank -- {bank}")


    @commands.command(name="bal")
    async def bal(self,ctx, member:discord.Member = None):
        if member is None:
            member = ctx.author
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT wallet, bank FROM main WHERE user_id = {member.id}")
        bal = cursor.fetchone()


        embed = discord.Embed(color=discord.Color.random())
        embed.set_author(icon_url=ctx.author.avatar, name=f"{ctx.author.name} Bank account")
        embed.add_field(name="Wallet", value=f"'💸{bal[0]}'")
        embed.add_field(name="Bank", value=f"'💸{bal[1]}'")
        embed.add_field(name="Networth", value=f"'💸{bal[0] + bal[1]}'")
        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1138/1138038.png")
        embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
        await ctx.send(embed=embed)


    @commands.command()
    async def earn(self,ctx):
        member = ctx.author

        earnings = random.randint(1, 5)
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()

        cursor.execute(f"SELECT wallet FROM main WHERE user_id = {member.id}")
        wallet = cursor.fetchone()
        try:
            wallet = wallet[0]
    
        except:
            wallet = 0


        sql = ("UPDATE main SET wallet = ? WHERE user_id = ?")
        val = (wallet + int(earnings), member.id)
        cursor.execute(sql, val)
        await ctx.send(f"You have earned {earnings}")

        db.commit()
        cursor.close()
        db.close()

async def setup(bot):
    await bot.add_cog(Commands(bot))