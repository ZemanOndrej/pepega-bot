import discord
import json
from discord.ext import commands
from params import getArgDict
from util.timeUtils import cd
import sys
from TicTacToeGame import TicTacToeGame
import asyncio

argDict = getArgDict(sys.argv)

with open(argDict['config'] if 'config' in argDict else './config.json') as config:
    d = json.load(config)
bot = commands.Bot(command_prefix=".")


async def backgroundTask():
    await bot.wait_until_ready()
    counter = 0
    loggingChannel = bot.get_channel(604220508267085824)

    await loggingChannel.send("bot is online")
    while not bot.is_closed():
        print(counter)
        counter += 1
        await loggingChannel.send(f"bot has been online for {counter} minutes.")
        await asyncio.sleep(60)



@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="with myself"))
    bot.loop.create_task(backgroundTask())
    print(f'We have logged in as {bot.user}')


tttList = []
players = []


@bot.event
async def on_message(message):
    await bot.process_commands(message)


def getGameByPlayer(p):
    return next(filter(lambda x: x.p1 == p or x.p2 == p, tttList))


def removePlayers(game):
    players.remove(game.p1)
    players.remove(game.p2)


@bot.command()
async def tttaccept(ctx):
    if ctx.author not in players:
        return await ctx.send(f"You have nothing to accept :(. To start a new game type `.tictactoe @some_user`")

    game = getGameByPlayer(ctx.author)
    if game.p2 == ctx.author:
        game.accept()
        return await ctx.send(game)

    await ctx.send(f"Player {game.p2} has to accept the game, not you!")


@bot.command()
async def tttforfeit(ctx):
    if ctx.author not in players:
        return await ctx.send(f"You have nothing to forfeit :(. To start a new game type `.tictactoe @some_user`")
    game = getGameByPlayer(ctx.author)
    removePlayers(game)
    if not game.isStarted:
        return await ctx.send(f"{ctx.author} left the game.")
    await ctx.send(
        f"Player {ctx.author} has forfeited the game. {game.p1 if game.p1 != ctx.author else game.p2} has won.")


@bot.command()
async def tttreject(ctx):
    if ctx.author not in players:
        return await ctx.send(f"You have nothing to reject :(. To start a new game type `.tictactoe @some_user`")
    game = getGameByPlayer(ctx.author)
    if game.isStarted:
        return await ctx.send("Game has already started. If you want to leave the game type `.tttforfeit`")
    if game.p2 == ctx.author:
        removePlayers(game)
        tttList.remove(game)
    await ctx.send(f"Player {ctx.author} has rejected the TicTacToe game.")


@bot.command()
async def tttplay(ctx, x, y):
    if ctx.author not in players:
        return await ctx.send(f"You are not in game :(. To start a new game type `.tictactoe @some_user`")
    game = getGameByPlayer(ctx.author)

    if not game.isStarted:
        return await ctx.send("stahp! game is not started yet.")

    if ctx.author != game.nextPlayer:
        return await ctx.send("stahp! it's not your turn")

    try:
        xInt = int(x)
        yInt = int(y)
    except:
        return await ctx.send("Wrong input!")

    if not game.isPositionCorrect(xInt, yInt):
        return await ctx.send("this position is not correct or free!")

    game.playTurn(ctx.author, xInt, yInt)

    if game.isFinished:
        removePlayers(game)
        tttList.remove(game)
    await ctx.send(game)


@bot.command()
async def tictactoe(ctx, p2: discord.Member):
    if p2 == bot.user:
        return await ctx.send("Im too :Pepega: for this game.")
    if p2 == ctx.author:
        return await ctx.send('you cant inv yourself :NotLikeThis:')

    p1InGame = ctx.author in players
    p2InGame = p2 in players

    if p1InGame or p2InGame:
        return await ctx.send(f'{ctx.author if p1InGame else p2} is already in game!')

    players.extend([p2, ctx.author])

    if ctx.author is not p2:
        tttList.append(TicTacToeGame(ctx.author, p2))
        await ctx.send(f'<@{ctx.author.id}> invited you to tictactoe <@{p2.id}> type \'.tttaccept\' or \'.tttreject\' ')


@bot.command()
async def countdown(ctx, *args):
    countStart = 0
    try:
        if len(args) > 1:
            countStart = int(getArgDict(args)['time'])
        elif len(args) == 1 and args[0].isnumeric():
            countStart = int(args[0])
    except:
        return await ctx.send("wrong input")
    if countStart > 20:
        return await ctx.send("number is too big!")

    await cd(ctx.send, countStart, 1, "countdown has started", "it is finished")


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


@bot.command()
async def tttboard(ctx):
    if ctx.author not in players:
        return await ctx.send(f"You are not in game :(. To start a new game type `.tictactoe @some_user`")
    game = getGameByPlayer(ctx.author)
    await ctx.send(str(game))

bot.run(d["token"])
