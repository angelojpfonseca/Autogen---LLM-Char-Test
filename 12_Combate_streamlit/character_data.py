from character_sheet import CharacterSheet, Ability, Action

characters = {
    "orc": CharacterSheet(
        name="Orc",
        type="humanoid (orc)",
        size="Medium",
        alignment="chaotic evil",
        armor_class=13,
        hit_points=15,
        hit_dice="2d8+6",
        speed="30 ft.",
        abilities={
            "STR": Ability(16, 3),
            "DEX": Ability(12, 1),
            "CON": Ability(16, 3),
            "INT": Ability(7, -2),
            "WIS": Ability(11, 0),
            "CHA": Ability(10, 0)
        },
        skills={"Intimidation": 2},
        senses={"Darkvision": "60 ft."},
        languages=["Common", "Orc"],
        challenge_rating="1/2",
        xp=100,
        traits={
            "Aggressive": "As a bonus action, the orc can move up to its speed toward a hostile creature that it can see."
        },
        actions=[
            Action(
                name="Greataxe",
                description="Melee Weapon Attack: +5 to hit, reach 5 ft., one target.",
                attack_bonus=5,
                damage_dice="1d12",
                damage_bonus=3
            ),
            Action(
                name="Javelin",
                description="Ranged Weapon Attack: +5 to hit, range 30/120 ft., one target.",
                attack_bonus=5,
                damage_dice="1d6",
                damage_bonus=3
            )
        ]
    ),
    "goblin": CharacterSheet(
        name="Goblin",
        type="humanoid (goblinoid)",
        size="Small",
        alignment="neutral evil",
        armor_class=15,
        hit_points=7,
        hit_dice="2d6",
        speed="30 ft.",
        abilities={
            "STR": Ability(8, -1),
            "DEX": Ability(14, 2),
            "CON": Ability(10, 0),
            "INT": Ability(10, 0),
            "WIS": Ability(8, -1),
            "CHA": Ability(8, -1)
        },
        skills={"Stealth": 6},
        senses={"Darkvision": "60 ft."},
        languages=["Common", "Goblin"],
        challenge_rating="1/4",
        xp=50,
        traits={
            "Nimble Escape": "The goblin can take the Disengage or Hide action as a bonus action on each of its turns."
        },
        actions=[
            Action(
                name="Scimitar",
                description="Melee Weapon Attack: +4 to hit, reach 5 ft., one target.",
                attack_bonus=4,
                damage_dice="1d6",
                damage_bonus=2
            ),
            Action(
                name="Shortbow",
                description="Ranged Weapon Attack: +4 to hit, range 80/320 ft., one target.",
                attack_bonus=4,
                damage_dice="1d6",
                damage_bonus=2
            )
        ]
    )
}