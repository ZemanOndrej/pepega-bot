def extractEmoteFromMessage(reaction):
    splitStr = reaction.split(':')
    if len(splitStr) > 1:
        emote = splitStr[2].replace('>', '')
    else:
        emote = splitStr[0]
    return emote


def getEmojiIdFromPayloadEmoji(e):
    return str(e.id) if e.id is not None else e.name
