import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from db.userRepo import getUsers, incUserMsgCount, updateUserKarma
from db.karmaRepo import getKarmaReactionByServerAndReaction, saveKarmaReaction, getKarmaReactionsByServer, removeKarmaReaction
from util.utilService import extractEmoteText
from strings.en_us import strings


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

    @commands.command(name="karmaInfo",help=strings['help_kr_print'])
    async def karmaInfo(self, ctx):
        karmaReaction = getKarmaReactionsByServer(str(ctx.message.guild.id))
        if len(karmaReaction) == 0:
            return await ctx.send('There are no karma reactions on this server')
        nl = '\n'
        return await ctx.send(
            f"""```KarmaReactions:
{nl.join([f"Reaction {extractEmoteText(x.reaction)} changes your karma by {x.karmaChange}" for x in karmaReaction])}
            ```""")

    @commands.command(name="removeKarmaReaction",help=strings['help_kr_remove'])
    async def removeKarmaReaction(self, ctx, reaction):
        removeKarmaReaction(str(ctx.guild.id), reaction)
        return await ctx.send(f"KarmaReaction with {reaction} was removed.")

    @commands.Cog.listener()
    async def on_message(self, message):
        incUserMsgCount(message.author)

    @commands.command(name="saveKarmaReaction",help=strings['help_kr_save'])
    async def addKarmaReaction(self, ctx,  reaction, val: int):
        saveKarmaReaction(str(ctx.message.guild.id), reaction, val)
        return await ctx.send(f'Reaction {reaction} will change your karma by {val}')

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
