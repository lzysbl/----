import pygame

class GameMap:
    """带碰撞检测的游戏地图"""
    TILE_SIZE = 32
    WIDTH = 25
    HEIGHT = 18

    def __init__(self):
        # 创建地图: 0-可走，1-墙体
        self.grid = self.create_map()
        
    def create_map(self):
        """创建地图布局"""
        # 初始化空地图
        grid = [[0 for _ in range(self.WIDTH)] for _ in range(self.HEIGHT)]
        
        # 添加边界墙
        for x in range(self.WIDTH):
            grid[0][x] = 1  # 上边界
            grid[self.HEIGHT-1][x] = 1  # 下边界
        for y in range(self.HEIGHT):
            grid[y][0] = 1  # 左边界
            grid[y][self.WIDTH-1] = 1  # 右边界
        
        # 添加一些内部墙体
        import random
        for y in range(2, self.HEIGHT-2):
            for x in range(2, self.WIDTH-2):
                if random.random() < 0.15:  # 15%概率生成墙体
                    grid[y][x] = 1
        
        # 添加一些房间结构
        self.add_rooms(grid)
        
        return grid
    
    def add_rooms(self, grid):
        """添加一些房间结构"""
        # 左上角房间
        for y in range(3, 7):
            for x in range(3, 8):
                grid[y][x] = 0
        # 房间墙体
        for x in range(3, 8):
            grid[2][x] = 1
            grid[7][x] = 1
        for y in range(3, 7):
            grid[y][2] = 1
            grid[y][8] = 1
        # 房间门口
        grid[5][2] = 0
        
        # 右下角房间
        for y in range(self.HEIGHT-7, self.HEIGHT-3):
            for x in range(self.WIDTH-8, self.WIDTH-3):
                grid[y][x] = 0
        # 房间墙体
        for x in range(self.WIDTH-8, self.WIDTH-3):
            grid[self.HEIGHT-8][x] = 1
            grid[self.HEIGHT-2][x] = 1
        for y in range(self.HEIGHT-7, self.HEIGHT-3):
            grid[y][self.WIDTH-9] = 1
            grid[y][self.WIDTH-2] = 1
        # 房间门口
        grid[self.HEIGHT-5][self.WIDTH-9] = 0

    def draw(self, surface):
        """绘制地图"""
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                rect = pygame.Rect(x*self.TILE_SIZE, y*self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                if tile == 0:  # 可走区域
                    pygame.draw.rect(surface, (50, 50, 50), rect)
                    pygame.draw.rect(surface, (70, 70, 70), rect, 1)  # 网格线
                else:  # 墙体
                    pygame.draw.rect(surface, (100, 50, 50), rect)
                    pygame.draw.rect(surface, (120, 70, 70), rect, 2)  # 墙体边框
    
    def is_wall(self, x, y):
        """检查指定像素坐标是否是墙体"""
        grid_x = int(x // self.TILE_SIZE)
        grid_y = int(y // self.TILE_SIZE)
        
        # 边界检查
        if grid_x < 0 or grid_x >= self.WIDTH or grid_y < 0 or grid_y >= self.HEIGHT:
            return True  # 超出边界视为墙体
        
        return self.grid[grid_y][grid_x] == 1
    
    def can_move_to(self, x, y, width=28, height=28):
        """检查实体是否可以移动到指定位置"""
        # 检查实体四个角是否碰撞墙体
        corners = [
            (x - width//2, y - height//2),  # 左上
            (x + width//2, y - height//2),  # 右上
            (x - width//2, y + height//2),  # 左下
            (x + width//2, y + height//2),  # 右下
        ]
        
        for corner_x, corner_y in corners:
            if self.is_wall(corner_x, corner_y):
                return False
        
        return True
    
    def get_wall_rect(self, grid_x, grid_y):
        """获取指定网格坐标的墙体矩形"""
        if self.grid[grid_y][grid_x] == 1:
            return pygame.Rect(grid_x * self.TILE_SIZE, grid_y * self.TILE_SIZE, 
                             self.TILE_SIZE, self.TILE_SIZE)
        return None
    
    def get_all_wall_rects(self):
        """获取所有墙体的矩形列表"""
        wall_rects = []
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self.grid[y][x] == 1:
                    wall_rects.append(self.get_wall_rect(x, y))
        return wall_rects
    
    def find_safe_position(self, start_x, start_y, width=28, height=28):
        """找到一个安全的生成位置（不与墙体碰撞）"""
        import random
        
        # 尝试100次找到安全位置
        for _ in range(100):
            x = random.randint(width//2 + self.TILE_SIZE, 
                             self.WIDTH * self.TILE_SIZE - width//2 - self.TILE_SIZE)
            y = random.randint(height//2 + self.TILE_SIZE, 
                             self.HEIGHT * self.TILE_SIZE - height//2 - self.TILE_SIZE)
            
            if self.can_move_to(x, y, width, height):
                return x, y
        
        # 如果找不到安全位置，返回中心位置
        return self.WIDTH * self.TILE_SIZE // 2, self.HEIGHT * self.TILE_SIZE // 2
    
    def is_position_near_walls(self, x, y):
        """检查位置是否离墙体太近"""
        grid_x = int(x // self.TILE_SIZE)
        grid_y = int(y // self.TILE_SIZE)
        
        # 检查周围的网格
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                check_x = grid_x + dx
                check_y = grid_y + dy
                
                if (0 <= check_x < self.WIDTH and 0 <= check_y < self.HEIGHT and 
                    self.grid[check_y][check_x] == 1):
                    return True
        
        return False
