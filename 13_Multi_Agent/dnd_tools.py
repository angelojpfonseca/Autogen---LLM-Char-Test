tools = [
    {
        "name": "simulate_combat_turn",
        "description": "Simulates a D&D 5e combat turn between two characters.",
        "input_schema": {
            "type": "object",
            "properties": {
                "attacker": {
                    "type": "string",
                    "description": "The name of the attacking character."
                },
                "defender": {
                    "type": "string",
                    "description": "The name of the defending character."
                }
            },
            "required": ["attacker", "defender"]
        }
    }
]