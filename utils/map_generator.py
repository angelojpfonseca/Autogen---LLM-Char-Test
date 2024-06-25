import random
from enum import Enum

class TerrainType(Enum):
    PLAIN = ('·', '\033[92m')  # Light green
    WALL = ('█', '\033[90m')   # Dark gray
    WATER = ('≈', '\033[94m')  # Blue
    FOREST = ('♠', '\033[32m') # Dark green

class MapGenerator:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[TerrainType.PLAIN for _ in range(width)] for _ in range(height)]

    def generate_map(self, complexity=0.1, water_ratio=0.1, forest_ratio=0.2):
        self._generate_terrain(TerrainType.WALL, complexity)
        self._generate_terrain(TerrainType.WATER, water_ratio)
        self._generate_terrain(TerrainType.FOREST, forest_ratio)

    def _generate_terrain(self, terrain_type, ratio):
        num_cells = int(self.width * self.height * ratio)
        for _ in range(num_cells):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self.map[y][x] = terrain_type

    def get_map(self):
        return [[cell for cell in row] for row in self.map]

    def print_map(self, characters=None):
        if characters is None:
            characters = []
        
        char_positions = {(c.position[0], c.position[1]): c for c in characters if c.is_alive()}
        
        print('╔' + '═' * (self.width * 2) + '╗')
        for y, row in enumerate(self.map):
            print('║', end='')
            for x, cell in enumerate(row):
                if (x, y) in char_positions:
                    char = char_positions[(x, y)]
                    print(f'\033[1m\033[93m{char.name[0]}\033[0m', end=' ')  # Bold yellow for characters
                else:
                    print(f'{cell.value[1]}{cell.value[0]}\033[0m', end=' ')
            print('║')
        print('╚' + '═' * (self.width * 2) + '╝')
        
        print("\nCharacter Legend:")
        for char in characters:
            if char.is_alive():
                print(f"\033[1m\033[93m{char.name[0]}\033[0m: {char.name} (HP: {char.hp})")

    def is_valid_position(self, x, y):
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                self.map[y][x] != TerrainType.WALL)

    def get_random_valid_position(self):
        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if self.is_valid_position(x, y):
                return x, y

def create_battle_map(width, height, complexity=0.1, water_ratio=0.1, forest_ratio=0.2):
    map_gen = MapGenerator(width, height)
    map_gen.generate_map(complexity, water_ratio, forest_ratio)
    return map_gen

# Example usage
if __name__ == "__main__":
    battle_map = create_battle_map(20, 10)
    battle_map.print_map()
    print("\nRandom valid position:", battle_map.get_random_valid_position())