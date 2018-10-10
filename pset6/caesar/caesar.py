import sys
from cs50 import get_string

if not len(sys.argv) == 2:
    print("Too many or not enough arguments.")
    exit(1)
if sys.argv[1].isnumeric():
    key = int(sys.argv[1])
    word = get_string("Enter your phrase: ")
    print("ciphertext: ", end="")
    for character in word:
        if character.islower():
            character = chr(((ord(character) - 96 + key) % 26) + 96)
        elif character.isupper():
            character = chr(((ord(character) - 64 + key) % 26) + 64)
        print(character, end="")
    print()
else:
    print("Key has to be a number")