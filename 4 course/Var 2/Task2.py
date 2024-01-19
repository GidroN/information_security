from prettytable import PrettyTable
import os
import sqlite3


def category_exist_handler(func):
    def wrapper(self, category: str, *args, **kwargs):
        db = DataBase()
        if not db.check_table_exists(category):
            return f'Категории {category} не существует. Сначала добавьте ее.'

        return func(self, category, *args, **kwargs)

    return wrapper


class DataBase:

    TOP_UP = 'Пополнение'
    TOP_DOWN = 'Снятие'

    def __init__(self, filename: str = 'database.db'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, filename)

        self.conn = self._get_connection(db_path)
        self.cur = self.conn.cursor()

    @staticmethod
    def _get_connection(path):
        if not os.path.exists(path):
            open(path, 'w').close()
        return sqlite3.connect(path)

    def _get_all_rows_from_category(self):
        ...

    def check_table_exists(self, category: str):
        prompt = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?"
        self.cur.execute(prompt, (category.capitalize(), ))
        self.conn.commit()
        return self.cur.fetchone()[0] == 1

    def add_table(self, category: str, balance):
        prompt = f"""
                    CREATE TABLE IF NOT EXISTS {category}(
                        ID INTEGER PRIMARY KEY,
                        balance REAL,
                        operation VARCHAR(50),
                        change REAL,
                        description TEXT 
                    ); 

                    INSERT INTO {category} (balance, operation, change, description) 
                    VALUES ({balance}, 'Пополнение', {balance}, 'Создание новой категории');
                    """

        self.cur.executescript(prompt)
        self.conn.commit()

    def add_row(self, category: str, balance: float, operation: str, change: float, description: str):
        prompt = ("INSERT INTO {category} (balance, operation, change, description) "
                  "VALUES (?, ?, ?, ?);").format(category=category.capitalize())

        self.cur.execute(prompt, (balance, operation, change, description))
        self.conn.commit()

    def get_balance(self, category: str):
        prompt = f"SELECT balance FROM {category} ORDER BY ID DESC LIMIT 1;".format(category=category.capitalize())

        self.cur.execute(prompt)
        return self.cur.fetchone()[0]


class Wallet:
    def __init__(self):
        self.db = DataBase()
        self.table = PrettyTable()

    def add_category(self, category: str, balance: float = 0.0) -> bool:
        if self.db.check_table_exists(category):
            print("Данная категория уже добавлена. Вностие изменения.")
            return False

        self.db.add_table(category, balance)
        print("Новая категория успешно добавлена. Можете вносить операции.")
        return True

    @category_exist_handler
    def top_up(self, category: str, amount: float, description: str = '') -> bool:
        current_balance = self.db.get_balance(category)
        new_balance = current_balance + amount
        self.db.add_row(category, new_balance, self.db.TOP_UP, amount, description)
        print(f"Пополнение успешно проведено. Ваш баланс в категории {category} составляет: {new_balance}")
        return True

    @category_exist_handler
    def top_down(self, category: str, amount: float, description: str = '') -> bool:
        current_balance = self.db.get_balance(category)
        if not self.check_balance(category, amount):
            print(f"У вас недостаточно средств на проведение данной операции. Ваш баланс: {current_balance}")
            return False
        new_balance = current_balance - amount
        self.db.add_row(category, new_balance, self.db.TOP_DOWN, amount, description)
        print(f"Снятие успешно проведено. Ваш баланс в категории {category} составляет: {new_balance}")
        return True

    @category_exist_handler
    def check_balance(self, category: str, amount: float) -> bool:
        return self.db.get_balance(category) >= amount

    @category_exist_handler
    def send_to_category(self, from_category: str, to_category: str, amount: float) -> bool:
        res = self.top_down(from_category, amount, f"Перевод в категорию {to_category}")
        if not res:
            return False
        self.top_up(to_category, amount, f"Перевод из категории {from_category}")
        print(f"Перевод из категории {from_category} в категорию {to_category} на сумму {amount} завершен успешно.")
        return True

    @category_exist_handler
    def print_category_stats(self, category: str):
        ...


# if __name__ == '__main__':
#     db = DataBase()
#     wallet = Wallet()
#     wallet.add_category('Food')
#     wallet.add_category('Clothes')
#     wallet.top_up('Food', 100,)
#     wallet.top_up('Clothes', 100)
    # wallet.top_down('Food', 50)
    # wallet.send_to_category('Food', 'Clothes', 30)

print('Статистика для категории Food:')
x = PrettyTable(['Описание операции', 'Тип операции', 'Сумма'])
x.add_row(['Внесение средств', 'Пополнение', 10.000])

print(x)