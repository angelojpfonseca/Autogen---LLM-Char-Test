# tools.py
import random

def roll_dice(dice_string):
    """Roll dice based on a string like '2d6' or '1d8+3'"""
    if '+' in dice_string:
        dice, modifier = dice_string.split('+')
        modifier = int(modifier)
    else:
        dice = dice_string
        modifier = 0
    
    num_dice, dice_type = map(int, dice.split('d'))
    roll = sum(random.randint(1, dice_type) for _ in range(num_dice))
    return roll + modifier

def attack_roll(attacker, target, attack_bonus, damage_dice):
    d20_roll = random.randint(1, 20)
    total_attack = d20_roll + attack_bonus
    damage = roll_dice(damage_dice)
    
    return {
        "attacker": attacker,
        "target": target,
        "d20_roll": d20_roll,
        "attack_bonus": attack_bonus,
        "total_attack": total_attack,
        "damage": damage
    }

def defend(defender, defender_ac, defender_hp, attack_roll, damage):
    is_hit = attack_roll >= defender_ac
    new_hp = defender_hp
    
    if is_hit:
        new_hp = max(0, defender_hp - damage)
    
    return {
        "defender": defender,
        "success": is_hit,
        "damage": damage if is_hit else 0,
        "original_hp": defender_hp,
        "new_hp": new_hp
    }