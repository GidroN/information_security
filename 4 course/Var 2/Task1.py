from zipfile import ZipFile
import os


class BruteForce:

    def __init__(self, data: list | str, zip_file: str):

        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir, data)
        self.zip_file_path = os.path.join(base_dir, zip_file)

        self.password_list = data if isinstance(data, list) else self._get_data_from_file(file_path)
        
    @staticmethod
    def _get_data_from_file(path: str):
        if not os.path.exists(path):
            print('Указанный файл не найден.')
            return
        
        with open(path, 'r') as file:
            return [item.strip() for item in file.readlines()] 
    
    def start_bruteforce(self):
        for password in self.password_list:
            password = password.encode('utf-8')
            with ZipFile(self.zip_file_path, 'r') as zip:
                try:
                    zip.extractall(pwd=password) 
                except RuntimeError:
                    pass

class PasswordGenerator:
    def __init__(self, length: int = 10):
        self.length = length

    def generate(self):
        ...


if __name__ == '__main__':
    brut = BruteForce('testdir_fixtures/passwords.txt', 'testdir_fixtures/secret_file.zip')
    brut.start_bruteforce()