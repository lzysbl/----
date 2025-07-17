import random
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from entities.enemy import Enemy

class EnemySpawner:
    """敌人生成器"""
    
    @staticmethod
    def find_valid_spawn_position(game_map, entity_width=28, entity_height=28, max_attempts=50):
        """找到一个有效的生成位置（不在墙里）"""
        for _ in range(max_attempts):
            # 随机生成位置，避开地图边缘，确保有足够的空间
            margin = max(entity_width, entity_height) // 2 + 5  # 额外留出5像素边距
            x = random.randint(margin, 800 - margin)
            y = random.randint(margin, 600 - margin)
            
            # 检查是否可以放置在这个位置
            if game_map.can_move_to(x, y, entity_width, entity_height):
                return x, y
        
        # 如果找不到有效位置，使用地图的安全位置查找功能
        return game_map.find_safe_position(400, 300, entity_width, entity_height)
    
    @staticmethod
    def spawn_enemy(game_map, enemy_type="basic", avoid_positions=None):
        """生成一个敌人，避开指定位置"""
        max_attempts = 100
        min_distance = 100  # 与避开位置的最小距离
        
        # 创建一个临时敌人来获取正确的尺寸
        temp_enemy = Enemy(0, 0, enemy_type)
        enemy_width = temp_enemy.width
        enemy_height = temp_enemy.height
        
        for _ in range(max_attempts):
            x, y = EnemySpawner.find_valid_spawn_position(game_map, enemy_width, enemy_height)
            
            # 检查是否与避开位置太近
            if avoid_positions:
                too_close = False
                for avoid_x, avoid_y in avoid_positions:
                    distance = ((x - avoid_x) ** 2 + (y - avoid_y) ** 2) ** 0.5
                    if distance < min_distance:
                        too_close = True
                        break
                
                if too_close:
                    continue
            
            # 最终验证位置是否有效
            if game_map.can_move_to(x, y, enemy_width, enemy_height):
                return Enemy(x=x, y=y, enemy_type=enemy_type)
        
        # 如果实在找不到合适位置，使用地图的安全位置
        safe_x, safe_y = game_map.find_safe_position(400, 300, enemy_width, enemy_height)
        return Enemy(x=safe_x, y=safe_y, enemy_type=enemy_type)
    
    @staticmethod
    def spawn_enemies(game_map, count=2, player_pos=None):
        """生成多个敌人"""
        enemies = []
        avoid_positions = [player_pos] if player_pos else []
        
        for _ in range(count):
            enemy = EnemySpawner.spawn_enemy(game_map, "basic", avoid_positions)
            enemies.append(enemy)
            # 将新生成的敌人位置也加入避开列表
            avoid_positions.append((enemy.x, enemy.y))
        
        return enemies
    
    @staticmethod
    def spawn_wave_enemies(game_map, wave_number, player_pos=None):
        """根据波次生成敌人"""
        # 根据波次决定敌人数量和类型
        if wave_number <= 2:
            enemy_count = wave_number + 1
            enemy_types = ["basic"] * enemy_count
        elif wave_number <= 5:
            enemy_count = 3
            enemy_types = ["basic", "basic", "elite"]
        else:
            enemy_count = 4
            if wave_number % 5 == 0:  # 每5波出现boss
                enemy_types = ["basic", "elite", "elite", "boss"]
            else:
                enemy_types = ["basic", "basic", "elite", "elite"]
        
        enemies = []
        avoid_positions = [player_pos] if player_pos else []
        
        for enemy_type in enemy_types:
            enemy = EnemySpawner.spawn_enemy(game_map, enemy_type, avoid_positions)
            enemies.append(enemy)
            avoid_positions.append((enemy.x, enemy.y))
        
        return enemies
