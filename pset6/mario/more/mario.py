from cs50 import get_int
while True:
    height = get_int("Enter a number: ")
    if height >= 0 and height <= 23:
        break
for hashes in range(1, height + 1, 1):
    print(" " * (height - hashes), end="")
    print("#" * hashes, end="")
    print(" " * 2, end="")
    print("#" * hashes)