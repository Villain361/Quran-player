import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.checks import is_allowed
from commands.music import MusicCommands
from flask import Flask

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return "Quran Bot is running!"

class QuranBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(
            command_prefix=os.getenv('PREFIX'),
            intents=intents,
            help_command=None
        )

    async def setup_hook(self):
        await self.add_cog(MusicCommands(self))

bot = QuranBot()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.check
async def global_check(ctx):
    allowed_users = list(map(int, os.getenv('ALLOWED_USER_IDS', '').split(',')))
    return ctx.author.id in allowed_users

def run():
    import threading
    threading.Thread(target=app.run, kwargs={'host': '0.0.0.0', 'port': 8080}).start()
    bot.run(os.getenv('TOKEN'))

if __name__ == "__main__":
    run()