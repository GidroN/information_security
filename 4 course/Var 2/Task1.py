import os
import itertools
import pyminizip
from zipfile import ZipFile, BadZipFile


class BruteforceZip:
    def __init__(self, zip_filename):
        self.zip_filename: str = zip_filename
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    @staticmethod
    def _get_data_from_file(path: str):
        if not os.path.exists(path):
            print('Указанный файл с паролями не найден.')
            return

        with open(path, 'r') as file:
            password_list = [item.strip() for item in file.readlines()]

        return password_list

    def create_protected_zip(self, content, password: str):
        pyminizip.compress(content, None, self.zip_filename, password, 0)

    def _extract_protected_zip(self, password: str, path: str = None):
        extract_path = self.base_dir if not path else path
        with ZipFile(self.zip_filename, 'r') as file:
            try:
                file.extractall(path=extract_path, pwd=password.encode('utf-8'))
                return True
            except (RuntimeError, BadZipFile):
                ...
        return False

    def brute_force_combinations(self, data: str, length: int):
        combinations = itertools.permutations(data, length)
        for comb in combinations:
            try_pass = ''.join(comb)
            print(f'Попытка: {try_pass}')
            if self._extract_protected_zip(try_pass):
                print(f'Пароль успешно найден: {try_pass}')
                return
        print('Пароль не найден =(')

    def brute_force_from_pass_list(self, data: str | list[str]):
        if isinstance(data, str):
            passwords_list = self._get_data_from_file(data)
        else:
            passwords_list = data

        for pwd in passwords_list:
            print(f'Попытка: {pwd}')
            if self._extract_protected_zip(pwd):
                print(f'Пароль успешно найден: {pwd}')
                return
        print('Пароль не найден =(')


if __name__ == '__main__':
    brute = BruteforceZip('testdir_v2/secret.zip')
    brute.create_protected_zip('testdir_v2/data.txt', 'qwe')
    # brute.brute_force_combinations('wqe', 3)
    # brute.brute_force_from_pass_list(['wqe', 'www', 'qwe'])
    brute.brute_force_from_pass_list('testdir_v2/passwords.txt')

