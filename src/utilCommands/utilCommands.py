import asyncio
import json
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from util.params import getEnvVariable
from util.params import getArgDict
from util.timeUtils import cd


class UtilCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='countdown')
    @has_permissions(administrator=True)
    async def countdown(self, ctx, *args):
        countStart = 0
        try:
            if len(args) > 1:
                countStart = int(getArgDict(args)['time'])
            elif len(args) == 1 and args[0].isnumeric():
                countStart = int(args[0])
        except:
            return await ctx.send("wrong input")
        if countStart > 20:
            return await ctx.send("number is too big!")

        await cd(ctx.send, countStart, 1, "countdown has started", "it is finished")

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send('pong')

    @commands.command(name='purge')
    @has_permissions(administrator=True)
    async def purge(self, ctx, arg):
        if arg.isdigit():
            number = int(arg) + 1
            counter = 0
            while counter < number:
                delNum = 100 if counter + 100 <= number else number - counter
                counter += delNum
                await ctx.channel.purge(limit=delNum, bulk=True)
                await asyncio.sleep(1.2)
        elif arg == 'all':
            while True:
                print('deleting...')
                await ctx.channel.purge(limit=100, bulk=True)
                try:
                    nxt = await ctx.channel.history(limit=1).next()
                except discord.errors.NoMoreItems:
                    break
                await asyncio.sleep(3)

    @commands.Cog.listener()
    async def on_disconnect(self):
        print('pepega was disconnected')
