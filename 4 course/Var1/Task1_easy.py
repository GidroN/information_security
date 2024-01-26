class BankAccount:
    accounts = {}

    def __init__(self):
        self.logged_in = False
        self.card_num = ''
        self.pin_code = ''

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
        return 0 if result == 10 else result

    def register(self, card_num: str, pin_code: str):
        card_num = card_num.replace(' ', '')

        if len(card_num) != 15 or not card_num.isdigit():
            return 'Invalid card number. It should be 15 digits.'
        if len(pin_code) != 6 or not pin_code.isdigit():
            return 'Invalid pin code. It should be 6 digits.'

        last_digit = self.luhn_checksum([int(i) for i in card_num])
        card_num += str(last_digit)

        if card_num in self.accounts:
            return 'This card number is already taken. Try to login.'

        self.accounts[card_num] = {'pin_code': pin_code, 'balance': 0.0}
        return f'You have successfully registered! Your card number is {card_num}.', card_num

    def log_in(self, card_num: str, pin_code: str):
        card_num = card_num.replace(' ', '')

        if card_num in self.accounts and self.accounts[card_num]['pin_code'] == pin_code:
            self.logged_in = True
            self.card_num = card_num
            self.pin_code = pin_code
            return "You have been logged in!"
        return "Wrong credentials or may you have to register first."

    def top_up(self, amount: float):
        if self.logged_in:
            self.accounts[self.card_num]['balance'] += amount
            return f"Successfully, your balance is {self.accounts[self.card_num]['balance']}"
        return "You have to register first!"

    def top_down(self, amount: float):
        if self.logged_in:
            if self.accounts[self.card_num]['balance'] >= amount:
                self.accounts[self.card_num]['balance'] -= amount
                return f"Successfully, your balance is {self.accounts[self.card_num]['balance']}"
            return f"Sorry, you have not enough money! Your balance is {self.accounts[self.card_num]['balance']}."
        return "You have to register first!"

    def check_balance(self):
        if self.logged_in:
            return f"Your balance is: {self.accounts[self.card_num]['balance']}"
        return "You have to register first!"


if __name__ == '__main__':
    account = BankAccount()
    card_num = '4163 1686 3146 972'
    pin_code = '201982'
    print(account.register(card_num, pin_code))
    # print(account.log_in(card_num, pin_code))
    # print(account.top_up(19_242))
    # print(account.top_down(9_000))
    # print(account.top_down(10_000))
    # print(account.top_down(250))

