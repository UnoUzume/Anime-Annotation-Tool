from pathlib import Path

rootPath: Path = None


def Patha(path):
    return Path(rootPath, path)
