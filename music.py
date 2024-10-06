import urllib.request
import discord
from discord.ext import commands
from pytubefix import YouTube
import urllib
from pytubefix import cipher
import re


def get_throttling_function_name(js: str) -> str:
    """Extract the name of the function that computes the throttling parameter.

    :param str js:
        The contents of the base.js asset file.
    :rtype: str
    :returns:
        The name of the function used to compute the throttling parameter.
    """
    function_patterns = [
        # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
        # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
        # var Bpa = [iha];
        # ...
        # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
        # Bpa.length || iha("")) }};
        # In the above case, `iha` is the relevant function name
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&\s*'
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])\([a-z]\)',
    ]
    # logger.debug('Finding throttling function name')
    for pattern in function_patterns:
        regex = re.compile(pattern)
        function_match = regex.search(js)
        if function_match:
            # logger.debug("finished regex search, matched: %s", pattern)
            if len(function_match.groups()) == 1:
                return function_match.group(1)
            idx = function_match.group(2)
            if idx:
                idx = idx.strip("[]")
                array = re.search(
                    r'var {nfunc}\s*=\s*(\[.+?\]);'.format(
                        nfunc=re.escape(function_match.group(1))),
                    js
                )
                if array:
                    array = array.group(1).strip("[]").split(",")
                    array = [x.strip() for x in array]
                    return array[int(idx)]

    raise RegexMatchError(
        caller="get_throttling_function_name", pattern="multiple"
    )


cipher.get_throttling_function_name = get_throttling_function_name

FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
client = discord.Client(intents=discord.Intents.all())


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
