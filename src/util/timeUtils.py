from asyncio import sleep


async def cd(send, countdownStart, sleepTime, startMessage="", endMessage=""):
    await send(startMessage)
    while countdownStart > 0:
        await send(countdownStart)
        countdownStart -= 1
        await sleep(sleepTime)
    await send(endMessage)
