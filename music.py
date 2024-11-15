import os.path
import urllib.request
import discord
from discord.ext import commands
from pytubefix import YouTube
import urllib
import re
from discord import File

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


class Music(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.voice_client = None
        self.is_playing = False

    @commands.command(name="play", help="plays youtube audio by url")
    async def play(self, ctx: commands.Context, url: str):
        try:
            voice_channel = ctx.author.voice.channel
            if self.is_playing:
                vc = self.voice_client
            else:
                vc = await voice_channel.connect()
            self.is_playing = True
            self.voice_client = vc
            html = urllib.request.urlopen(url)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            await ctx.message.delete()
            await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            vc.pause()
            ## YOU HAVE TO DOWNLOAD THE ffmpeg.exe AND CHANGE THE FILE PATH TO YOURS.
            vc.play(discord.FFmpegPCMAudio(
                executable="C:/Program Files (x86)/ffmpeg-2024-04-21-git-20206e14d7-full_build/bin/ffmpeg.exe",
                source=f"{stream.url}", **FFMPEG_OPTIONS))
            await ctx.send('Now playing...')
        except Exception as e:
            print(e)

    @commands.command(name="download", help="Downloads MP3 from youtube")
    async def download(self, ctx: commands.Context, url: str):
        try:
            await ctx.message.delete()
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            destination = '.'
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
