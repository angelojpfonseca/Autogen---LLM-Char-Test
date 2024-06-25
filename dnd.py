import random

class SimpleNPC:
    def __init__(self, name, ac, hp, attack_bonus, fixed_damage):
        self.name = name
        self.ac = ac  # Armor Class
        self.hp = hp  # Directly assign Hit Points
        self.attack_bonus = attack_bonus  # Attack bonus
        self.fixed_damage = fixed_damage  # Fixed damage

    def __str__(self):
        return f"{self.name}"

    def display_stats(self):
        print(f"Name: {self.name}")
        print(f"Armor Class: {self.ac}")
        print(f"Hit Points: {self.hp}")
        print(f"Attack Bonus: +{self.attack_bonus}")
        print(f"Fixed Damage: {self.fixed_damage}")

    def attack(self, target):
        attack_roll = random.randint(1, 20)
        total_attack_roll = attack_roll + self.attack_bonus
        if total_attack_roll >= target.ac:
            target.hp -= self.fixed_damage
            print(f"{self.name} rolls a {attack_roll} + {self.attack_bonus} = {total_attack_roll} to hit {target.name}.")
            print(f"{self.name} hits {target.name} for {self.fixed_damage} damage. {target.name} has {target.hp} HP left.")
            return self.fixed_damage
        else:
            print(f"{self.name} rolls a {attack_roll} + {self.attack_bonus} = {total_attack_roll} to hit {target.name}.")
            print(f"{self.name} misses {target.name}.")
            return 0

def combat(npc1, npc2):
    print(f"Combat starts between {npc1.name} and {npc2.name}!\n")

    # Determine initiative
    initiative_npc1 = random.randint(1, 20)
    initiative_npc2 = random.randint(1, 20)
    print(f"{npc1.name} rolls a {initiative_npc1} for initiative.")
    print(f"{npc2.name} rolls a {initiative_npc2} for initiative.")

    if initiative_npc1 > initiative_npc2:
        first, second = npc1, npc2
    else:
        first, second = npc2, npc1

    print(f"{first.name} wins the initiative and will attack first.")

    round_counter = 1
    while npc1.hp > 0 and npc2.hp > 0:
        print(f"\nRound {round_counter}:")
        if first.attack(second) > 0 and second.hp > 0:
            second.attack(first)
        elif second.hp > 0:
            second.attack(first)
        round_counter += 1
        print("\n" + "-"*40 + "\n")

    if npc1.hp > 0:
        print(f"{npc1.name} wins!")
    else:
        print(f"{npc2.name} wins!")

# Define multiple simplified NPCs
simple_npcs_data = [
    {
        "name": "Goblin",
        "ac": 15,
        "hp": 7,  # Directly assign Hit Points
        "attack_bonus": 4,  # Directly assign Attack Bonus
        "fixed_damage": 5  # Fixed damage for the Goblin's attack
    },
    {
        "name": "Orc",
        "ac": 13,
        "hp": 15,  # Directly assign Hit Points
        "attack_bonus": 5,  # Directly assign Attack Bonus
        "fixed_damage": 9  # Fixed damage for the Orc's attack
    }
]

# Create multiple simplified NPCs
simple_npcs = [SimpleNPC(**data) for data in simple_npcs_data]

# Simulate combat between the two NPCs
combat(simple_npcs[0], simple_npcs[1])
