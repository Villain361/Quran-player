import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.youtube import YTDLSource

# Load environment variables
load_dotenv()

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents)

# Get allowed user IDs from .env
allowed_user_ids = list(map(int, os.getenv('ALLOWED_USER_IDS').split(',')))

# Check if the user is allowed
def is_allowed_user(ctx):
    return ctx.author.id in allowed_user_ids

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command(name='play', help='Plays Quran from a YouTube URL')
@commands.check(is_allowed_user)
async def play(ctx, url: str):
    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=bot.loop)
        ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)
    await ctx.send(f'Now playing: {player.title}')

@bot.command(name='join', help='Joins the voice channel')
@commands.check(is_allowed_user)
async def join(ctx):
    if not ctx.message.author.voice:
        await ctx.send(f"{ctx.message.author.name} is not connected to a voice channel")
        return
    channel = ctx.message.author.voice.channel
    await channel.connect()

@bot.command(name='leave', help='Leaves the voice channel')
@commands.check(is_allowed_user)
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()

@bot.command(name='stop', help='Stops the current song')
@commands.check(is_allowed_user)
async def stop(ctx):
    ctx.voice_client.stop()

@play.before_invoke
@join.before_invoke
async def ensure_voice(ctx):
    if ctx.voice_client is None:
        if ctx.author.voice:
            await ctx.author.voice.channel.connect()
        else:
            await ctx.send("You are not connected to a voice channel.")
            raise commands.CommandError("Author not connected to a voice channel.")
    elif ctx.voice_client.is_playing():
        ctx.voice_client.stop()

# Run the bot
bot.run(os.getenv('DISCORD_TOKEN'))
