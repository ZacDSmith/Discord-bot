from discord.ext import commands
import sqlite3


class Event(commands.Cog):

    @commands.Cog.listener()
    async def on_ready(self):
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS main (
                       user_id INTEGER, wallet INTEGER, bank INTEGER
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                       items TEXT, price INTEGER, description TEXT, id INTEGER PRIMARY KEY
        )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS inv (
                       user_id INTEGER, item TEXT, id INTEGER PRIMARY KEY, count INTEGER
        )''')
        print("Bot Online.")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        author = message.author
        db = sqlite3.connect("main.sqlite")
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM main WHERE user_id = {author.id}")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main(user_id, wallet, bank) VALUES (?, ? ,?)")
            val = (author.id, 100, 0)
            cursor.execute(sql, val)

        db.commit()
        cursor.close()
        db.close()


async def setup(bot):
    await bot.add_cog(Event(bot))
