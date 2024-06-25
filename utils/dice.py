import random

def roll_dice(count, sides):
    return sum(random.randint(1, sides) for _ in range(count))

def roll_d20():
    return random.randint(1, 20)

# If you need any other specific dice rolls, you can add them here