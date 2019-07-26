import numpy as np
import random
import datetime


class TicTacToeGame:
    def __init__(self, p1, p2, xByx: int = 3, winCondition: int = 3, turnTime: int = 5*60):
        self.timeStarted = datetime.datetime.now()
        self.p1 = p1
        self.p2 = p2
        self.winCondition = winCondition
        self.timeLastTurn = datetime.datetime.now()
        self.xByx = xByx
        self.gameBoard = [[0 for x in range(xByx)]for x in range(xByx)]
        self.nextPlayer = p1 if random.random() < 0.5 else p2
        self.isStarted = False
        self.turnTime = turnTime
        self.playerWon = 0
        self.isFinished = False

    def isPositionCorrect(self, x: int, y: int):
        return x < self.xByx and y < self.xByx and x >= 0 and y >= 0 and self.gameBoard[y][x] == 0

    def accept(self):
        self.isStarted = True

    def checkIfLiveGame(self):
        return datetime.datetime.now() > self.timeLastTurn + datetime.timedelta(seconds=self.turnTime)

    def __str__(self):
        finStr = ""
        if self.isFinished and self.playerWon != 0:
            finStr = "{self.playerWon} won this game!"
        elif self.isFinished:
            finStr = "Its a draw :|"
        gb = ""
        for row in self.gameBoard:
            gb = gb+f" {'|'.join(str(x) for x in row )} \n"

        return f"""
```turn timer is {self.turnTime/60} minutes

{gb}

player {self.nextPlayer} is going next
type `.tttplay column row `
{finStr}
```
"""

    def playTurn(self, p, x, y):
        symbol = 1 if p == self.p1 else 2
        self.gameBoard[y][x] = symbol
        self.timeLastTurn = datetime.datetime.now()

        self.playerWon = self._checkWin()
        self.isFinished = self.playerWon != 0 and any(
            0 in subl for subl in self.gameBoard)

        if not self.isFinished:
            self.nextPlayer = self.p1 if p == self.p2 else self.p2

    def _checkWin(self):
        # transposition to check rows, then columns
        for newBoard in [self.gameBoard, np.transpose(self.gameBoard)]:
            result = checkRows(newBoard)
            if result:
                return result
        return checkDiagonals(self.gameBoard)


def checkDiagonals(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return 0


def checkRows(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return 0
