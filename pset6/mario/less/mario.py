height = -1
while height > 23 or height < 0:
    height = int(input("Enter a number: "))
if height == 0:
    exit()
else:
    for hashes in range(1, height + 1, 1):
        print(" " * (height - hashes), end="")
        print("#" * hashes)