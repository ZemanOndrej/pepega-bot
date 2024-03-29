import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from db.userRepo import getUsers, incUserMsgCount, updateUserKarma, getUserById, getUserCountWithMoreMessages
from db.karmaRepo import getKarmaReactionByServerAndReaction, saveKarmaReaction, getKarmaReactionsByServer, removeKarmaReaction, removeAllKarmaReactions
from util.utilService import extractEmoteText
from discord.ext.commands import has_permissions
from strings.en_us import strings
import typing
from emoji import UNICODE_EMOJI


class UserModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="leaderboardCheck")
    async def leaderBoardCheck(self, ctx, user: discord.User):
        dbUser = getUserById(str(user.id))
        count = getUserCountWithMoreMessages(dbUser.message_count)
        return await ctx.send(f"`{count+1}. {dbUser.name}: msgCount={dbUser.message_count}, karma={dbUser.karma}`\n")

    @commands.command(name="leaderboard")
    async def leaderBoard(self, ctx, count=20, page=0):
        leaderBoard = getUsers(count, page)
        parsedLeaderboard = parseLeaderboard(leaderBoard, page*count)
        await ctx.send(f"""```Leaderboard:
{parsedLeaderboard}```""")

    @commands.Cog.listener()
    async def on_message(self, message):
        incUserMsgCount(message.author)

    @commands.command(name="karmaInfo", help=strings['help_kr_print'])
    async def karmaInfo(self, ctx):
        karmaReaction = getKarmaReactionsByServer(str(ctx.message.guild.id))
        if len(karmaReaction) == 0:
            return await ctx.send('There are no karma reactions on this server')
        nl = '\n'
        return await ctx.send(
            f"""```KarmaReactions:
{nl.join([f"Reaction {extractEmoteText(x.reaction)} changes your karma by {x.karmaChange}" for x in karmaReaction])}\
            ```""")

    @commands.command(name="saveKarmaReaction", help=strings['help_kr_save'])
    @has_permissions(administrator=True)
    async def addKarmaReaction(self, ctx,  reaction: typing.Union[discord.PartialEmoji, str], value: int):
        if type(reaction) == str and reaction not in UNICODE_EMOJI:
            return await ctx.send(f"Invalid Emote")
        if value>10 or value<-10:
            return await ctx.send(f"Invalid value (-10<value<10)")

        saveKarmaReaction(str(ctx.message.guild.id), str(reaction), value)
        return await ctx.send(f'Reaction {reaction} will change your karma by {value}')

    @commands.command(name="removeKarmaReaction", help=strings['help_kr_remove'])
    @has_permissions(administrator=True)
    async def removeKarmaReaction(self, ctx, reaction):
        removeKarmaReaction(str(ctx.guild.id), reaction)
        return await ctx.send(f"KarmaReaction with {reaction} was removed.")

    @commands.command(name='resetKarmaReaction', help=strings['help_kr_reset'])
    @has_permissions(administrator=True)
    async def resetKarmaReaction(self, ctx):
        removeAllKarmaReactions(str(ctx.guild.id))
        return await ctx.send(f"KarmaReaction settings have been reset")

    @commands.Cog.listener(name='on_raw_reaction_remove')
    async def onReactionRemove(self, payload: discord.RawReactionActionEvent):
        chn = self.bot.get_channel(payload.channel_id)
        msg = await chn.fetch_message(payload.message_id)
        if payload.user_id == msg.author.id:
            return
        serverId = str(payload.guild_id)
        emoji = str(payload.emoji)

        karmaReaction = getKarmaReactionByServerAndReaction(serverId, emoji)
        if karmaReaction is not None:
            updateUserKarma(str(msg.author.id), -karmaReaction.karmaChange)

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def onReactionAdd(self, payload: discord.RawReactionActionEvent):
        chn = self.bot.get_channel(payload.channel_id)
        msg = await chn.fetch_message(payload.message_id)
        if payload.user_id == msg.author.id:
            return

        serverId = str(payload.guild_id)
        emoji = str(payload.emoji)

        karmaReaction = getKarmaReactionByServerAndReaction(serverId, emoji)
        if karmaReaction is not None:
            updateUserKarma(str(msg.author.id), karmaReaction.karmaChange)


def parseLeaderboard(l, offset):
    parsedLeaderboard = ''
    for index, user in enumerate(l):
        s = f"{index+1+offset}. {user.name}: msgCount={user.message_count}, karma={user.karma}\n"
        if len(parsedLeaderboard+s)+20 > 2000:
            break
        parsedLeaderboard += s
    return parsedLeaderboard
