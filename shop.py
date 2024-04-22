import discord
from discord.ext import commands
import sqlite3
import random
import itertools


class Shop(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def additem(self, ctx: commands.Context, name:str, price:int, decscription:str):
        try:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"INSERT INTO items(name, price, description) Values (?, ? ,?)", (name, price, decscription))
            db.commit()
            embed = discord.Embed(color=discord.Color.random())
            embed.add_field(name="Item", value=f"'{name}'")
            embed.add_field(name="Price", value=f"'{price}'")
            embed.add_field(name="Desc", value=f"'{decscription}'")
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    @commands.command()
    async def shop(self, ctx: commands.Context):
        try:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT name, price, description FROM items")
            items = cursor.fetchall()
            
            
            embed = discord.Embed(color=discord.Color.random())
            for item in items:
                embed.add_field(name=item[0], value=f"Desc: {item[2]}\nPrice: {item[1]}", inline=False)
                
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()
    @commands.command()
    async def buy(self, ctx: commands.Context, name):
        """
        1. Subtract price from Wallet
        2. Display item purchased
        3. Show inventory after purchase
        """
        try:
            member = ctx.author
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT wallet FROM main WHERE user_id = {member.id}")
            wallet = cursor.fetchone()
            try:
                wallet = wallet[0]
        
            except:
                wallet = 0

            #cursor.execute(f"SELECT name, price FROM items")
            cursor.execute(f"SELECT name FROM items WHERE name = ?", (name,))
            cursor.execute("INSERT INTO inv(user_id, item) Values(?,?)",(member.id, name))
            db.commit()
            

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()
            


    """
    Check Inventory Command
    @commands.command()
    async def inv(self, ctx: commands.Context):
        member = ctx.author
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT item FROM inv WHERE user_id = {member.id}")
        """

async def setup(bot):
    await bot.add_cog(Shop(bot))