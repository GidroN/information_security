# Some cipher (1 variant)

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

    for outer_index in range(rows):
        for inner_index in range(columns):
            if table[outer_index][inner_index] == '':
                table[outer_index][inner_index] = '$'


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
    rows = key
    columns = len(string) // key if len(string) % key == 0 else len(string) // key + 1
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

    number_of_special_symbols = 0
    for i in range(len(result) - 1, -1, -1):
        if result[i] == '$':
            number_of_special_symbols += 1
        else:
            break

    return result[:len(result) - number_of_special_symbols]


def main():
    prompt = input("1 - Encode or 2 - Decode?: ")

    if prompt == '1':
        string = input('Enter the string to encode: ')
        key = int(input('Enter the key: '))
        print(encode(string, key))
    elif prompt == '2':
        string = input('Enter the string to decode: ')
        key = int(input('Enter the key: '))
        print(decode(string, key))
    else:
        print("Enter please 1 or 2.")


if __name__ == '__main__':
    main()
