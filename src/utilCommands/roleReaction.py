import asyncio
import discord
from discord.ext import commands


class RoleReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # TODO add database for this shit
    @commands.command(name="roleReaction")
    async def role(self, ctx, room: discord.TextChannel):
        print('not implemented')
