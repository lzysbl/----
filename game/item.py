import pygame

class Item:
    """地图上可拾取的物品"""
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.size = 20
        # 金币黄色
        if name == "Gold":
            self.color = (255, 215, 0)  # 金币黄色
        elif name == "Potion":
            self.color = (255, 0, 255)  # 药水紫色
        else:
            self.color = (0, 255, 255)  # 其他物品青色

    def draw(self, surface):
        if self.name == "Gold":
            # 绘制金币为圆形
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size//2)
        else:
            # 绘制其他物品为方形
            pygame.draw.rect(
                surface,
                self.color,
                pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
            )

    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
