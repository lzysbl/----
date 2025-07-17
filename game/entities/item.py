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
        elif name == "血瓶":
            self.color = (255, 0, 255)  # 药水紫色
        else:
            self.color = (0, 255, 255)  # 其他物品青色

    def draw(self, surface):
        if self.name == "Gold":
            # 绘制金币为圆形
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size//2)
        elif self.name == "血瓶":
            # 绘制血瓶为圆形药瓶
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size//2)
            # 添加瓶口
            pygame.draw.circle(surface, (200, 200, 200), (int(self.x), int(self.y - self.size//3)), 3)
        else:
            # 绘制其他物品为方形
            pygame.draw.rect(
                surface,
                self.color,
                pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)
            )

    def get_rect(self):
        return pygame.Rect(self.x - self.size//2, self.y - self.size//2, self.size, self.size)

    @staticmethod
    def create_safe_item(name, game_map, existing_items=None):
        """创建一个安全位置的物品，避免与墙体和其他物品重叠"""
        if existing_items is None:
            existing_items = []
        
        item_size = 20
        safe_distance = 30  # 与其他物品的最小距离
        
        # 尝试100次找到安全位置
        for _ in range(100):
            x, y = game_map.find_safe_position(0, 0, width=item_size, height=item_size)
            
            # 检查是否离墙体太近
            if game_map.is_position_near_walls(x, y):
                continue
            
            # 检查是否与现有物品重叠
            safe_position = True
            for existing_item in existing_items:
                distance = ((x - existing_item.x) ** 2 + (y - existing_item.y) ** 2) ** 0.5
                if distance < safe_distance:
                    safe_position = False
                    break
            
            if safe_position:
                return Item(name, x, y)
        
        # 如果找不到安全位置，返回默认位置
        return Item(name, game_map.WIDTH * game_map.TILE_SIZE // 2, game_map.HEIGHT * game_map.TILE_SIZE // 2)
