import pygame
from equipment import EquipmentSystem

class InventoryUI:
    """背包界面类"""
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.is_open = False
        self.selected_slot = 0
        self.equipment_list = EquipmentSystem.get_all_equipment()
        
        # 界面配置
        self.bg_color = (40, 40, 40, 200)  # 半透明背景
        self.border_color = (100, 100, 100)
        self.selected_color = (255, 255, 0)
        self.text_color = (255, 255, 255)
        
        # 界面尺寸
        self.width = 600
        self.height = 450
        self.x = (800 - self.width) // 2  # 居中
        self.y = (600 - self.height) // 2
        
        # 装备槽位置
        self.equipment_slots = {
            "weapon": (self.x + 50, self.y + 50, 100, 100),
            "armor": (self.x + 200, self.y + 50, 100, 100), 
            "accessory": (self.x + 350, self.y + 50, 100, 100)
        }
        
        # 背包格子
        self.inventory_start_x = self.x + 50
        self.inventory_start_y = self.y + 200
        self.slot_size = 50
        self.slots_per_row = 10
        self.inventory_rows = 4
    
    def toggle(self):
        """切换背包开关状态"""
        self.is_open = not self.is_open
        if self.is_open:
            self.selected_slot = 0
    
    def handle_input(self, event, player):
        """处理背包输入"""
        if not self.is_open:
            return None
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB or event.key == pygame.K_ESCAPE:
                self.toggle()
                return "close"
            elif event.key == pygame.K_LEFT:
                self.selected_slot = max(0, self.selected_slot - 1)
            elif event.key == pygame.K_RIGHT:
                self.selected_slot = min(len(player.inventory) - 1, self.selected_slot + 1)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                return self.use_selected_item(player)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                return self.handle_mouse_click(event.pos, player)
        
        return None
    
    def handle_mouse_click(self, mouse_pos, player):
        """处理鼠标点击"""
        mx, my = mouse_pos
        
        # 检查是否点击装备槽
        for slot_type, (sx, sy, sw, sh) in self.equipment_slots.items():
            if sx <= mx <= sx + sw and sy <= my <= sy + sh:
                return f"unequip_{slot_type}"
        
        # 检查是否点击背包物品
        for i, item in enumerate(player.inventory):
            slot_x = self.inventory_start_x + (i % self.slots_per_row) * (self.slot_size + 5)
            slot_y = self.inventory_start_y + (i // self.slots_per_row) * (self.slot_size + 5)
            
            if (slot_x <= mx <= slot_x + self.slot_size and 
                slot_y <= my <= slot_y + self.slot_size):
                self.selected_slot = i
                return self.use_item(player, i)
        
        return None
    
    def use_selected_item(self, player):
        """使用选中的物品"""
        if 0 <= self.selected_slot < len(player.inventory):
            return self.use_item(player, self.selected_slot)
        return None
    
    def use_item(self, player, index):
        """使用物品"""
        if index >= len(player.inventory):
            return None
            
        item_name = player.inventory[index]
        
        # 检查是否是装备
        if item_name.startswith("装备_"):
            equipment_id = item_name.split("_")[1]
            if equipment_id in self.equipment_list:
                equipment = self.equipment_list[equipment_id]
                return self.equip_item(player, equipment, index)
        
        # 检查是否是消耗品
        elif item_name == "Potion":
            if player.hp < player.max_hp:
                heal_amount = min(30, player.max_hp - player.hp)
                player.hp += heal_amount
                player.inventory.pop(index)
                if self.selected_slot >= len(player.inventory) and self.selected_slot > 0:
                    self.selected_slot -= 1
                return f"使用血瓶，恢复{heal_amount}点生命值"
        
        return None
    
    def equip_item(self, player, equipment, inventory_index):
        """装备物品"""
        # 检查等级要求
        if player.level < equipment.level_requirement:
            return f"等级不足！需要等级{equipment.level_requirement}"
        
        # 卸下当前装备（如果有）
        old_equipment = None
        if hasattr(player, 'equipped') and equipment.type in player.equipped:
            old_equipment = player.equipped[equipment.type]
            self.unequip_item(player, equipment.type)
        
        # 装备新装备
        if not hasattr(player, 'equipped'):
            player.equipped = {}
        
        player.equipped[equipment.type] = equipment
        player.inventory.pop(inventory_index)
        
        # 应用装备属性
        self.apply_equipment_stats(player, equipment, True)
        
        # 调整选中槽位
        if self.selected_slot >= len(player.inventory) and self.selected_slot > 0:
            self.selected_slot -= 1
        
        return f"装备了 {equipment.name}"
    
    def unequip_item(self, player, equipment_type):
        """卸下装备"""
        if not hasattr(player, 'equipped') or equipment_type not in player.equipped:
            return None
        
        equipment = player.equipped[equipment_type]
        
        # 移除装备属性
        self.apply_equipment_stats(player, equipment, False)
        
        # 将装备放回背包
        player.inventory.append(f"装备_{list(self.equipment_list.keys())[list(self.equipment_list.values()).index(equipment)]}")
        
        # 移除装备
        del player.equipped[equipment_type]
        
        return f"卸下了 {equipment.name}"
    
    def apply_equipment_stats(self, player, equipment, equip=True):
        """应用或移除装备属性"""
        multiplier = 1 if equip else -1
        
        if "attack" in equipment.stats:
            if not hasattr(player, 'base_attack'):
                player.base_attack = getattr(player, 'attack', 20)
            player.attack = player.base_attack + (equipment.stats["attack"] * multiplier)
        
        if "defense" in equipment.stats:
            if not hasattr(player, 'base_defense'):
                player.base_defense = getattr(player, 'defense', 5)
            player.defense = player.base_defense + (equipment.stats["defense"] * multiplier)
        
        if "hp" in equipment.stats:
            hp_change = equipment.stats["hp"] * multiplier
            player.max_hp += hp_change
            player.hp += hp_change  # 装备时也增加当前HP
            player.hp = max(1, min(player.hp, player.max_hp))  # 确保HP在合理范围
        
        if "mp" in equipment.stats:
            mp_change = equipment.stats["mp"] * multiplier
            player.max_mp += mp_change
            player.mp += mp_change  # 装备时也增加当前MP
            player.mp = max(0, min(player.mp, player.max_mp))  # 确保MP在合理范围
    
    def draw(self, player):
        """绘制背包界面"""
        if not self.is_open:
            return
        
        # 创建半透明背景
        overlay = pygame.Surface((800, 600))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(128)
        self.screen.blit(overlay, (0, 0))
        
        # 绘制背包窗口
        pygame.draw.rect(self.screen, self.bg_color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(self.screen, self.border_color, (self.x, self.y, self.width, self.height), 3)
        
        # 标题
        title = self.font.render("背包 (TAB关闭)", True, self.text_color)
        self.screen.blit(title, (self.x + 20, self.y + 10))
        
        # 绘制装备槽
        self.draw_equipment_slots(player)
        
        # 绘制背包物品
        self.draw_inventory_items(player)
        
        # 绘制物品信息
        self.draw_item_info(player)
    
    def draw_equipment_slots(self, player):
        """绘制装备槽"""
        slot_labels = {"weapon": "武器", "armor": "护甲", "accessory": "饰品"}
        
        for slot_type, (sx, sy, sw, sh) in self.equipment_slots.items():
            # 绘制槽位边框
            pygame.draw.rect(self.screen, self.border_color, (sx, sy, sw, sh), 2)
            
            # 绘制标签
            label = self.font.render(slot_labels[slot_type], True, self.text_color)
            self.screen.blit(label, (sx, sy - 25))
            
            # 绘制装备的装备
            if hasattr(player, 'equipped') and slot_type in player.equipped:
                equipment = player.equipped[slot_type]
                name_surface = self.font.render(equipment.name[:4], True, self.text_color)
                text_rect = name_surface.get_rect(center=(sx + sw//2, sy + sh//2))
                self.screen.blit(name_surface, text_rect)
            else:
                # 绘制空槽提示
                empty_text = self.font.render("空", True, (128, 128, 128))
                text_rect = empty_text.get_rect(center=(sx + sw//2, sy + sh//2))
                self.screen.blit(empty_text, text_rect)
    
    def draw_inventory_items(self, player):
        """绘制背包物品"""
        # 背包标题
        inv_title = self.font.render("物品:", True, self.text_color)
        self.screen.blit(inv_title, (self.inventory_start_x, self.inventory_start_y - 30))
        
        for i, item in enumerate(player.inventory):
            slot_x = self.inventory_start_x + (i % self.slots_per_row) * (self.slot_size + 5)
            slot_y = self.inventory_start_y + (i // self.slots_per_row) * (self.slot_size + 5)
            
            # 绘制槽位边框
            color = self.selected_color if i == self.selected_slot else self.border_color
            pygame.draw.rect(self.screen, color, (slot_x, slot_y, self.slot_size, self.slot_size), 2)
            
            # 绘制物品图标或名称
            if item.startswith("装备_"):
                # 装备物品
                item_text = "装"
                text_color = (255, 255, 0)  # 金色
            elif item == "Potion":
                item_text = "药"
                text_color = (255, 0, 0)  # 红色
            elif item == "Gold":
                item_text = "金"
                text_color = (255, 215, 0)  # 金色
            else:
                item_text = item[:2]
                text_color = self.text_color
            
            text_surface = self.font.render(item_text, True, text_color)
            text_rect = text_surface.get_rect(center=(slot_x + self.slot_size//2, slot_y + self.slot_size//2))
            self.screen.blit(text_surface, text_rect)
    
    def draw_item_info(self, player):
        """绘制物品信息"""
        if not player.inventory or self.selected_slot >= len(player.inventory):
            return
        
        item_name = player.inventory[self.selected_slot]
        info_x = self.x + 450
        info_y = self.y + 200
        
        # 绘制信息背景
        pygame.draw.rect(self.screen, (60, 60, 60), (info_x, info_y, 140, 150))
        pygame.draw.rect(self.screen, self.border_color, (info_x, info_y, 140, 150), 2)
        
        info_lines = []
        
        if item_name.startswith("装备_"):
            equipment_id = item_name.split("_")[1]
            if equipment_id in self.equipment_list:
                equipment = self.equipment_list[equipment_id]
                info_lines.append(equipment.name)
                info_lines.append(f"类型: {equipment.type}")
                info_lines.append(f"等级: {equipment.level_requirement}")
                
                if "attack" in equipment.stats:
                    info_lines.append(f"攻击: +{equipment.stats['attack']}")
                if "defense" in equipment.stats:
                    info_lines.append(f"防御: +{equipment.stats['defense']}")
                if "hp" in equipment.stats:
                    info_lines.append(f"生命: +{equipment.stats['hp']}")
                if "mp" in equipment.stats:
                    info_lines.append(f"魔法: +{equipment.stats['mp']}")
        
        elif item_name == "Potion":
            info_lines = ["血瓶", "恢复30点生命值", "", "按回车使用"]
        elif item_name == "Gold":
            info_lines = ["金币", "游戏货币"]
        else:
            info_lines = [item_name, "未知物品"]
        
        # 绘制信息文本
        for i, line in enumerate(info_lines):
            if line:  # 跳过空行
                text_surface = self.font.render(line, True, self.text_color)
                self.screen.blit(text_surface, (info_x + 5, info_y + 10 + i * 20))
