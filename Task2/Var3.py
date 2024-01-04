from functools import wraps
import os

def file_error_handler(func):
    @wraps(func)
    def wrapper(self, filename, *args, **kwargs):
        new_path = os.path.join(self.PATH, filename)
        if not os.path.exists(new_path):
            raise FileNotFoundError('File does not exist')
        return func(self, new_path, *args, **kwargs)
    return wrapper

class FileManager:
    def __init__(self, path: str):
        self.PATH = path
        self._check_dir_exists(self.PATH)

    @staticmethod
    def _check_dir_exists(path: str):
        if not os.path.exists(path) or not os.path.isdir(path):
            raise FileNotFoundError(f"{path} not found or is not a directory")

    @file_error_handler
    def delete(self, file_path: str) -> bool:
        os.remove(file_path)
        return True

    @file_error_handler
    def update(self, file_path: str, content: str) -> bool:
        with open(file_path, 'a') as f:
            f.write(content)
        return True

    def make_unique(self):
        """
        Разве система сама не заботиться о том,
        чтобы названия файлов были уникальными?
        """
        ...

    @file_error_handler
    def show(self, file_path: str) -> str:
        with open(file_path) as f:
            return str(f.readlines())

    def add(self, filename: str, content: str = '') -> bool | None:
        new_path = os.path.join(self.PATH, filename)
        if os.path.exists(new_path):
            return None
        with open(new_path, 'w') as f:
            f.write(content)
        return True

    def sort(self, ascending: bool = True):
        files = os.listdir(self.PATH)
        files.sort(reverse=not ascending)
        return files


if __name__ == '__main__':
    path = ""
    manager = FileManager(path)
    manager.add('b.txt')
    manager.add('c.txt')
    manager.add('a.txt')
    print(manager.sort(ascending=True))