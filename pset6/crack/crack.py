from cs50 import get_string
from itertools import product
import sys
from string import ascii_letters
from crypt import crypt

if not len(sys.argv) == 2:
    print("Too many or not enough arguments")
    exit(1)
salt = sys.argv[1][:2]
for num_of_digits in range(1, 6):
    key_variants = product(ascii_letters, repeat=num_of_digits)
    for i in key_variants:
        crypted_word = crypt("".join(i), salt)
        if crypted_word == sys.argv[1]:
            print("".join(i))
            exit()
print("Password we cracking is not in range a-Z of 5 digits")