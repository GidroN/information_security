# Some cipher (3 variant)
from string import ascii_letters


# Cesar cipher
def rot13(message, letter, reverse=False):
    if reverse:
        return message.translate(str.maketrans(ascii_letters, ascii_letters[ascii_letters.find(letter):] + ascii_letters[:ascii_letters.find(letter)]))
    return message.translate(str.maketrans(ascii_letters[ascii_letters.find(letter):] + ascii_letters[:ascii_letters.find(letter)], ascii_letters))


def encode(string: str, key: str) -> str:
    result = ''
    index = 0
    for letter in string:
        try:
            result += rot13(letter, key[index])
        except IndexError:
            index = 0
            result += rot13(letter, key[index])
        index += 1

    return result


def decode(string: str, key: str) -> str:
    result = ''
    index = 0
    for letter in string:
        try:
            result += rot13(letter, key[index], reverse=True)
        except IndexError:
            index = 0
            result += rot13(letter, key[index], reverse=True)
        index += 1

    return result


def main():
    prompt = input("1 - Encode or 2 - Decode?: ")

    if prompt == '1':
        string = input('Enter the string to encode: ')
        key = input('Enter the key: ')
        print(encode(string, key))
    elif prompt == '2':
        string = input('Enter the string to decode: ')
        key = input('Enter the key: ')
        print(decode(string, key))
    else:
        print("Enter please 1 or 2.")


if __name__ == '__main__':
    main()