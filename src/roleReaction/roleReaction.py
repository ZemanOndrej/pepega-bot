import discord
from discord.ext import commands

from src.db.roleReactionRepo import saveServer, createRoleReaction, getServerById, getReactionRoleByServerAndReaction, \
    EntityNotFound


class RoleReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="roleReactionChannel")
    async def addServerChannel(self, ctx, channel: discord.TextChannel):
        saveServer(serverId=str(ctx.message.guild.id), channelId=channel.id)
        return await ctx.send(
            f"""
                The reactionRole channel is set to `#{channel}`
            """)

    @commands.command(name="roleReaction")
    async def addRoleReaction(self, ctx, role: str, reaction: str):
        try:
            createRoleReaction(serverId=str(ctx.message.guild.id), role=role.replace('<@&', '').replace('>', ''),
                               reaction=reaction)
        except EntityNotFound:
            return await ctx.send(
                """
                This dc server doesnt have roleReaction channel setup type `.roleReactionChannel #channel`
                """)

        print(f'role reaction {role}/{reaction} id in {ctx.message.guild}')

    @commands.Cog.listener(name='on_raw_reaction_add')
    async def onReactionAdd(self, payload: discord.RawReactionActionEvent):
        serverId = str(payload.guild_id)
        serverDb = getServerById(serverId)
        if str(payload.channel_id) == serverDb.channel_id:
            serverReactionRole = getReactionRoleByServerAndReaction(serverId, payload.emoji.name)
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
        if str(payload.channel_id) == serverDb.channel_id:
            serverReactionRole = getReactionRoleByServerAndReaction(serverId, payload.emoji.name)
            if serverReactionRole is not None:
                server = self.bot.get_guild(int(serverDb.id))
                user = server.get_member(payload.user_id)
                role = server.get_role(int(serverReactionRole.role))
                if role in user.roles:
                    await user.remove_roles(role, atomic=True)
