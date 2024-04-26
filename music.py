import urllib.request
import discord
from discord.ext import commands
from pytube import YouTube
import urllib
import re




FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
client = discord.Client(intents=discord.Intents.all())
class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.voice_client = None
        self.is_playing = False

    @commands.command()
    async def play(self,ctx:commands.Context, url: str):
        try:    
            voice_channel = ctx.author.voice.channel 
            if self.is_playing:
                vc = self.voice_client
            else:
                vc = await voice_channel.connect()
            self.is_playing = True
            self.voice_client = vc
            html = urllib.request.urlopen(url)
            video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())
            await ctx.message.delete()
            await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            vc.pause()
            vc.play(discord.FFmpegPCMAudio(executable="C:/Users/Ratfi/OneDrive/Desktop/ffmpeg-2024-04-21-git-20206e14d7-full_build/bin/ffmpeg.exe", source=f"{stream.url}", **FFMPEG_OPTIONS))
            await ctx.send('Now playing...')
        except Exception as e:
            print(e)

    @commands.command()
    async def stop(self,ctx: commands.Context):
        try:
            await ctx.voice_client.disconnect()
            await ctx.send('Stopped...')
            self.is_playing = False
        except Exception as e:
             print(e)    

    @commands.command()
    async def pause(self,ctx: commands.Context):
        self.voice_client.pause()
        await ctx.message.delete()
        await ctx.send('Paused...')
        self.is_playing = False

    @commands.command()
    async def resume(self, ctx):
        await ctx.message.delete()
        self.voice_client.resume()
        await ctx.send('Resumed...')
        self.is_playing = True

async def setup(bot):
    await bot.add_cog(Music(bot))