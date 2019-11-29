import asyncio

import discord
from discord.ext import commands
from db.serverRepo import saveServer
from db.userRepo import createUser, createUsers
from util.params import getEnvVariable


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def backgroundTask(self):
        await self.bot.wait_until_ready()
        counter = 0
        status_chan_id = int(getEnvVariable('STATUS_ROOM'))
        loggingChannel = self.bot.get_channel(status_chan_id)

        await loggingChannel.send('bot is online')
        while not self.bot.is_closed():
            await asyncio.sleep(60 * 5)
            counter += 5
            print(counter)
            await loggingChannel.send(f'bot has been online for {counter} minutes.')

    @commands.Cog.listener(name='on_guild_join')
    async def onServerJoin(self, server):
        saveServer(str(server.id))

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(activity=discord.Game(name='with myself'))
        self.bot.loop.create_task(self.backgroundTask())
        for server in self.bot.guilds:
            saveServer(str(server.id))
        createUsers(self.bot.get_all_members())
        print(f'We have logged in as {self.bot.user}')

    @commands.Cog.listener(name='on_member_join')
    async def onMemberJoin(self, member):
        createUser(str(member.id), str(member))
