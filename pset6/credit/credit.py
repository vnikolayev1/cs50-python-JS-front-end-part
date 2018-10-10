from cs50 import get_int

while True:
    card = get_int("Enter card number: ")
    if (card > 0) and card < 10**16:
        break
card_digits = card
odd = 0
even = 0
while not card_digits == 0:
    odd = odd + ((((card_digits % 100 // 10) * 2) % 10) + (((card_digits % 100 // 10) * 2) // 10))  # Luhn's 2nd digit sum
    even = even + (card_digits % 10)
    card_digits //= 100
sum_digits = (odd + even) % 10
if sum_digits == 0:
    if card // 10**12 == 4 or card // 10**15 == 4:
        print("VISA")
    elif card // 10**14 == 34 or card // 10**13 == 37:
        print("AMEX")
    elif card // 10**14 >= 51 and card // 10**14 <= 55:
        print("MASTERCARD")
    else:
        print("INVALID")
else:
    print("INVALID")