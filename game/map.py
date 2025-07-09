import pygame

class GameMap:
    """简单网格地图示例"""
    TILE_SIZE = 32
    WIDTH = 25
    HEIGHT = 18

    def __init__(self):
        # 生成随机地形: 0-可走，1-障碍
        import random
        self.grid = [[random.choice([0, 0, 0, 1]) for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                color = (50, 50, 50) if tile == 0 else (100, 100, 100)
                pygame.draw.rect(
                    surface,
                    color,
                    pygame.Rect(x*self.TILE_SIZE, y*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                )
