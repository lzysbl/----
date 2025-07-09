import pygame

class Player:
    """玩家类"""
    SPEED = 4

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.width = 28
        self.height = 28
        self.color = (0, 255, 0)
        self.hp = 100  # 玩家生命值
        self.attack_power = 20  # 玩家攻击力
        self.inventory = []  # 玩家背包，用于存放物品名称
        self.max_hp = 100  # 最大生命值
        self.exp = 0  # 经验值
        self.level = 1  # 等级
        self.gold = 0  # 金币
        self.speed_boost = 0  # 速度提升
        self.last_heal_time = 0  # 上次使用血瓶的时间
        self.h_key_pressed = False  # H键按下状态

    def is_alive(self):
        """判断玩家是否存活"""
        return self.hp > 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        current_speed = self.SPEED + self.speed_boost
        if keys[pygame.K_LEFT]:
            dx = -current_speed
        if keys[pygame.K_RIGHT]:
            dx = current_speed
        if keys[pygame.K_UP]:
            dy = -current_speed
        if keys[pygame.K_DOWN]:
            dy = current_speed
        return dx, dy

    def update(self):
        dx, dy = self.handle_input()
        self.x += dx
        self.y += dy
        
        # 保持玩家在屏幕边界内
        self.x = max(self.width//2, min(800 - self.width//2, self.x))
        self.y = max(self.height//2, min(600 - self.height//2, self.y))

    def handle_keydown_movement(self, key):
        """处理按键事件驱动的移动（备用方案，解决输入法问题）"""
        move_distance = self.SPEED + self.speed_boost
        if key == pygame.K_LEFT:
            self.x -= move_distance
        elif key == pygame.K_RIGHT:
            self.x += move_distance
        elif key == pygame.K_UP:
            self.y -= move_distance
        elif key == pygame.K_DOWN:
            self.y += move_distance
        
        # 保持边界
        self.x = max(self.width//2, min(800 - self.width//2, self.x))
        self.y = max(self.height//2, min(600 - self.height//2, self.y))

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(self.x-self.width//2, self.y-self.height//2, self.width, self.height)
        )

    def get_rect(self):
        """获取玩家的矩形区域，用于碰撞检测"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

    # pick_up 方法已定义于此，无需重复定义

    def pick_up(self, item):
        """拾取物品，并加入背包"""
        if item.name == "Gold":
            self.gold += 10
        else:
            self.inventory.append(item.name)

    def handle_special_input(self):
        """处理特殊按键（如使用物品）"""
        keys = pygame.key.get_pressed()
        
        # H键使用血瓶 - 只在按下瞬间触发
        if keys[pygame.K_h] and not self.h_key_pressed:
            self.use_potion()
            self.h_key_pressed = True
        elif not keys[pygame.K_h]:
            self.h_key_pressed = False

    def gain_exp(self, exp_amount):
        """获得经验值并检查是否升级"""
        self.exp += exp_amount
        if self.exp >= self.level * 100:  # 升级需要的经验值
            self.level_up()

    def level_up(self):
        """升级"""
        self.level += 1
        self.exp = 0
        self.max_hp += 20
        self.hp = self.max_hp  # 升级时恢复满血
        self.attack_power += 5

    def use_potion(self):
        """使用血瓶"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_heal_time < 2000:  # 2秒冷却
            return False
            
        if "Potion" in self.inventory:
            heal_amount = min(30, self.max_hp - self.hp)
            if heal_amount > 0:  # 只有在需要治疗时才使用
                self.hp += heal_amount
                self.inventory.remove("Potion")
                self.last_heal_time = current_time
                return True
            else:
                return False
        else:
            return False
