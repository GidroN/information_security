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

    def add_category(self, category: str):
        prompt = """
                    CREATE TABLE IF NOT EXISTS {category}(
                        ID INTEGER PRIMARY KEY,
                        balance REAL,
                        operation VARCHAR(50),
                        change REAL,
                        description TEXT 
                    );
                 """.format(category=category.capitalize())

        self.cur.execute(prompt)
        self.conn.commit()

    def add_operation(self, category: str, balance: float, operation: str, change: float, description: str):
        prompt = ("INSERT INTO {category} (balance, operation, change, description) "
                  "VALUES (?, ?, ?, ?);").format(category=category.capitalize())

        self.cur.execute(prompt, (balance, operation, change, description))
        self.conn.commit()

    def get_balance(self, category: str):
        prompt = f"SELECT balance FROM {category} ORDER BY ID DESC LIMIT 1;".format(category=category.capitalize())

        self.cur.execute(prompt, (category, ))
        return self.cur.fetchone()[0]


class Wallet:
    def __init__(self):
        self.db = DataBase()

    def add_category(self, category: str):
        self.db.add_category(category)
        return "Новая категория успешно добавлена. Можете вносить операции."

    def top_up(self, amount: float, description: str = ''):
        balance = self.db.get 

    def top_down(self, amount: float, description: str = '') -> bool:
        ...

    def check_balance(self, amount: float, category: str) -> bool:
        ...

    def send_to_category(self, amount: float, category: str):
        ...

    def print_wallet(self):
        ...


db = DataBase()
db.add_category('food')
db.add_operation('food', 10.0, db.TOP_UP, 10, '')