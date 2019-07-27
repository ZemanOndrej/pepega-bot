import asyncio

import discord
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def backgroundTask(self):
        await self.bot.wait_until_ready()
        counter = 0
        loggingChannel = self.bot.get_channel(604220508267085824)

        await loggingChannel.send("bot is online")
        while not self.bot.is_closed():
            await asyncio.sleep(60 * 5)
            print(counter)
            counter += 5
            await loggingChannel.send(f"bot has been online for {counter} minutes.")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name="with myself"))
        self.bot.loop.create_task(self.backgroundTask())
        print(f'We have logged in as {self.bot.user}')

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.process_commands(message)
