from utils.dice import roll_dice, roll_d20

def perform_attack(attacker, target):
    attack_roll = roll_d20() + attacker.attack_bonus
    if attack_roll >= target.ac:
        damage = roll_damage(attacker.damage_dice) + attacker.damage_bonus
        target.take_damage(damage)
        return f"{attacker.name} hits {target.name} for {damage} damage!"
    else:
        return f"{attacker.name} misses {target.name}."

def roll_damage(damage_dice):
    dice_count, dice_size = map(int, damage_dice.split('d'))
    return roll_dice(dice_count, dice_size)