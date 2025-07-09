import pygame
import random

class GameState:
    """游戏状态管理"""
    def __init__(self):
        self.state = "playing"  # playing, paused, game_over
        self.battle_messages = []
        self.message_timer = 0
        self.wave_number = 1
        self.enemies_killed = 0
        
    def add_battle_message(self, message):
        """添加战斗信息"""
        self.battle_messages.append(message)
        self.message_timer = pygame.time.get_ticks()
        # 限制消息数量，避免内存占用过多
        if len(self.battle_messages) > 10:
            self.battle_messages.pop(0)
        
    def update_messages(self):
        """更新消息显示"""
        current_time = pygame.time.get_ticks()
        if current_time - self.message_timer > 3000:  # 3秒后清除消息
            self.battle_messages.clear()
            
    def check_wave_complete(self, enemies):
        """检查波次是否完成"""
        if len(enemies) == 0:
            self.wave_number += 1
            return True
        return False
        
    def spawn_new_wave(self):
        """生成新的敌人波次"""
        from enemy import Enemy
        new_enemies = []
        enemy_count = 2 + self.wave_number  # 每波增加敌人数量
        
        for _ in range(enemy_count):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            new_enemies.append(Enemy(x, y))
            
        return new_enemies
