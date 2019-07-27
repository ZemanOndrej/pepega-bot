import json
from discord.ext import commands

from utilCommands.events import Events
from utilCommands.utilCommands import UtilCommands
from ticTacToe.ticTacToe import TicTacToe
from util.params import getArgDict
import sys

argDict = getArgDict(sys.argv)

with open(argDict['config'] if 'config' in argDict else './config.json') as config:
    d = json.load(config)
bot = commands.Bot(command_prefix=".")

bot.add_cog(Events(bot))
bot.add_cog(UtilCommands(bot))
bot.add_cog(TicTacToe(bot))
bot.run(d["token"])
