from zipfile import ZipFile, BadZipFile
import os
import sys


class BruteForce:

    def __init__(self, data: list | str, zip_file: str):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.extract_files_folder = os.path.join(base_dir, 'testdir_fixtures')

        if isinstance(data, list):
            self.password_list = data
        else:
            file_path = os.path.join(base_dir, data)
            self.password_list = self._get_data_from_file(file_path)

        self.zip_file_path = os.path.join(base_dir, zip_file)

    @staticmethod
    def _get_data_from_file(path: str):
        if not os.path.exists(path):
            print('Указанный файл с паролями не найден.')
            sys.exit(1)

        with open(path, 'r') as file:
            return [item.strip() for item in file.readlines()]

    def start_bruteforce(self):
        if not os.path.exists(self.zip_file_path):
            print('Указанный архив не найден.')
            return

        print('Начат брутфорс.')
        for password in self.password_list:
            try:
                with ZipFile(self.zip_file_path, 'r') as zip:
                    zip.extractall(path=self.extract_files_folder, pwd=password.encode('utf-8'))
                    print(f'Подходящий пароль: {password}')
                    print('Брут успешно завершен.')
                    break
            except (BadZipFile, RuntimeError):
                print(f'Неподходящий пароль: {password}')


if __name__ == '__main__':
    brut = BruteForce(['qwerty', 'qwerqwer', '123'], 'testdir_fixtures/secret.zip')
    brut.start_bruteforce()
