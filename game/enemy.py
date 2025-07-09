import pygame
import random

class Enemy:
    """敌人类，随机移动并可被玩家触发战斗"""
    SPEED = 2
    COLOR = (255, 0, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 28
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.hp = 50  # 敌人生命值
        self.attack_power = 10  # 敌人攻击力
        self.max_hp = 50
        self.exp_reward = 50  # 击败后给予的经验值
        self.last_attack_time = 0  # 上次攻击时间，用于攻击冷却

    def is_alive(self):
        """判断敌人是否存活"""
        return self.hp > 0

    def update(self):
        # 随机改变方向
        if random.random() < 0.02:
            self.direction = random.choice(['left', 'right', 'up', 'down'])
        dx = dy = 0
        if self.direction == 'left':
            dx = -self.SPEED
        elif self.direction == 'right':
            dx = self.SPEED
        elif self.direction == 'up':
            dy = -self.SPEED
        elif self.direction == 'down':
            dy = self.SPEED
        self.x += dx
        self.y += dy
        
        # 保持在屏幕范围内
        self.x = max(self.width//2, min(800 - self.width//2, self.x))
        self.y = max(self.height//2, min(600 - self.height//2, self.y))

    def can_attack(self):
        """检查是否可以攻击（攻击冷却）"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time > 1000:  # 1秒攻击冷却
            self.last_attack_time = current_time
            return True
        return False

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.COLOR,
            pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        )

    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
