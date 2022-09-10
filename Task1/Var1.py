# Some others cipher

def encode(string: str, key: int) -> str:
    columns = key
    rows = len(string) // key if len(string) % key == 0 else len(string) // key + 1
    table = [['' for i in range(columns)] for i in range(rows)]
    inner_index = outer_index = 0

    for letter in string:
        try:
            table[outer_index][inner_index] = letter
        except IndexError:
            inner_index = 0
            outer_index += 1
            table[outer_index][inner_index] = letter
        inner_index += 1

    print(table)

    inner_index = outer_index = 0
    result = ''

    for _ in range(columns * rows):
        try:
            result += table[outer_index][inner_index]
        except IndexError:
            inner_index += 1
            outer_index = 0
            result += table[outer_index][inner_index]
        outer_index += 1

    return result


def decode(string: str, key: int) -> str:
    pass


def main():
    string = input('Enter the string: ')
    key = int(input('Enter the key: '))
    print(encode(string, key))


if __name__ == '__main__':
    main()
