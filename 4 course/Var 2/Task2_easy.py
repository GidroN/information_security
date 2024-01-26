class Wallet:
    TOP_UP = 'Пополнение'
    TOP_DOWN = 'Снятие'

    def __init__(self):
        self.categories = {}

    def add_category(self, category: str, balance: float = 0.0):
        if category in self.categories:
            print("Данная категория уже добавлена.")
            return False

        self.categories[category] = {
            "operations": [],  # внутри списка кортежи - (описание, тип операции, сумма)
            "balance": balance
        }

        if balance != 0.0:
            self.categories[category]["operations"].append(('Создание новой категории', self.TOP_UP, balance))

        print("Новая категория успешно добавлена.")
        return True

    def change_balance(self, category: str, amount: float, operation: str, description):
        current_balance = self.categories[category]["balance"]

        if operation == self.TOP_UP:
            new_balance = current_balance + amount
        elif operation == self.TOP_DOWN:
            new_balance = current_balance - amount

        if new_balance < 0:
            print("Недостаточно средств.")
            return False

        self.categories[category]["balance"] = new_balance
        self.categories[category]["operations"].append((description, operation, amount))
        print(f"Операция {operation} успешна. Баланс в категории {category}: {new_balance}")
        return True

    def top_up(self, category: str, amount: float, description: str = ''):
        if category not in self.categories:
            print("Категория не найдена.")
            return False

        return self.change_balance(category, amount, self.TOP_UP, description)

    def top_down(self, category: str, amount: float, description: str = ''):
        if category not in self.categories:
            print("Категория не найдена.")
            return False

        return self.change_balance(category, amount, self.TOP_DOWN, description)

    def print_category_stats(self, category: str):
        if category not in self.categories:
            print("Категория не найдена.")
            return

        print(f'Статистика для категории {category}: ')
        for operation in self.categories[category]["operations"]:
            print(f'Описание: {operation[0]}, Тип: {operation[1]}, Сумма: {operation[2]}')
        print(f'Итоговый баланс: {self.categories[category]["balance"]}')

    def calculate_percent_spend(self):
        total_top_up = 0.0
        for category in self.categories:
            for operation in self.categories[category]["operations"]:
                operation_type = operation[1]
                amount = operation[2]

                if operation_type == self.TOP_UP:
                    total_top_up += amount

        if total_top_up == 0.0:
            print("Нет операций пополнения.")
            return

        print("Процент расходов по категориям:")
        for category in self.categories:
            total_top_down = 0.0
            for operation in self.categories[category]["operations"]:
                operation_type = operation[1]
                amount = operation[2]

                if operation_type == self.TOP_DOWN:
                    total_top_down += amount

            percent = (total_top_down / total_top_up) * 100
            print(f"{category}: {percent:.2f}%")


if __name__ == '__main__':
    wallet = Wallet()
    wallet.add_category("Развлечения", 1000)
    wallet.top_up("Развлечения", 500, "Пополнение наличными")
    wallet.top_down("Развлечения", 200, "Кино")
    wallet.print_category_stats("Развлечения")
    wallet.calculate_percent_spend()
