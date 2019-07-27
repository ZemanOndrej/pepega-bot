from discord.ext import commands
from utilCommands.events import Events
from utilCommands.utilCommands import UtilCommands
from ticTacToe.ticTacToe import TicTacToe
from config import CONFIG

bot = commands.Bot(command_prefix=".")

bot.add_cog(Events(bot))
bot.add_cog(UtilCommands(bot))
bot.add_cog(TicTacToe(bot))
bot.run(CONFIG["token"])
