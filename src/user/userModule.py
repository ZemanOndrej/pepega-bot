import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from db.serverRepo import getServerById
from db.userRepo import getUsers, incUserMsgCount, updateUserKarma
from db.karmaRepo import getKarmaEmoteByServerAndReaction, createKarmaEmote
from util.utilService import extractEmoteFromMessage, getEmojiIdFromPayloadEmoji


class UserModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leaderboard")
    async def leaderBoard(self, ctx, count=20):
        leaderBoard = getUsers(count)
        parsedLeaderboard = ''
        for user in leaderBoard:
            parsedLeaderboard += f"{user.name}: msgCount={user.message_count}, karma={user.karma}\n"

        await ctx.send(f"```{parsedLeaderboard}```")

    @commands.Cog.listener()
    async def on_message(self, message):
        incUserMsgCount(message.author)

    @commands.command(name="addKarmaReaction")
    async def addKarmaEmote(self, ctx,  reaction, val: int):
        createKarmaEmote(str(ctx.message.guild.id),
                         extractEmoteFromMessage(reaction), val)

    @commands.Cog.listener(name='on_raw_reaction_remove')
    async def onReactionRemove(self, payload: discord.RawReactionActionEvent):
        chn = self.bot.get_channel(payload.channel_id)
        msg = await chn.fetch_message(payload.message_id)
        if payload.user_id == msg.author.id:
            return
        serverId = str(payload.guild_id)
        emoji = getEmojiIdFromPayloadEmoji(payload.emoji)

        karmaEmote = getKarmaEmoteByServerAndReaction(serverId, emoji)
        if karmaEmote is not None:
            updateUserKarma(str(msg.author.id), -karmaEmote.karmaChange)

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def onReactionAdd(self, payload: discord.RawReactionActionEvent):
        chn = self.bot.get_channel(payload.channel_id)
        msg = await chn.fetch_message(payload.message_id)
        if payload.user_id == msg.author.id:
            return

        serverId = str(payload.guild_id)
        emoji = getEmojiIdFromPayloadEmoji(payload.emoji)

        karmaEmote = getKarmaEmoteByServerAndReaction(serverId, emoji)
        if karmaEmote is not None:
            updateUserKarma(str(msg.author.id), karmaEmote.karmaChange)
