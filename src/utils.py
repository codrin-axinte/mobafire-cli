from pathlib import Path


def rmdir(directory):
    directory = Path(directory)
    for item in directory.iterdir():
        if item.is_dir():
            rmdir(item)
        else:
            item.unlink()
    directory.rmdir()


def make_folders(folders):
    for folder in folders:
        if not Path(folder).exists():
            Path(folder).mkdir()
