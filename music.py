import asyncio
import os.path
import discord
from discord.ext import commands
from pytubefix import YouTube
from discord import File
import yt_dlp

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
voice_clients = {}
yt_dl_options = {"format": "bestaudio/best"}
ytdl = yt_dlp.YoutubeDL(yt_dl_options)

#FFMPEG_OPTIONS = {'options': '-vn'}

class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.voice_client = None
        self.is_playing = False

    @commands.command(name="play", help="plays youtube audio by url")
    async def play(self, ctx):
        try:
            voice_client = await ctx.message.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except Exception as e:
            print(e)

        try:
            url = ctx.message.content.split()[1]
            loop = asyncio.get_event_loop()
            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))
            song = data['url']
            player = discord.FFmpegPCMAudio(song, **FFMPEG_OPTIONS)
            voice_clients[ctx.message.guild.id].play(player)
            await ctx.message.delete()
            await ctx.send(f"{url} now playing!")

        except Exception as e:
            print(e)



    @commands.command(name="download", help="Downloads MP3 from youtube")
    async def download(self, ctx: commands.Context, url: str):
        try:
            await ctx.message.delete()
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            destination = ''
            out_file = stream.download(output_path=destination)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            file = File(new_file)
            await ctx.send(file=file)
            os.remove(new_file)
        except Exception as e:
            os.remove(new_file)
            await ctx.send("Error! Deleting System 32 now.")
            print(e)

    @commands.command(name="stop", help="stops the audio")
    async def stop(self, ctx: commands.Context):
        try:
            await ctx.voice_client.disconnect()
            await ctx.send('Stopped...')
            self.is_playing = False
        except Exception as e:
            print(e)

    @commands.command(name="pause", help="pauses the audio")
    async def pause(self, ctx: commands.Context):
        self.voice_client.pause()
        await ctx.message.delete()
        await ctx.send('Paused...')
        self.is_playing = False

    @commands.command(name="resume", help="resumes the audio")
    async def resume(self, ctx):
        await ctx.message.delete()
        self.voice_client.resume()
        await ctx.send('Resumed...')
        self.is_playing = True


async def setup(bot):
    await bot.add_cog(Music(bot))
