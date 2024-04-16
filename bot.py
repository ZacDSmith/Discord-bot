import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('OTg3MTQ4ODMxOTk5Mjk1NDg4.GF9qCx._yoIk8w7XsCTd4Nn5z-ShCe8ylxc-qUc3QkLko')