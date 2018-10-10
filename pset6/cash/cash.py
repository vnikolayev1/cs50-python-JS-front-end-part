from cs50 import get_float
import sys

while True:
    change_owed = get_float("Change owed: ")
    if change_owed > 0 and change_owed <= sys.float_info.max:
        break
change_owed *= 100 + 0.5
print(change_owed)
change_owed = int(change_owed)
print(change_owed)
# we have coins 25, 10, 5, 1
coins = change_owed // 25
change_owed %= 25
print(coins)
coins += change_owed // 10
change_owed %= 10
print(coins)
coins += change_owed // 5
change_owed %= 5
print(coins)
coins += change_owed // 1
print(coins)