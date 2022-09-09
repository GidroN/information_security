# Some cipher

def encode(string: str, key: str) -> str:
    result = ''
    for index, symbol in enumerate(string):
        result += ord(symbol) ^ ord(key[index])

    return result


def decode(string: str, key: str) -> str:
    result = '' 
    for index, symbol in enumerate(string):
        result += ord(symbol) ^ ord(key[index])

    return result
    
 
def main():
    prompt = input("1 - Encode or 2 - Decode?: ")
    string = input("Enter the string: ")
    key = input("Enter the key: ")

    if len(key) < len(string):
        print("Error: key must be longer or equal to string.")
        quit()
    
    if prompt == '1':
        print(encode(string, key))
    else:
        print(decode(string, key))


if __name__ == '__main__':
    main()
