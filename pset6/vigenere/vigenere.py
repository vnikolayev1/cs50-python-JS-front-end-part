import sys
from cs50 import get_string

if not len(sys.argv) == 2:
    print("Too many or not enough arguments")
    exit(1)
if sys.argv[1].isalpha():
    key = sys.argv[1].lower()
    word = get_string("Enter your phrase: ")
    keylen_counter = 0
    print("ciphertext: ", end="")
    for character in word:
        if keylen_counter == len(key):
            keylen_counter = 0
        if character.islower():
            character = chr(((ord(character) - 97 + ord(key[keylen_counter]) - 97) % 26) + 97)
            keylen_counter += 1
        elif character.isupper():
            character = chr(((ord(character) - 65 + ord(key[keylen_counter]) - 97) % 26) + 65)
            keylen_counter += 1
        print(character, end="")
    print()
else:
    print("Input has to be alphabetical.")
    exit(1)