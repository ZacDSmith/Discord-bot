import discord
from discord.ext import commands
import aiohttp
import os
from dotenv import load_dotenv
import ollama

load_dotenv()
apikey = os.environ['GPT']
clients = ollama.Client()


class Chatbot(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    # @commands.command(name="chat", help="Responds to a prompt entered by the user.")
    # async def chat(self, ctx: commands.Context, *, prompt: str):
    #     try:
    #         async with aiohttp.ClientSession() as session:
    #             payload = {
    #                 "model": "gpt-3.5-turbo",
    #                 "messages": [{"role": "user", "content": prompt}],
    #                 "temperature": 0.5,
    #                 "max_tokens": 50,
    #                 "presence_penalty": 0,
    #                 "frequency_penalty": 0
    #             }
    #             headers = {"Authorization": f"Bearer {apikey}"}
    #             async with session.post("https://api.openai.com/v1/chat/completions", json=payload,
    #                                     headers=headers) as resp:
    #                 response = await resp.json()
    #                 embed = discord.Embed(title="Chat GPT's Response:",
    #                                       description=response["choices"][0]["message"]["content"])
    #                 await ctx.send(embed=embed)
    #     except Exception as e:
    #         print(e)
    def split_string_every_2000_chars(input_string):
        return [input_string[i:i + 2000] for i in range(0, len(input_string), 2000)]

    @commands.command(name="google", description="ai chatbot that can write code.")
    async def google(self, ctx, prompt: str):
        model = "deepseek-r1:8b"
        try:
            response = clients.generate(model=model, prompt=prompt)
            #input_string = response.response  # replace with your string
            #chunks = split_string_every_2000_chars(input_string)
            await ctx.send(f"Prompt: {prompt}. \n Response:")
            #for chunk in chunks:
                #await ctx.send(f"{chunk}")
            await ctx.send(f"Prompt: {prompt}. \n Response: {response.response}")
        except Exception as e:
            print("Error occurred: ", e)


async def setup(bot):
    await bot.add_cog(Chatbot(bot))
