import pygame
import random
import math

class Enemy:
    """敌人类，随机移动并可被玩家触发战斗"""
    SPEED = 2
    COLOR = (255, 0, 0)

    def __init__(self, x, y, enemy_type="basic"):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 28
        self.direction = random.choice(['left', 'right', 'up', 'down'])
        self.enemy_type = enemy_type
        self.last_attack_time = 0  # 上次攻击时间，用于攻击冷却
        self.ai_state = "patrol"  # AI状态：patrol, chase, attack
        self.player_last_seen = None  # 玩家最后被看到的位置
        self.patrol_center = (x, y)  # 巡逻中心点
        self.sight_range = 100  # 视野范围
        self.chase_range = 150  # 追击范围
        
        # 根据敌人类型设置属性
        self.setup_enemy_stats()

    def setup_enemy_stats(self):
        """根据敌人类型设置属性"""
        if self.enemy_type == "basic":
            self.hp = 50
            self.max_hp = 50
            self.attack_power = 10
            self.attack_damage = 10  # 攻击伤害
            self.exp_reward = 50
            self.level = 1
        elif self.enemy_type == "elite":
            self.hp = 100
            self.max_hp = 100
            self.attack_power = 20
            self.attack_damage = 20  # 攻击伤害
            self.exp_reward = 100
            self.level = 2
            self.COLOR = (150, 0, 0)  # 深红色
            self.SPEED = 3
        elif self.enemy_type == "boss":
            self.hp = 200
            self.max_hp = 200
            self.attack_power = 35
            self.attack_damage = 35  # 攻击伤害
            self.exp_reward = 200
            self.level = 3
            self.COLOR = (100, 0, 0)  # 暗红色
            self.SPEED = 2.5
            self.width = 35
            self.height = 35

    def is_alive(self):
        """判断敌人是否存活"""
        return self.hp > 0

    def distance_to_player(self, player):
        """计算到玩家的距离"""
        return math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2)

    def can_see_player(self, player):
        """检查是否能看到玩家"""
        distance = self.distance_to_player(player)
        return distance <= self.sight_range

    def update(self, player=None, game_map=None):
        """更新敌人状态和AI"""
        if player and self.is_alive():
            self.update_ai(player, game_map)
        else:
            self.patrol(game_map)

    def update_ai(self, player, game_map=None):
        """更新AI状态"""
        distance = self.distance_to_player(player)
        
        # 状态转换逻辑
        if distance <= self.sight_range:
            self.player_last_seen = (player.x, player.y)
            if distance <= 40:  # 攻击距离
                self.ai_state = "attack"
            else:
                self.ai_state = "chase"
        elif distance <= self.chase_range and self.player_last_seen:
            self.ai_state = "chase"
        else:
            self.ai_state = "patrol"
            self.player_last_seen = None
        
        # 执行AI行为
        if self.ai_state == "patrol":
            self.patrol(game_map)
        elif self.ai_state == "chase":
            self.chase_player(player, game_map)
        elif self.ai_state == "attack":
            self.attack_player(player)

    def approach_player(self, player, game_map=None):
        """靠近玩家但不攻击"""
        target_x, target_y = player.x, player.y
        distance = self.distance_to_player(player)
        
        # 如果距离足够近，停止移动
        if distance <= 35:
            return
        
        # 向玩家靠近
        self.move_towards_target(target_x, target_y, game_map)

    def patrol(self, game_map=None):
        """巡逻行为"""
        # 随机改变方向
        if random.random() < 0.02:
            self.direction = random.choice(['left', 'right', 'up', 'down'])
        
        # 计算移动
        dx = dy = 0
        if self.direction == 'left':
            dx = -self.SPEED
        elif self.direction == 'right':
            dx = self.SPEED
        elif self.direction == 'up':
            dy = -self.SPEED
        elif self.direction == 'down':
            dy = self.SPEED
        
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 碰撞检测
        can_move = True
        if game_map:
            can_move = game_map.can_move_to(new_x, new_y, self.width, self.height)
        
        # 在巡逻范围内且没有碰撞时移动
        if (can_move and 
            abs(new_x - self.patrol_center[0]) < 80 and 
            abs(new_y - self.patrol_center[1]) < 80):
            self.x = new_x
            self.y = new_y
        else:
            # 改变方向或向巡逻中心移动
            if random.random() < 0.3:  # 30%概率改变方向
                self.direction = random.choice(['left', 'right', 'up', 'down'])
            else:
                # 向巡逻中心移动
                self.move_towards_target(self.patrol_center[0], self.patrol_center[1], game_map)
        
        # 保持在屏幕范围内
        self.x = max(self.width//2, min(800 - self.width//2, self.x))
        self.y = max(self.height//2, min(600 - self.height//2, self.y))

    def chase_player(self, player, game_map=None):
        """追击玩家"""
        target_x, target_y = self.player_last_seen if self.player_last_seen else (player.x, player.y)
        self.move_towards_target(target_x, target_y, game_map)
    
    def move_towards_target(self, target_x, target_y, game_map=None):
        """向目标移动 - 改进版本防止卡墙"""
        # 计算移动方向
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            # 标准化方向向量
            dx /= distance
            dy /= distance
            
            # 计算移动步长
            if hasattr(self, 'ai_state') and self.ai_state == "chase":
                speed = self.SPEED * 1.2  # 追击时稍快
            else:
                speed = self.SPEED
            
            # 先尝试直接移动
            new_x = self.x + dx * speed
            new_y = self.y + dy * speed
            
            if game_map:
                # 检查是否可以直接移动到目标位置
                if game_map.can_move_to(new_x, new_y, self.width, self.height):
                    self.x = new_x
                    self.y = new_y
                else:
                    # 如果不能直接移动，尝试分别在X和Y轴上移动
                    can_move_x = game_map.can_move_to(new_x, self.y, self.width, self.height)
                    can_move_y = game_map.can_move_to(self.x, new_y, self.width, self.height)
                    
                    if can_move_x and can_move_y:
                        # 优先选择移动距离更大的方向
                        if abs(dx) > abs(dy):
                            self.x = new_x
                        else:
                            self.y = new_y
                    elif can_move_x:
                        self.x = new_x
                    elif can_move_y:
                        self.y = new_y
                    else:
                        # 如果都不能移动，尝试避障
                        self.try_avoid_wall(game_map)
            else:
                self.x = new_x
                self.y = new_y
        
        # 保持在屏幕范围内
        self.x = max(self.width//2, min(800 - self.width//2, self.x))
        self.y = max(self.height//2, min(600 - self.height//2, self.y))

    def attack_player(self, player):
        """攻击玩家状态 - 停止移动，准备攻击"""
        # 在攻击状态下，敌人停止移动
        # 实际的攻击逻辑在主循环中处理
        pass

    def can_attack(self):
        """检查是否可以攻击（攻击冷却）"""
        current_time = pygame.time.get_ticks()
        cooldown = 1500  # 基础冷却时间，增加到1.5秒
        
        # 根据敌人类型调整冷却时间
        if self.enemy_type == "elite":
            cooldown = 1200  # 精英1.2秒
        elif self.enemy_type == "boss":
            cooldown = 1000  # Boss1秒
        
        if current_time - self.last_attack_time > cooldown:
            self.last_attack_time = current_time
            return True
        return False

    def draw(self, surface):
        # 绘制敌人主体
        pygame.draw.rect(
            surface,
            self.COLOR,
            pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)
        )
        
        # 绘制血条
        if self.hp < self.max_hp:
            bar_width = self.width
            bar_height = 4
            bar_x = self.x - bar_width//2
            bar_y = self.y - self.height//2 - 8
            
            # 血条背景
            pygame.draw.rect(surface, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            # 血条
            hp_ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width * hp_ratio, bar_height))
        
        # 绘制攻击冷却指示器
        current_time = pygame.time.get_ticks()
        cooldown = 1500  # 基础冷却时间
        if self.enemy_type == "elite":
            cooldown = 1200
        elif self.enemy_type == "boss":
            cooldown = 1000
        
        time_since_attack = current_time - self.last_attack_time
        if time_since_attack < cooldown:
            # 绘制冷却指示器
            cooldown_ratio = time_since_attack / cooldown
            cooldown_width = int(self.width * cooldown_ratio)
            cooldown_bar_y = self.y - self.height//2 - 12
            
            # 冷却条背景
            pygame.draw.rect(surface, (50, 50, 50), (self.x - self.width//2, cooldown_bar_y, self.width, 2))
            # 冷却条
            pygame.draw.rect(surface, (255, 255, 0), (self.x - self.width//2, cooldown_bar_y, cooldown_width, 2))
        
        # 绘制AI状态指示器（调试用）
        if self.ai_state == "chase":
            pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y - self.height//2 - 15)), 3)
        elif self.ai_state == "attack":
            pygame.draw.circle(surface, (255, 0, 0), (int(self.x), int(self.y - self.height//2 - 15)), 3)

    def get_rect(self):
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

    def try_avoid_wall(self, game_map):
        """尝试避开墙体"""
        # 尝试8个方向的移动
        directions = [
            (1, 0), (0, 1), (-1, 0), (0, -1),  # 4个主方向
            (1, 1), (1, -1), (-1, 1), (-1, -1)  # 4个对角方向
        ]
        
        for dx, dy in directions:
            new_x = self.x + dx * self.SPEED
            new_y = self.y + dy * self.SPEED
            
            if game_map.can_move_to(new_x, new_y, self.width, self.height):
                self.x = new_x
                self.y = new_y
                break
