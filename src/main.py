from discord.ext import commands

from config import CONFIG
from roleReaction.roleReaction import RoleReaction
from ticTacToe.ticTacToe import TicTacToe
from utilCommands.events import Events
from utilCommands.utilCommands import UtilCommands

bot = commands.Bot(command_prefix=CONFIG["default_prefix"])

bot.add_cog(Events(bot))
bot.add_cog(UtilCommands(bot))
bot.add_cog(RoleReaction(bot))
bot.add_cog(TicTacToe(bot))
bot.run(CONFIG["token"])
