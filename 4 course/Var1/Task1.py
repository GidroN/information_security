import sqlite3
import os


class DataBase:
    def __init__(self, card_num: str, pin_code: str, filename: str = 'database.db'):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, filename)

        self.conn = self._get_connection(db_path)
        self.cur = self.conn.cursor()
        self._init_db()

        self.card_num = card_num
        self.pin_code = pin_code

    @staticmethod
    def _get_connection(path):
        if not os.path.exists(path):
            open(path, 'w').close()
        return sqlite3.connect(path)

    def _init_db(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS Account(
                ID INTEGER PRIMARY KEY,
                card_num VARCHAR(16),
                pin_code VARCHAR(6),
                balance REAL, -- FLOAT
                UNIQUE(card_num)
            );
                """
        )
        self.conn.commit()

    def check_row_exists(self, only_card_num=False) -> bool:
        query = "SELECT * FROM Account WHERE card_num = ?"

        if not only_card_num:
            query += "AND pin_code = ?"
            self.cur.execute(query, (self.card_num, self.pin_code))
        else:
            self.cur.execute(query, (self.card_num, ))

        return self.cur.fetchone() is not None

    def get_balance(self):
        query = "SELECT balance FROM Account WHERE card_num = ?"
        self.cur.execute(query, (self.card_num,))
        return self.cur.fetchone()[0]

    def set_balance(self, balance: float):
        query = "UPDATE Account SET balance = ? WHERE card_num = ?"
        self.cur.execute(query, (balance, self.card_num))
        self.conn.commit()

    def add_row(self):
        query = "INSERT INTO Account (card_num, pin_code, balance) VALUES (?, ?, ?);"
        self.cur.execute(query,(self.card_num, self.pin_code, 0.0))
        self.conn.commit()

    def delete_row(self):
        query = """DELETE FROM Account WHERE card_num = ?"""
        self.cur.execute(query, (self.card_num, ))
        self.conn.commit()


class BankAccount:
    def __init__(self,):
        self.logged_in = False
        self.db: DataBase = None

    @staticmethod
    def luhn_checksum(number: list[int]) -> int:
        nums = []
        for i in range(len(number)):
            digit = number[i]
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit = sum(map(int, str(digit)))
            nums.append(digit)
        full_sum = sum(nums)

        last_digit = full_sum % 10
        result = 10 - last_digit
        return result if result != 10 else 0

    def register(self, card_num: str, pin_code: str):
        card_num = card_num.replace(' ', '')

        if len(card_num) != 15 or not card_num.isdigit():
            return 'Invalid card number. It should be 15 digits.'
        if len(pin_code) != 6 or not pin_code.isdigit():
            return 'Invalid pin code. It should be 6 digits.'

        last_digit = self.luhn_checksum([int(i) for i in card_num])
        card_num += str(last_digit)

        self.db = DataBase(card_num, pin_code)
        if self.db.check_row_exists(only_card_num=True):
            return 'This card number is already taken. Try to login.'

        self.db.add_row()
        return f'You have successfully registered! Your card number is {card_num}.'

    def log_in(self, card_num: str, pin_code: str):
        card_num = card_num.replace(' ', '')
        self.db = DataBase(card_num, pin_code)
        if self.db.check_row_exists():
            self.logged_in = True
            return "You have been logged in!"
        return "Wrong credentials or may you have to register first."

    def top_up(self, amount: float):
        if self.logged_in:
            balance = self.db.get_balance()
            balance += amount
            self.db.set_balance(balance)
            return f"Successfully, your balance is {balance}"
        return "You have to register first!"

    def top_down(self, amount: float):
        if self.logged_in:
            balance = self.db.get_balance()
            new_balance = balance - amount
            if new_balance < 0:
                return f"Sorry, you have not enough money! Your balance is {balance}."
            self.db.set_balance(new_balance)
            return f"Successfully, your balance is {new_balance}"
        return "You have to register first!"

    def check_balance(self):
        if self.logged_in:
            balance = self.db.get_balance()
            return f"Your balance is: {balance}"
        return "You have to register first!"


if __name__ == '__main__':
    card_num = '4163168631469723'
    pin_code = '323614'
    account = BankAccount()
    # print(account.register(card_num, pin_code))
    print(account.log_in(card_num, pin_code))
    print(account.top_up(100))
    # print(account.top_down(50))
    # print(account.check_balance())
    # print(account.top_down(60))