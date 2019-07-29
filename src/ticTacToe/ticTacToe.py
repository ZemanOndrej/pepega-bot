import discord
from discord.ext import commands

from src.ticTacToe.ticTacToeGame import TicTacToeGame


class TicTacToe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.tttList = []

    def getGameByPlayer(self, p):
        return next(filter(lambda x: x.p1 == p or x.p2 == p, self.tttList))

    def removePlayers(self, game):
        self.players.remove(game.p1)
        self.players.remove(game.p2)

    @commands.command(name="tttaccept")
    async def accept(self, ctx):
        if ctx.author not in self.players:
            return await ctx.send(f"You have nothing to accept :(. To start a new game type `.tictactoe @some_user`")

        game = self.getGameByPlayer(ctx.author)
        if game.p2 == ctx.author:
            game.accept()
            return await ctx.send(game)

        await ctx.send(f"Player {game.p2} has to accept the game, not you!")

    @commands.command(name='tttforfeit')
    async def forfeit(self, ctx):
        if ctx.author not in self.players:
            return await ctx.send(f"You have nothing to forfeit :(. To start a new game type `.tictactoe @some_user`")
        game = self.getGameByPlayer(ctx.author)
        self.removePlayers(game)
        if not game.isStarted:
            return await ctx.send(f"{ctx.author} left the game.")
        await ctx.send(
            f"Player {ctx.author} has forfeited the game. {game.p1 if game.p1 != ctx.author else game.p2} has won.")

    @commands.command(name='tttreject')
    async def reject(self, ctx):
        if ctx.author not in self.players:
            return await ctx.send(f"You have nothing to reject :(. To start a new game type `.tictactoe @some_user`")
        game = self.getGameByPlayer(ctx.author)
        if game.isStarted:
            return await ctx.send("Game has already started. If you want to leave the game type `.tttforfeit`")
        if game.p2 == ctx.author:
            self.removePlayers(game)
            self.tttList.remove(game)
        await ctx.send(f"Player {ctx.author} has rejected the TicTacToe game.")

    @commands.command(name='tttplay')
    async def play(self, ctx, x, y):
        if ctx.author not in self.players:
            return await ctx.send(f"You are not in game :(. To start a new game type `.tictactoe @some_user`")
        game = self.getGameByPlayer(ctx.author)

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
            self.removePlayers(game)
            self.tttList.remove(game)
        await ctx.send(game)

    @commands.command(name='tttstart')
    async def start(self, ctx, p2: discord.Member):
        if p2 == self.bot.user:
            return await ctx.send("Im too :Pepega: for this game.")
        if p2 == ctx.author:
            return await ctx.send('you cant inv yourself :NotLikeThis:')

        p1InGame = ctx.author in self.players
        p2InGame = p2 in self.players

        if p1InGame or p2InGame:
            return await ctx.send(f'{ctx.author if p1InGame else p2} is already in game!')

        self.players.extend([p2, ctx.author])

        if ctx.author is not p2:
            self.tttList.append(TicTacToeGame(ctx.author, p2))
            await ctx.send(
                f'<@{ctx.author.id}> invited you to tictactoe <@{p2.id}> type \'.tttaccept\' or \'.tttreject\' ')

    @commands.command(name='tttboard')
    async def getBoard(self, ctx):
        if ctx.author not in self.players:
            return await ctx.send(f"You are not in game :(. To start a new game type `.tictactoe @some_user`")
        game = self.getGameByPlayer(ctx.author)
        await ctx.send(str(game))
