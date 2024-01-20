from prettytable import PrettyTable
from functools import wraps
import os
import sqlite3




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

    def get_money_rows_from_category(self, category: str, operation: str) -> list[tuple[int]]:
        prompt = f"SELECT SUM(change) FROM {category.capitalize()} WHERE operation='{operation}'"
        self.cur.execute(prompt)
        return self.cur.fetchone()[0]

    def get_info_rows_from_category(self, category: str) -> list[tuple[str, int]]:
        prompt = f"SELECT description, operation, change FROM {category.capitalize()};"
        self.cur.execute(prompt)
        return self.cur.fetchall()

    def check_table_exists(self, category: str) -> int:
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
                    VALUES ({balance}, '{self.TOP_UP}', {balance}, 'Создание новой категории');
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

    @staticmethod
    def category_exist_handler(func):
        @wraps(func)
        def wrapper(self, category: str | list, *args, **kwargs):
            categories = [category] if isinstance(category, str) else category
            missing_categories = [cat for cat in categories if not self.db.check_table_exists(cat)]

            if missing_categories:
                missing_str = ', '.join(missing_categories)
                print(f'Категории {missing_str} не существует. Сначала добавьте ее/их.')
                return

            return func(self, category, *args, **kwargs)

        return wrapper

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
    def print_category_stats(self, category: str) -> None:
        print(f'Статистика для категории {category.capitalize()}: ')
        table = PrettyTable(['Описание операции', 'Тип операции', 'Сумма'])
        items = self.db.get_info_rows_from_category(category)

        for row in items:
            table.add_row(list(row))

        total = self.db.get_balance(category)
        table.add_row(['ИТОГО', '', total])

        print(table)

    def _calculate_percent_spend_for_each_category(self, categories: list[str]) -> list[tuple[str, float]]:
        result = []
        spend_money = []
        earned_money = []

        for category in categories:
            total_spend_in_category = self.db.get_money_rows_from_category(category, self.db.TOP_DOWN)
            total_earned_in_category = self.db.get_money_rows_from_category(category, self.db.TOP_UP)

            spend_money.append((category, total_spend_in_category))
            earned_money.append((category, total_earned_in_category))

        total_earned = sum(item[1] for item in earned_money)

        for category, amount_spend in spend_money:
            amount_spend = 0.0 if not amount_spend else amount_spend
            percent = round((amount_spend / total_earned) * 100, 2)
            result.append((category, percent))

        return result

    @category_exist_handler
    def calculate_percent_spend_for_each_category(self, categories: list) -> None:
        spend_in_categories = self._calculate_percent_spend_for_each_category(categories)
        table = PrettyTable(['Категория', 'потраченный % от общей суммы'])
        for category, percent in spend_in_categories:
            table.add_row([category, percent])

        print(table)


if __name__ == '__main__':
    wallet = Wallet()
    wallet.add_category('Food')
    wallet.add_category('Clothes')
    wallet.top_up('Food', 100,)
    wallet.top_up('Clothes', 100)
    wallet.top_down('Food', 50)
    wallet.top_down('Clothes', 100)
    wallet.send_to_category('Food', 'Clothes', 30)
    wallet.print_category_stats('food')
    wallet.print_category_stats('clothes')
    wallet.calculate_percent_spend_for_each_category(['food', 'clothes'])

