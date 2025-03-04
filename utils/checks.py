from discord.ext import commands
import os

def is_allowed():
    async def predicate(ctx):
        allowed_users = list(map(int, os.getenv('ALLOWED_USER_IDS', '').split(',')))
        if ctx.author.id not in allowed_users:
            await ctx.send("You are not authorized to use this bot.")
            return False
        return True
    return commands.check(predicate)