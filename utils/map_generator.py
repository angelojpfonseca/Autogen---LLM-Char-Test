import pygame
import random

class TerrainType:
    PLAIN = 0
    WALL = 1
    WATER = 2
    FOREST = 3

class PygameMapGenerator:
    def __init__(self, width, height, cell_size=30):
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.map = [[TerrainType.PLAIN for _ in range(width)] for _ in range(height)]
        
        pygame.init()
        self.screen = pygame.display.set_mode((width * cell_size, height * cell_size))
        pygame.display.set_caption("D&D Combat Simulator")
        
        self.colors = {
            TerrainType.PLAIN: (200, 200, 100),  # Light yellow
            TerrainType.WALL: (100, 100, 100),   # Gray
            TerrainType.WATER: (100, 100, 255),  # Blue
            TerrainType.FOREST: (0, 150, 0)      # Green
        }
        
        self.character_colors = [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
        ]

    def generate_map(self, complexity=0.1, water_ratio=0.1, forest_ratio=0.2):
        self._generate_terrain(TerrainType.WALL, complexity)
        self._generate_terrain(TerrainType.WATER, water_ratio)
        self._generate_terrain(TerrainType.FOREST, forest_ratio)

    def _generate_terrain(self, terrain_type, ratio):
        num_cells = int(self.width * self.height * ratio)
        for _ in range(num_cells):
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            self.map[y][x] = terrain_type

    def is_valid_position(self, x, y):
        return (0 <= x < self.width and 
                0 <= y < self.height and 
                self.map[y][x] != TerrainType.WALL)

    def get_random_valid_position(self):
        while True:
            x, y = random.randint(0, self.width - 1), random.randint(0, self.height - 1)
            if self.is_valid_position(x, y):
                return x, y

    def draw_map(self, characters):
        self.screen.fill((0, 0, 0))  # Fill screen with black
        
        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                pygame.draw.rect(self.screen, self.colors[cell], 
                                 (x * self.cell_size, y * self.cell_size, 
                                  self.cell_size, self.cell_size))
                
                # Draw grid lines
                pygame.draw.rect(self.screen, (50, 50, 50), 
                                 (x * self.cell_size, y * self.cell_size, 
                                  self.cell_size, self.cell_size), 1)
        
        # Draw characters
        font = pygame.font.Font(None, 24)
        for i, char in enumerate(characters):
            if char.is_alive():
                x, y = char.position
                color = self.character_colors[i % len(self.character_colors)]
                pygame.draw.circle(self.screen, color, 
                                   (x * self.cell_size + self.cell_size // 2, 
                                    y * self.cell_size + self.cell_size // 2), 
                                   self.cell_size // 3)
                text = font.render(char.name[0], True, (0, 0, 0))
                text_rect = text.get_rect(center=(x * self.cell_size + self.cell_size // 2, 
                                                  y * self.cell_size + self.cell_size // 2))
                self.screen.blit(text, text_rect)
        
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
        return True

def create_battle_map(width, height, cell_size=30):
    map_gen = PygameMapGenerator(width, height, cell_size)
    map_gen.generate_map()
    return map_gen

# Example usage
if __name__ == "__main__":
    battle_map = create_battle_map(20, 15)
    running = True
    while running:
        battle_map.draw_map([])
        running = battle_map.handle_events()
    pygame.quit()