from discord.ext import commands
from roleReaction.roleReactionModule import RoleReactionModule
from ticTacToe.ticTacToe import TicTacToe
from utilCommands.events import Events
from utilCommands.utilCommands import UtilCommands
from user.userModule import UserModule
from util.params import getEnvVariable


bot = commands.Bot(command_prefix=getEnvVariable("DEFAULT_PREFIX"))

bot.add_cog(Events(bot))
bot.add_cog(UtilCommands(bot))
bot.add_cog(RoleReactionModule(bot))
bot.add_cog(TicTacToe(bot))
bot.add_cog(UserModule(bot))
bot.run(getEnvVariable('DC_TOKEN'))
