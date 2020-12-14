from src.utils import *


class Cache:

    def __init__(self, base_path):
        self.base_path = base_path
        self.sub_folders = [
            self.get_path('guides'),
            self.get_path('search'),
        ]

    def clear(self):
        rmdir(self.base_path)

    def init(self):
        folders = [self.base_path] + self.sub_folders
        make_folders(folders)

    def reload(self):
        self.clear()
        self.init()

    def get_path(self, path):
        return self.base_path + '/' + path

    def exists(self, filepath):
        return Path(self.get_path(filepath)).exists()

    def read(self, filepath):
        with open(self.get_path(filepath), 'r') as file:
            return file.read()

    def write(self, filepath, content):
        # Cache response
        with open(self.get_path(filepath), 'w') as file:
            file.write(content)
