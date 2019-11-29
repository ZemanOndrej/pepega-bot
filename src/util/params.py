import os


def getArgDict(argv: list):
    argDict = {}
    for i, arg in enumerate(argv):
        if not arg.startswith('--'):
            continue
        else:
            parsedArg = arg.replace('--', '')
            if i + 1 < len(argv) and not argv[i + 1].startswith('--'):
                argDict[parsedArg] = argv[i + 1]
            else:
                argDict[parsedArg] = True
    return argDict


def getEnvVariable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f'Expected environment variable "{name}" not set.'
        raise Exception(message)
