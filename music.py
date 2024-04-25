import urllib.request
import discord
from discord.ext import commands
from pytube import YouTube
import urllib
import re
import ffmpeg



FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}

client = discord.Client(intents=discord.Intents.all())
#vc = discord.VoiceClient
class Music(commands.Cog):

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def join(self,ctx: commands.Context):
        voice_channel = ctx.author.voice.channel
        if ctx.author.voice is None:
            await ctx.send("You're not in a voice channel!")
        else:
            print(voice_channel)
            await voice_channel.connect()
        
    @commands.command()
    async def disconnect(self,ctx: commands.Context):
        await vc.disconnect()


    @commands.command()
    async def play(self,ctx:commands.Context, url: str):
        try:



            html = urllib.request.urlopen(url)
            video_ids = re.findall(r"watch\?v=(\S{11})",html.read().decode())


            
            #await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])
            yt = YouTube(url)

            stream = yt.streams.filter(only_audio=True).first()
            voice_channel = ctx.author.voice.channel  # converts the youtube audio source into a source discord can use
            vc = await voice_channel.connect()
            #need a ffmpeg.exe or something
            vc.play(discord.FFmpegPCMAudio(executable="C:/Users/Ratfi/OneDrive/Desktop/ffmpeg-2024-04-21-git-20206e14d7-full_build/bin/ffmpeg.exe", source=f"{stream.url}", **FFMPEG_OPTIONS))
            await ctx.send('Now playing...')
        except Exception as e:
            print(e)

    @commands.command()
    async def pause(self,ctx: commands.Context):
        await vc.pause()
        await ctx.send("paused")

    @commands.command()
    async def pause(self,ctx: commands.Context):
        await vc.resume()
        await ctx.send("resumed")



async def setup(bot):
    await bot.add_cog(Music(bot))