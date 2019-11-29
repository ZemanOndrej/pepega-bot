import json


def extractEmoteFromMessage(reaction):
    splitStr = reaction.split(':')
    if len(splitStr) > 1:
        emote = splitStr[2].replace('>', '')
    else:
        emote = splitStr[0]
    return emote


def getEmojiIdFromPayloadEmoji(e):
    return str(e.id) if e.id is not None else e.name


def extractBoolFromString(s):
    return json.loads(s.lower())


def extractRole(s):
    return s.replace('<@&', '').replace('>', '')


def extractEmoteText(s):
    splitStr = s.split(':')
    if len(splitStr) > 1:
        return f':{splitStr[1]}:'
    return splitStr[0]
