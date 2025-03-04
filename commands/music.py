import discord
from discord.ext import commands
import yt_dlp
import os

YTDLP_OPTS = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

FFMPEG_OPTS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

class MusicCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}

    @commands.command()
    @commands.check_any(commands.is_owner(), commands.guild_only())
    async def play(self, ctx, *, url: str = None):
        url = url or os.getenv('YOUTUBE_URL')
        
        voice_client = ctx.voice_client
        if not voice_client:
            if ctx.author.voice:
                voice_client = await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("You need to be in a voice channel.")

        with yt_dlp.YoutubeDL(YTDLP_OPTS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['url']

        voice_client.stop()
        voice_client.play(discord.FFmpegPCMAudio(url2, **FFMPEG_OPTS))
        await ctx.send(f"Now playing: {info.get('title', 'Unknown Title')}")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
            ctx.voice_client.stop()
            await ctx.voice_client.disconnect()
            await ctx.send("Stopped playback.")

async def setup(bot):
    await bot.add_cog(MusicCommands(bot))