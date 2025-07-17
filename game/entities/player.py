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
        
        # 技能系统相关属性
        self.mp = 100  # 魔法值
        self.max_mp = 100  # 最大魔法值
        self.skill_cooldowns = {}  # 技能冷却时间
        self.projectiles = []  # 投射物列表
        self.buffs = {}  # 增益效果
        self.mp_regen_rate = 1  # 魔法恢复速度
        self.last_mp_regen = 0  # 上次魔法恢复时间

    def is_alive(self):
        """判断玩家是否存活"""
        return self.hp > 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        dx = dy = 0
        current_speed = self.SPEED + self.speed_boost
        if keys[pygame.K_a]:  # A键向左
            dx = -current_speed
        if keys[pygame.K_d]:  # D键向右
            dx = current_speed
        if keys[pygame.K_w]:  # W键向上
            dy = -current_speed
        if keys[pygame.K_s]:  # S键向下
            dy = current_speed
        return dx, dy

    def update(self, game_map=None):
        dx, dy = self.handle_input()
        
        # 保存原始位置
        old_y = self.y
        
        # 尝试移动
        new_x = self.x + dx
        new_y = self.y + dy
        
        # 碰撞检测
        if game_map:
            # 检查X轴移动
            if game_map.can_move_to(new_x, old_y, self.width, self.height):
                self.x = new_x
            
            # 检查Y轴移动
            if game_map.can_move_to(self.x, new_y, self.width, self.height):
                self.y = new_y
        else:
            # 没有地图时直接移动
            self.x = new_x
            self.y = new_y
        
        # 保持玩家在屏幕边界内
        self.x = max(self.width//2, min(800 - self.width//2, self.x))
        self.y = max(self.height//2, min(600 - self.height//2, self.y))
        
        # 更新魔法值恢复
        self.update_mp_regen()
        
        # 更新投射物
        self.update_projectiles()
        
        # 更新增益效果
        self.update_buffs()

    def update_mp_regen(self):
        """更新魔法值恢复"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_mp_regen > 1000:  # 每秒恢复魔法值
            if self.mp < self.max_mp:
                self.mp = min(self.max_mp, self.mp + self.mp_regen_rate)
                self.last_mp_regen = current_time

    def update_projectiles(self):
        """更新投射物"""
        for projectile in self.projectiles[:]:
            # 移动投射物
            dx = projectile["target_x"] - projectile["x"]
            dy = projectile["target_y"] - projectile["y"]
            distance = (dx**2 + dy**2)**0.5
            
            if distance > 0:
                projectile["x"] += (dx / distance) * projectile["speed"]
                projectile["y"] += (dy / distance) * projectile["speed"]
            
            # 检查是否到达目标或超出范围
            if distance < 10 or projectile["x"] < 0 or projectile["x"] > 800 or projectile["y"] < 0 or projectile["y"] > 600:
                self.projectiles.remove(projectile)

    def update_buffs(self):
        """更新增益效果"""
        current_time = pygame.time.get_ticks()
        for buff_name in list(self.buffs.keys()):
            if current_time > self.buffs[buff_name]["end_time"]:
                del self.buffs[buff_name]

    def handle_keydown_movement(self, key, game_map=None):
        """处理按键事件驱动的移动（备用方案，解决输入法问题）"""
        move_distance = self.SPEED + self.speed_boost
        new_x = self.x
        new_y = self.y
        
        if key == pygame.K_a:  # A键向左
            new_x = self.x - move_distance
        elif key == pygame.K_d:  # D键向右
            new_x = self.x + move_distance
        elif key == pygame.K_w:  # W键向上
            new_y = self.y - move_distance
        elif key == pygame.K_s:  # S键向下
            new_y = self.y + move_distance
        
        # 碰撞检测
        if game_map:
            if game_map.can_move_to(new_x, new_y, self.width, self.height):
                self.x = new_x
                self.y = new_y
        else:
            self.x = new_x
            self.y = new_y
        
        # 保持边界
        self.x = max(self.width//2, min(800 - self.width//2, self.x))
        self.y = max(self.height//2, min(600 - self.height//2, self.y))

    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self.color,
            pygame.Rect(self.x-self.width//2, self.y-self.height//2, self.width, self.height)
        )
        
        # 绘制投射物
        for projectile in self.projectiles:
            if projectile["type"] == "fireball":
                pygame.draw.circle(surface, (255, 100, 0), (int(projectile["x"]), int(projectile["y"])), 8)
        
        # 绘制护盾效果
        if "shield" in self.buffs:
            pygame.draw.circle(surface, (0, 100, 255), (int(self.x), int(self.y)), self.width//2 + 5, 2)

    def get_rect(self):
        """获取玩家的矩形区域，用于碰撞检测"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, self.width, self.height)

    # pick_up 方法已定义于此，无需重复定义

    def pick_up(self, item):
        """拾取物品，并加入背包"""
        # 检查是否是叠加物品（只有血瓶等消耗品可以叠加）
        is_stackable = item.name in ["血瓶", "Gold"]
        
        # 如果不是叠加物品，或者是叠加物品但背包中没有，需要检查显示槽位
        if not is_stackable or (is_stackable and item.name not in self.inventory):
            # 计算显示列表长度（去重后的物品数量）
            display_items = []
            seen_items = set()
            for inv_item in self.inventory:
                if inv_item not in seen_items:
                    display_items.append(inv_item)
                    seen_items.add(inv_item)
            
            # 检查背包显示槽位是否已满
            if len(display_items) >= 20:  # 背包最大显示容量
                return "背包已满！"
        
        if item.name == "Gold":
            self.gold += 10
        elif item.name == "血瓶":
            # 血瓶最多携带10个
            potion_count = self.inventory.count("血瓶")
            if potion_count >= 10:
                return "血瓶已满！(最多10个)"
            self.inventory.append(item.name)
            return "拾取了血瓶！"
        elif hasattr(item, 'equipment_id'):
            # 装备物品每个都占用独立槽位，不叠加
            equipment_id = item.equipment_id
            self.inventory.append(f"装备_{equipment_id}")
            
            # 获取装备信息用于显示
            from systems.equipment import EquipmentSystem
            equipment = EquipmentSystem.get_all_equipment().get(equipment_id)
            if equipment:
                return f"获得了 {equipment.name}！已放入背包"
            else:
                return "获得了装备！已放入背包"
        else:
            self.inventory.append(item.name)
            return f"拾取了 {item.name}！"

    def handle_special_input(self):
        """处理特殊按键（如使用物品）"""
        keys = pygame.key.get_pressed()
        
        # H键使用血瓶 - 只在按下瞬间触发
        if keys[pygame.K_h] and not self.h_key_pressed:
            result = self.use_potion()
            self.h_key_pressed = True
            if result:
                return "使用血瓶恢复生命！"
            elif "血瓶" not in self.inventory:
                return "没有血瓶了！"
            elif self.hp >= self.max_hp:
                return "生命值已满！"
            else:
                return "血瓶冷却中..."
        elif not keys[pygame.K_h]:
            self.h_key_pressed = False
        
        return None

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
        # 升级时恢复魔法值
        self.max_mp += 10
        self.mp = self.max_mp

    def use_potion(self):
        """使用血瓶"""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_heal_time < 2000:  # 2秒冷却
            return False
            
        if "血瓶" in self.inventory:
            heal_amount = min(30, self.max_hp - self.hp)
            if heal_amount > 0:  # 只有在需要治疗时才使用
                self.hp += heal_amount
                self.inventory.remove("血瓶")
                self.last_heal_time = current_time
                return True
            else:
                return False
        else:
            return False

    def get_effective_defense(self):
        """获取有效防御力（包括护盾加成）"""
        defense = 0
        
        # 基础防御力
        if hasattr(self, 'base_defense'):
            defense += self.base_defense
        
        # 护盾加成
        if "shield" in self.buffs:
            defense += self.buffs["shield"]["defense"]
        
        return defense
