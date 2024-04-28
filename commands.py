import discord
from discord.ext import commands
import sqlite3
import random
import datetime

class Commands(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command(name="bal")
    async def bal(self,ctx, member:discord.Member = None):
        try:
            if member is None:
                member = ctx.author
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT wallet, bank FROM main WHERE user_id = {member.id}")
            bal = cursor.fetchone()

            embed = discord.Embed(color=discord.Color.random())
            embed.set_author(icon_url=member.avatar, name=f"{member.name} Bank account")
            embed.add_field(name="Wallet", value=f"💸{bal[0]}")
            embed.add_field(name="Bank", value=f"💸{bal[1]}")
            embed.add_field(name="Networth", value=f"💸{bal[0] + bal[1]}")
            embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1138/1138038.png")
            embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
      
    @commands.command()
    async def deposit(self, ctx: commands.Context, amount: int):
        try:
            member = ctx.author
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT wallet, bank FROM main WHERE user_id = {member.id}")

            bal = cursor.fetchone()
            try:
                wallet = bal[0]
                bank = bal[1]
        
            except:
                wallet = wallet
                bank = bank
            
            if amount < 0:
                return await ctx.send("Enter Valid Number")
            elif wallet < amount:
                await ctx.send ("Not enough cash")
            elif wallet >= amount:
                new_wallet_amt: int = wallet - amount
                new_bank_amt: int = bank + amount

                cursor.execute(f"UPDATE main SET wallet = {new_wallet_amt}, bank = {new_bank_amt} WHERE user_id = {member.id}")
                db.commit()

                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(icon_url=member.avatar, name=f"{member.name} Bank account")
                embed.add_field(name="Wallet", value=f"💸{new_wallet_amt}")
                embed.add_field(name="Bank", value=f"💸{new_bank_amt}")
                embed.add_field(name="Networth", value=f"💸{new_wallet_amt + new_bank_amt}")
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1138/1138038.png")
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                await ctx.send(embed=embed)

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    @commands.command()
    async def withdraw(self, ctx: commands.Context, amount: int=1):
        try:
            member = ctx.author
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT wallet, bank FROM main WHERE user_id = {member.id}")

            bal = cursor.fetchone()
            try:
                wallet = bal[0]
                bank = bal[1]
        
            except:
                await ctx.send ("There is an error")
            if amount < 0:
                return await ctx.send("Enter Valid Number")
            elif bank < amount:
                await ctx.send ("Not enough cash")
            elif bank >= amount:
                new_wallet_amt: int = wallet + amount
                new_bank_amt: int = bank - amount

                cursor.execute(f"UPDATE main SET wallet = {new_wallet_amt}, bank = {new_bank_amt} WHERE user_id = {member.id}")
                db.commit()

                embed = discord.Embed(color=discord.Color.random())
                embed.set_author(icon_url=member.avatar, name=f"{member.name} Bank account")
                embed.add_field(name="Wallet", value=f"💸{new_wallet_amt}")
                embed.add_field(name="Bank", value=f"💸{new_bank_amt}")
                embed.add_field(name="Networth", value=f"💸{new_wallet_amt + new_bank_amt}")
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1138/1138038.png")
                embed.timestamp = datetime.datetime.now(datetime.timezone.utc)
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    @commands.command()
    async def mine(self,ctx):
        try:
            member = ctx.author

            earnings = random.randint(1, 999)
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()

            cursor.execute(f"SELECT wallet FROM main WHERE user_id = {member.id}")
            db.commit()
            wallet = cursor.fetchone()
            try:
                wallet = wallet[0]
        
            except:
                wallet = wallet
            try:
                new_wallet_amt: int = wallet + earnings
                cursor.execute(f"UPDATE main SET wallet = {wallet + int(earnings)} WHERE user_id = {member.id}")
                db.commit()
                embed = discord.Embed(color=discord.Color.random())
                embed.add_field(name="You Mined:", value=f"💸{earnings}", inline=False)
                embed.add_field(name="New Wallet Amount:", value=f"💸{new_wallet_amt}")
                embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/1231812202533752884/1234231239708250253/mining-cart.png?ex=662ffaea&is=662ea96a&hm=faaee8da09e77565069865f0f0f0485d204333de421cc17110beeb4e862dfc10&")
                await ctx.send(embed=embed)
            except Exception as E:
                print(E)

        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    @commands.command()
    async def gamble(self, ctx: commands.Context, amount:int=0):
        try:
            member = ctx.author
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT wallet FROM main WHERE user_id = {member.id}")
            wallet = cursor.fetchone()
            try:
                wallet = wallet[0]
        
            except:
                wallet = wallet

            if amount <= 10:
                return await ctx.send("Please enter a number above 10")
            if wallet < amount:
                return await ctx.send("You don't have enough money.")
            
            user_strikes = random.randint(1, 15)
            bot_strikes = random.randint(8, 15)

            """gets bots nickname based on specific server. 
            https://discordpy.readthedocs.io/en/stable/api.html#client"""
            guild = await self.bot.fetch_guild(1038514358390632489)
            bot_member = await guild.fetch_member(987148831999295488)


            if user_strikes > bot_strikes:
                percentage = random.randint(50, 100)
                amount_won = int(amount*(percentage/100))
                cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet + amount_won, member.id))
                db.commit()
                embed = discord.Embed(description=f"You Won! **{amount_won}**\nPercentage **{percentage}%**\nNew Balance **{wallet + amount_won}**", color=discord.Color.green())
                embed.set_author(name=f"Wow {member.name} You are a pro!", icon_url=ctx.author.avatar)

            elif user_strikes < bot_strikes:
                percentage = random.randint(0, 80)
                amount_lost = int(amount*(percentage/100))
                cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet - amount_lost, member.id))
                db.commit()
                embed = discord.Embed(description=f"You Lost! **{amount_lost}**\nPercentage **{percentage}%**\nNew Balance **{wallet - amount_lost}**", color=discord.Color.red())
                embed.set_author(name=f"Shit Play {member.name}!", icon_url=ctx.author.avatar)
            else:
                embed = discord.Embed(description=f"**It was a tie**", color=discord.Color.orange())
                embed.set_author(name=f"Shit Play {member.name}!", icon_url=ctx.author.avatar)

            embed.add_field(name=f"**{member.name.title()}**", value=f"Strikes {user_strikes}")
            embed.add_field(name=f"**{bot_member.nick}**", value=f"Strikes {bot_strikes}")
            await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

    @commands.command()
    async def slots(self, ctx, amount:int=10):
        try:
            member = ctx.author
            db = sqlite3.connect("main.sqlite")
            cursor = db.cursor()
            cursor.execute(f"SELECT wallet FROM main WHERE user_id = {member.id}")
            wallet = cursor.fetchone()
            try:
                wallet = wallet[0]
            except:
                wallet = wallet

            if amount < 9:
                return await ctx.send("You need at least $10")
            if wallet < amount:
                return await ctx.send("You don't have enough $$$")
            
            times_factors = random.randint(1, 5)
            earning = int(amount*times_factors)

            final = []
            for i in range(3):
                a = random.choice(["🍉","💎", "💰"])
                final.append(a)
            if final[0] == final[1] or final[0] == final[2] or final[2] == final[0]:
                cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet + earning, member.id))
                db.commit()
                embed = discord.Embed(title=f"Slot Machine", color= discord.Color.green())
                embed.add_field(name=f"You Won 💸{earning}", value=f'{final}')
                embed.add_field(name=f"---------------------------------", value=f"**Multiplier** x{times_factors}", inline=False)
                embed.add_field(name=f"---------------------------------", value=f"**New Balance** 💸{wallet + earning}", inline=False)
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
                await ctx.send(embed=embed)
            else:
                cursor.execute("UPDATE main SET wallet = ? WHERE user_id = ?", (wallet - amount, member.id))
                db.commit()
                embed = discord.Embed(title=f"Slot Machine", color= discord.Color.red())
                embed.add_field(name=f"You Lost 💸{amount}", value=f'{final}')
                embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/1055/1055823.png")
                await ctx.send(embed=embed)
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            db.close()

async def setup(bot):
    await bot.add_cog(Commands(bot))