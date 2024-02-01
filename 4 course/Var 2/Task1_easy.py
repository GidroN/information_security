from zipfile import ZipFile, BadZipFile
import os


class BruteForce:

    def __init__(self, data: list | str, zip_file: str, extract_folder: str):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.extract_files_folder = os.path.join(base_dir, extract_folder)
        self.zip_file_path = os.path.join(base_dir, zip_file)

        if isinstance(data, list):
            self.password_list = data
        else:
            file_path = os.path.join(base_dir, data)
            self.password_list = self._get_data_from_file(file_path)

    @staticmethod
    def _get_data_from_file(path: str):
        if not os.path.exists(path):
            print('Указанный файл с паролями не найден.')
            exit(1)

        password_list = []
        with open(path, 'r') as file:
            for item in file.readlines():
                password_list.append(item.strip())

        return password_list

    def start_bruteforce(self):
        if not os.path.exists(self.zip_file_path):
            print('Указанный архив не найден.')
            exit(1)

        print('Начат брутфорс.')
        for password in self.password_list:
            try:
                with ZipFile(self.zip_file_path, 'r') as zip:
                    zip.extractall(path=self.extract_files_folder, pwd=password.encode('utf-8'))
                    print(f'Нужный пароль: {password}')
                    print('Брут успешно завершен.')
                    break
            except (BadZipFile, RuntimeError):
                print(f'Попытка: {password}')


if __name__ == '__main__':
    brut = BruteForce('testdir_fixtures/passwords.txt', 'testdir_fixtures/secret.zip', 'testdir_fixtures')
    brut.start_bruteforce()
