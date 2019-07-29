from discord.ext import commands
from src.utilCommands.events import Events
from src.utilCommands.utilCommands import UtilCommands
from src.ticTacToe.ticTacToe import TicTacToe
from src.config import CONFIG

bot = commands.Bot(command_prefix=".")

bot.add_cog(Events(bot))
bot.add_cog(UtilCommands(bot))
bot.add_cog(TicTacToe(bot))
bot.run(CONFIG["token"])
