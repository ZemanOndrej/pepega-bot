import discord
from discord.ext import commands

from db.roleReactionRepo import createRoleReaction, getReactionRoleByServerAndReaction
from db.db import EntityNotFound
from util.utilService import extractEmoteFromMessage, getEmojiIdFromPayloadEmoji
from db.serverRepo import saveServer, getServerById


class RoleReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _prefix(self):
        return self.bot.command_prefix

    @commands.command(name="roleReactionChannel")
    async def addServerChannel(self, ctx, channel: discord.TextChannel):
        saveServer(serverId=str(ctx.message.guild.id), channelId=channel.id)
        return await ctx.send(
            f"""
                The reactionRole channel is set to `#{channel}`
            """)

    @commands.command(name="addRoleReaction")
    async def addRoleReaction(self, ctx, role: str, reaction):
        try:
            createRoleReaction(serverId=str(ctx.message.guild.id), role=role.replace('<@&', '').replace('>', ''),
                               reaction=extractEmoteFromMessage(reaction))
        except EntityNotFound:
            return await ctx.send(
                f"""
            This dc server doesnt have roleReaction channel setup, type `{self._prefix()}roleReactionChannel #channel`
                """)
        print(f'role reaction {role}/{reaction} id in {ctx.message.guild}')
        return await ctx.send(f"Reaction {reaction} was set for {role} role")

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def onReactionAdd(self, payload: discord.RawReactionActionEvent):
        serverId = str(payload.guild_id)
        serverDb = getServerById(serverId)
        if serverDb is not None and str(payload.channel_id) == serverDb.role_reaction_channel_id:
            emoji = getEmojiIdFromPayloadEmoji(payload.emoji)
            serverReactionRole = getReactionRoleByServerAndReaction(
                serverId, emoji)
            if serverReactionRole is not None:

                server = self.bot.get_guild(int(serverDb.id))
                user = server.get_member(payload.user_id)
                role = server.get_role(int(serverReactionRole.role))
                if role not in user.roles:
                    await user.add_roles(role, atomic=True)

    @commands.Cog.listener(name='on_raw_reaction_remove')
    async def onReactionRemove(self, payload: discord.RawReactionActionEvent):
        serverId = str(payload.guild_id)
        serverDb = getServerById(serverId)
        if serverDb is not None and str(payload.channel_id) == serverDb.role_reaction_channel_id:
            emoji = getEmojiIdFromPayloadEmoji(payload.emoji)

            serverReactionRole = getReactionRoleByServerAndReaction(
                serverId, emoji)
            if serverReactionRole is not None:
                server = self.bot.get_guild(int(serverDb.id))
                user = server.get_member(payload.user_id)
                role = server.get_role(int(serverReactionRole.role))
                if role in user.roles:
                    await user.remove_roles(role, atomic=True)
