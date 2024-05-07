import discord
from discord.ext import commands
import sqlite3
import datetime

class Shop(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="additem", help="Add an item to the DB (ADMIN ONLY)")
    @commands.has_permissions(administrator=True)
    async def additem(self, ctx: commands.Context, name:str, price:int, *, decscription: str):
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

    @commands.command(name="removeitem", help="Remove an item from the DB (ADMIN ONLY)")
    @commands.has_permissions(administrator=True)
    async def removeitem(self, ctx: commands.Context, name:str):
        try:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"DELETE FROM inv WHERE item = ?", (name,))
            db.commit()
            cursor.execute(f"DELETE FROM items WHERE name = ?", (name,))
            db.commit()
            embed = discord.Embed(color=discord.Color.red())
            embed.add_field(name=f"REMOVED ITEM : {name}", value=f"")
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    @commands.command(name="shop", help="Displays items in the DB with name, price, descrip")
    async def shop(self, ctx: commands.Context):
        try:
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT name, price, description FROM items")
            items = cursor.fetchall()

            embed = discord.Embed(color=discord.Color.random())
            for item in items:
                embed.add_field(name=item[0], value=f"{item[2]}\n💸{item[1]}", inline=False)
                
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    @commands.command(name="buy", help="Buy an item from the shop")
    async def buy(self, ctx: commands.Context, name):
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

            cursor.execute(f"SELECT name FROM items WHERE name = ?", (name,))
            itemconfirm = cursor.fetchall()
            if len(itemconfirm) == 0:
                embed = discord.Embed(color=discord.Color.red())
                embed.set_author(icon_url=member.avatar, name=f"{member.name} must be smoking that reefer.")
                embed.add_field(name=f"**Item doesn't exist**", value="")
                await ctx.send(embed=embed)
                return
            cursor.execute(f"SELECT count FROM inv WHERE user_id = ? AND item = ?" , (member.id, name))
            count: tuple = cursor.fetchall()
            if len(count) == 0:    
                cursor.execute("INSERT INTO inv(user_id, item, count) Values(?,?,?)",(member.id, name, 1))
            else:
                cursor.execute("UPDATE inv SET count = ? WHERE user_id = ? AND item = ?",(count[0][0] + 1, member.id, name))
            cursor.execute(f"SELECT items.price, items.name, inv.item FROM items, inv WHERE user_id = {member.id} AND inv.item = items.name")
            purchase = cursor.fetchall()
            try:
                price = purchase[0]
            except:
                price = price


            if wallet < price[0]:
                await ctx.send ("Not enough cash")
                return
            elif wallet >= price[0]:
                new_wallet_amt: int = wallet - price[0]
            cursor.execute(f"UPDATE main SET wallet = {new_wallet_amt} WHERE user_id = {member.id}") 
            db.commit()

            embed = discord.Embed(color=discord.Color.random())
            embed.set_author(icon_url=member.avatar, name=f"{member.name} Purchased {name}")
            embed.add_field(name="Wallet", value=f"'💸{new_wallet_amt}'")
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await ctx.send(embed=embed)
            
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()
            
    @commands.command(name="sell", help="Sell an item for currency")
    async def sell(self, ctx: commands.Context, name):
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

            cursor.execute(f"SELECT count FROM inv WHERE user_id = ? AND item = ?" , (member.id, name))
            count: tuple = cursor.fetchone()[0]
            if not count > 0:
                return
            cursor.execute("UPDATE inv SET count = ? WHERE user_id = ? AND item = ?",(count - 1, member.id, name))
            cursor.execute(f"SELECT items.price, items.name, inv.item FROM items, inv WHERE user_id = {member.id} AND inv.item = items.name")
            sold = cursor.fetchall()
            try:
                price = sold[0]

            except:
                price = price


            if wallet < price[0]:
                await ctx.send ("Not enough cash")
                return
            elif wallet >= price[0]:
                new_wallet_amt: int = wallet + price[0]
            cursor.execute(f"UPDATE main SET wallet = {new_wallet_amt} WHERE user_id = {member.id}") 
            db.commit()

            embed = discord.Embed(color=discord.Color.red())
            embed.set_author(icon_url=member.avatar, name=f"{member.name} Sold {name}")
            embed.add_field(name="Wallet", value=f"'💸{new_wallet_amt}'")
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await ctx.send(embed=embed)
            
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()
            
    @commands.command(name="inv", help="Check your inv for items you've purchased")
    async def inv(self, ctx: commands.Context):
        try:
            member = ctx.author
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(
                f"SELECT inv.item, items.name, items.description, inv.count FROM inv, items WHERE user_id = {member.id} AND inv.item = items.name AND inv.count > 0 ORDER by 1,2")
            items = cursor.fetchall()
            embed = discord.Embed(color=discord.Color.random())
            for item in items:
                embed.add_field(name=f"{item[0]}  :  {item[3]} ", value=f"Desc: {item[2]}", inline=False)
            embed.set_author(icon_url=member.avatar, name=f"{member.name} Inventory")
            await ctx.send(embed=embed)
            
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

async def setup(bot):
    await bot.add_cog(Shop(bot))