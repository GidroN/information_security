# Some cipher (2 variant)

def encode(string: str, key: str) -> str:
    result = ''
    for index, symbol in enumerate(string):
        result += str(ord(symbol) ^ ord(key[index]))
        result += ' '

    return result


def decode(string: str, key: str) -> str:
    result = '' 
    for index, symbol in enumerate(string.split()):
        result += chr(int(symbol) ^ ord(key[index]))

    return result

 
def main():
    prompt = input("1 - Encode or 2 - Decode?: ")
    
    if prompt == '1':
        string = input("Enter the string to encode: ")
        key = input("Enter the key: ")
        if len(key) < len(string):
            print("Error: key must be longer or equal to string.")
            quit()
        print(f"Encoded string: {encode(string, key)}")

    elif prompt == '2':
        string = input("Enter the string to decode: ")
        key = input("Enter the key: ")
        if len(key) < len(string.split()):
            print("Error: key must be longer or equal to string.")
            quit()
        print(f"Decoded string: {decode(string, key)}")
    else:
        print("Enter please 1 or 2.")

if __name__ == '__main__':
    main()
