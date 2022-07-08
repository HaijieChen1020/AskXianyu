import random
from exception.exceptions import InvalidNumberException

def roll_dice(lower, upper):
    try:
        num1 = int(lower)
        num2 = int(upper)
    except Exception:
        raise InvalidNumberException("arg1 and arg2 has to be numbers")
    if not num1 <= num2:
        raise InvalidNumberException("arg1 must smaller than arg2")
    return random.randint(num1, num2)