import asyncio
import json
from pathlib import Path

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

from src.config import CONFIG
from src.util.params import getArgDict
from src.util.timeUtils import cd


class UtilCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.leaderBoardPath = Path(
            CONFIG['leaderboardPath'] if CONFIG['leaderboardPath'] else './leaderboard.json')
        self.leaderBoard = {}

    @commands.command(name='countdown')
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

    @commands.command(name="leaderboard")
    async def leaderBoard(self, ctx):
        parsedLeaderboard = ''
        for key in sorted(self.leaderBoard, key=self.leaderBoard.get, reverse=True):
            parsedLeaderboard += f"{key}: {self.leaderBoard[key]}\n"

        await ctx.send(f"```{parsedLeaderboard}```")

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.leaderBoardPath.is_file():
            self.leaderBoard = {}
        else:
            with open(self.leaderBoardPath) as file:
                self.leaderBoard = json.loads(file.read())
        self.bot.loop.create_task(self.backgroundSaving())

    @commands.Cog.listener()
    async def on_message(self, message):
        authorId = str(message.author)
        if authorId in self.leaderBoard:
            self.leaderBoard[authorId] += 1
        else:
            self.leaderBoard[authorId] = 1

    @commands.Cog.listener()
    async def on_disconnect(self):
        print('pepega was disconnected')
        self.saveLeaderboard()

    async def backgroundSaving(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            await asyncio.sleep(30)
            print('saving leaderboard')
            self.saveLeaderboard()

    def saveLeaderboard(self):
        with open(self.leaderBoardPath, '+w') as file:
            file.write(json.dumps(self.leaderBoard))
