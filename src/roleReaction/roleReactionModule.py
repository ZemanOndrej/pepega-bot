import discord
from discord.ext import commands
from db.roleReactionRepo import createRoleReaction, getRoleReactionByServerAndReaction, getRoleReactionByServer, removeRoleReaction, removeAllRoleReactions
from db.db import EntityNotFound
from util.utilService import extractRole, extractEmoteText
from db.serverRepo import saveServer, getServerById
from discord.ext.commands import has_permissions
from strings.en_us import strings
from emoji import UNICODE_EMOJI
import typing


class RoleReactionModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _prefix(self):
        return self.bot.command_prefix


# TODO fix permissions
    @commands.command(name='roleReaction', help=strings['help_rr_print'])
    async def printRoleReactions(self, ctx):
        serverId = str(ctx.message.guild.id)
        server = getServerById(serverId)

        if server.role_reaction_channel_id is None:
            return await ctx.send(f"RoleReaction is not configured on this server.")
        chn = self.bot.get_channel(int(server.role_reaction_channel_id))
        roles = ctx.message.guild.roles
        roleReactions = getRoleReactionByServer(serverId)
        rString = []
        for rr in roleReactions:
            role = next(filter(lambda x: x.id == int(rr.role), roles))
            rString.append(
                f"  Reaction {extractEmoteText(rr.reaction)} is set for <@{role.name}> role")
        nl = '\n'
        return await ctx.send(
            f"""```
The roleReaction channel is set to `#{chn}`\n
{nl.join(rString) if len(roleReactions)>0 else "This server doesnt have any roleReactions"}\
            ```""")

    @commands.command(name="roleReactionChannel", help=strings['help_rr_channel'])
    async def addServerChannel(self, ctx, channel: discord.TextChannel):
        saveServer(serverId=str(ctx.message.guild.id), channelId=channel.id)
        return await ctx.send(
            f"""
                The roleReaction channel is set to `#{channel}`
            """)

    @commands.command(name="addRoleReaction", help=strings['help_rr_add'])
    async def addRoleReaction(self, ctx, role: discord.Role, reaction: typing.Union[discord.PartialEmoji, str]):

        if type(reaction) == str and reaction not in UNICODE_EMOJI:
            return await ctx.send(f"Invalid Emote")

        server = getServerById(str(ctx.message.guild.id))
        if server.role_reaction_channel_id is None:
            return await ctx.send(
                f"""
            This dc server doesnt have roleReaction channel setup, type `{self._prefix()}roleReactionChannel #channel`
                """)

        if len(list(filter(lambda x: x == role, ctx.message.guild.roles))) == 0:
            return await ctx.send("Invalid Role")

        createRoleReaction(serverId=str(ctx.message.guild.id),
                           role=role.id, reaction=str(reaction))
        print(f'role reaction {role}/{reaction} id in {ctx.message.guild}')
        return await ctx.send(f"Reaction {reaction} was set for @{role} role")

    @commands.command(name="removeRoleReaction", help=strings['help_rr_remove'])
    async def removeRoleReaction(self, ctx, reaction):
        removeRoleReaction(str(ctx.guild.id), reaction)
        return await ctx.send(f"RoleReaction with {reaction} was removed.")

    @commands.command(name='resetRoleReaction', help=strings['help_rr_reset'])
    @has_permissions(administrator=True)
    async def resetRoleReaction(self, ctx):
        removeAllRoleReactions(str(ctx.guild.id))
        return await ctx.send(f"RoleReaction settings have been reset")

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def onReactionAdd(self, payload: discord.RawReactionActionEvent):
        serverId = str(payload.guild_id)
        serverDb = getServerById(serverId)
        if serverDb is not None and str(payload.channel_id) == serverDb.role_reaction_channel_id:
            serverRoleReaction = getRoleReactionByServerAndReaction(
                serverId,  str(payload.emoji))
            if serverRoleReaction is not None:

                server = self.bot.get_guild(int(serverDb.id))
                user = server.get_member(payload.user_id)
                role = server.get_role(int(serverRoleReaction.role))
                if role not in user.roles:
                    await user.add_roles(role, atomic=True)

    @commands.Cog.listener(name='on_raw_reaction_remove')
    async def onReactionRemove(self, payload: discord.RawReactionActionEvent):
        serverId = str(payload.guild_id)
        serverDb = getServerById(serverId)
        if serverDb is not None and str(payload.channel_id) == serverDb.role_reaction_channel_id:

            serverRoleReaction = getRoleReactionByServerAndReaction(
                serverId, str(payload.emoji))
            if serverRoleReaction is not None:
                server = self.bot.get_guild(int(serverDb.id))
                user = server.get_member(payload.user_id)
                role = server.get_role(int(serverRoleReaction.role))
                if role in user.roles:
                    await user.remove_roles(role, atomic=True)
