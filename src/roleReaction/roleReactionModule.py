import discord
from discord.ext import commands
from db.roleReactionRepo import createRoleReaction, getReactionRoleByServerAndReaction, getReactionRoleByServer, removeRoleReaction
from db.db import EntityNotFound
from util.utilService import extractRole, extractEmoteText
from db.serverRepo import saveServer, getServerById
from strings.en_us import strings


class RoleReactionModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _prefix(self):
        return self.bot.command_prefix


    @commands.command(name='roleReaction', help=strings['help_rr_print'])
    async def printRoleReactions(self, ctx):
        serverId = str(ctx.message.guild.id)
        server = getServerById(serverId)

        if server.role_reaction_channel_id is None:
            return await ctx.send(f"RoleReaction is not configured on this server.")
        chn = self.bot.get_channel(int(server.role_reaction_channel_id))
        roles = ctx.message.guild.roles
        roleReactions = getReactionRoleByServer(serverId)
        rString = []
        for rr in roleReactions:
            role = next(filter(lambda x: x.id == int(rr.role), roles))
            rString.append(
                f"  Reaction {extractEmoteText(rr.reaction)} is set for <@{role.name}> role")
        nl = '\n'
        return await ctx.send(
            f"""```
The roleReaction channel is set to `#{chn}`

{nl.join(rString) if len(roleReactions)>0 else "This server doesnt have any roleReactions"}\
            ```""")

# TODO INPUT VALIDATION!!!!!!!!!!!
    @commands.command(name="roleReactionChannel", help=strings['help_rr_channel'])
    async def addServerChannel(self, ctx, channel: discord.TextChannel):
        saveServer(serverId=str(ctx.message.guild.id), channelId=channel.id)
        return await ctx.send(
            f"""
                The reactionRole channel is set to `#{channel}`
            """)

    @commands.command(name="addRoleReaction", help=strings['help_rr_add'])
    async def addRoleReaction(self, ctx, role: str, reaction):

        server = getServerById(str(ctx.message.guild.id))
        if server.role_reaction_channel_id is None:
            return await ctx.send(
                f"""
            This dc server doesnt have roleReaction channel setup, type `{self._prefix()}roleReactionChannel #channel`
                """)

        createRoleReaction(serverId=str(ctx.message.guild.id), role=extractRole(
            role), reaction=reaction)
        print(f'role reaction {role}/{reaction} id in {ctx.message.guild}')
        return await ctx.send(f"Reaction {reaction} was set for {role} role")

    @commands.command(name="removeRoleReaction", help=strings['help_rr_remove'])
    async def removeRoleReaction(self, ctx, reaction):
        removeRoleReaction(str(ctx.guild.id), reaction)
        return await ctx.send(f"RoleReaction with {reaction} was removed.")

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def onReactionAdd(self, payload: discord.RawReactionActionEvent):
        serverId = str(payload.guild_id)
        serverDb = getServerById(serverId)
        if serverDb is not None and str(payload.channel_id) == serverDb.role_reaction_channel_id:
            serverReactionRole = getReactionRoleByServerAndReaction(
                serverId,  str(payload.emoji))
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

            serverReactionRole = getReactionRoleByServerAndReaction(
                serverId, str(payload.emoji))
            if serverReactionRole is not None:
                server = self.bot.get_guild(int(serverDb.id))
                user = server.get_member(payload.user_id)
                role = server.get_role(int(serverReactionRole.role))
                if role in user.roles:
                    await user.remove_roles(role, atomic=True)
