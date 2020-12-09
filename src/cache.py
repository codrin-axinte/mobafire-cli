from pathlib import Path


class Cache:
    def __init__(self, base_path):
        self.base_path = base_path

    def make_path(self, path):
        return self.base_path + '/' + path

    def exists(self, filepath):
        return Path(self.make_path(filepath)).exists()

    def read(self, filepath):
        with open(self.make_path(filepath), 'r') as file:
            return file.read()

    def write(self, filepath, content):
        # Cache response
        with open(self.make_path(filepath), 'w') as file:
            file.write(content)
