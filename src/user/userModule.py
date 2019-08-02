import discord
from discord.ext import commands
from discord.ext.commands import has_permissions


from db.userRepo import getUsers, incUserMsgCount


class UserModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leaderboard")
    async def leaderBoard(self, ctx, count=20):
        leaderBoard = getUsers(count)
        parsedLeaderboard = ''
        for key in leaderBoard:
            parsedLeaderboard += f"{key.name}: {key.message_count}\n"

        await ctx.send(f"```{parsedLeaderboard}```")

    @commands.Cog.listener()
    async def on_message(self, message):
        incUserMsgCount(message.author)
