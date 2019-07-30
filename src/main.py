from discord.ext import commands

from src.config import CONFIG
from src.roleReaction.roleReaction import RoleReaction
from src.ticTacToe.ticTacToe import TicTacToe
from src.utilCommands.events import Events
from src.utilCommands.utilCommands import UtilCommands

bot = commands.Bot(command_prefix=".")

bot.add_cog(Events(bot))
bot.add_cog(UtilCommands(bot))
bot.add_cog(RoleReaction(bot))
bot.add_cog(TicTacToe(bot))
bot.run(CONFIG["token"])
