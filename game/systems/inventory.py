import pygame
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from systems.equipment import EquipmentSystem

class InventoryUI:
    """背包界面类"""
    
    def __init__(self, screen, font):
        self.screen = screen
        self.font = font
        self.is_open = False
        self.selected_slot = 0  # 背包物品槽位索引
        self.selected_equipment_slot = None  # 选中的装备槽
        self.equipment_list = EquipmentSystem.get_all_equipment()
        
        # 界面配置
        self.bg_color = (40, 40, 40, 200)  # 半透明背景
        self.border_color = (100, 100, 100)
        self.selected_color = (255, 255, 0)
        self.text_color = (255, 255, 255)
        
        # 装备图标配置
        self.equipment_icons = {
            "weapon": "⚔",
            "armor": "🛡", 
            "accessory": "💍"
        }
        
        # 界面尺寸
        self.width = 600
        self.height = 450
        self.x = (800 - self.width) // 2  # 居中
        self.y = (600 - self.height) // 2
        
        # 装备槽位置 - 在上部显示
        self.equipment_slots = {
            "weapon": (self.x + 50, self.y + 50, 100, 100),
            "armor": (self.x + 200, self.y + 50, 100, 100), 
            "accessory": (self.x + 350, self.y + 50, 100, 100)
        }
        
        # 背包格子 - 留出足够间距
        self.inventory_start_x = self.x + 50
        self.inventory_start_y = self.y + 180
        self.slot_size = 50
        self.slots_per_row = 8  # 减少每行物品数量
        self.inventory_rows = 4
    
    def _get_display_items(self, player):
        """获取显示物品列表（装备不叠加，消耗品叠加）"""
        display_items = []
        seen_items = set()
        for item in player.inventory:
            # 装备类物品不叠加，每个都显示
            if item.startswith("装备_"):
                display_items.append(item)
            # 消耗品叠加显示
            elif item not in seen_items:
                display_items.append(item)
                seen_items.add(item)
        return display_items

    def _get_actual_index(self, player, display_index):
        """根据显示索引获取实际背包索引（考虑装备不叠加）"""
        display_items = self._get_display_items(player)
        if display_index < 0 or display_index >= len(display_items):
            return 0
        
        # 直接返回显示列表中对应位置的物品在原始背包中的索引
        target_item = display_items[display_index]
        
        # 统计在显示列表中该位置之前有多少个相同的装备
        same_item_count = 0
        for i in range(display_index):
            if display_items[i] == target_item:
                same_item_count += 1
        
        # 在原始背包中找到第 (same_item_count + 1) 个匹配的物品
        found_count = 0
        for i, item in enumerate(player.inventory):
            if item == target_item:
                if found_count == same_item_count:
                    return i
                found_count += 1
        return 0

    def _get_display_index(self, player, actual_index):
        """根据实际索引获取显示索引"""
        if actual_index < 0 or actual_index >= len(player.inventory):
            return 0
        target_item = player.inventory[actual_index]
        display_items = self._get_display_items(player)
        for i, item in enumerate(display_items):
            if item == target_item:
                return i
        return 0
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
                display_items = self._get_display_items(player)
                self.selected_slot = max(0, self.selected_slot - 1)
            elif event.key == pygame.K_RIGHT:
                display_items = self._get_display_items(player)
                self.selected_slot = min(len(display_items) - 1, self.selected_slot + 1)
            elif event.key == pygame.K_UP:
                display_items = self._get_display_items(player)
                self.selected_slot = max(0, self.selected_slot - self.slots_per_row)
            elif event.key == pygame.K_DOWN:
                display_items = self._get_display_items(player)
                self.selected_slot = min(len(display_items) - 1, self.selected_slot + self.slots_per_row)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_equipment_slot is not None:
                    return self.unequip_item(player, self.selected_equipment_slot)
                else:
                    return self.use_selected_item(player)
            elif event.key == pygame.K_d:  # D键丢弃
                return self.drop_selected_item(player)
            elif event.key == pygame.K_x:  # X键摧毁
                return self.destroy_selected_item(player)
        
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
                self.selected_equipment_slot = slot_type
                self.selected_slot = -1  # 取消背包物品选中
                # 检查槽位是否有装备
                if hasattr(player, 'equipped') and slot_type in player.equipped and player.equipped[slot_type]:
                    equipment_id = player.equipped[slot_type]
                    if equipment_id in self.equipment_list:
                        equipment = self.equipment_list[equipment_id]
                        return f"选中了已装备的 {equipment.name}"
                return "选中了空装备槽"
        
        # 检查是否点击背包物品（使用统一的显示列表）
        display_items = self._get_display_items(player)
        item_counts = {}
        
        for item in player.inventory:
            item_counts[item] = item_counts.get(item, 0) + 1
        
        for i, item in enumerate(display_items):
            slot_x = self.inventory_start_x + (i % self.slots_per_row) * (self.slot_size + 5)
            slot_y = self.inventory_start_y + (i // self.slots_per_row) * (self.slot_size + 5)
            
            if (slot_x <= mx <= slot_x + self.slot_size and 
                slot_y <= my <= slot_y + self.slot_size):
                self.selected_slot = i  # 直接使用显示列表索引
                self.selected_equipment_slot = None  # 取消装备槽选择
                
                # 装备不显示数量，消耗品显示数量
                if item.startswith("装备_"):
                    return f"选中了 {item}"
                else:
                    count = item_counts[item]
                    if count > 1:
                        return f"选中了 {item} x{count}"
                    else:
                        return f"选中了 {item}"
        
        return None
    
    def use_selected_item(self, player):
        """使用选中的物品（显示列表索引转实际索引）"""
        display_items = self._get_display_items(player)
        if 0 <= self.selected_slot < len(display_items):
            actual_index = self._get_actual_index(player, self.selected_slot)
            return self.use_item(player, actual_index)
        return None
    
    def use_item(self, player, index):
        """使用物品"""
        if index >= len(player.inventory):
            return None
            
        item_name = player.inventory[index]
        
        # 检查是否是装备
        if item_name.startswith("装备_"):
            equipment_id = item_name[3:]  # 去掉 "装备_" 前缀
            if equipment_id in self.equipment_list:
                equipment = self.equipment_list[equipment_id]
                return self.equip_item(player, equipment, index)
        
        # 检查是否是消耗品
        elif item_name == "血瓶":
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
        
        # 先从背包中移除要装备的物品
        item_to_equip = player.inventory.pop(inventory_index)
        
        # 卸下当前装备（如果有）
        if hasattr(player, 'equipped') and equipment.type in player.equipped:
            if player.equipped[equipment.type]:  # 如果有装备
                self.unequip_item(player, equipment.type)
        
        # 装备新装备
        if not hasattr(player, 'equipped'):
            player.equipped = {}
        
        # 找到装备ID
        equipment_id = None
        for eq_id, eq_obj in self.equipment_list.items():
            if eq_obj == equipment:
                equipment_id = eq_id
                break
        
        if equipment_id:
            player.equipped[equipment.type] = equipment_id  # 存储装备ID而不是对象
            
            # 应用装备属性
            self.apply_equipment_stats(player, equipment, True)
            
            # 调整选中槽位
            if self.selected_slot >= len(player.inventory) and self.selected_slot > 0:
                self.selected_slot -= 1
            
            return f"装备了 {equipment.name}"
        else:
            # 装备失败，将物品放回背包
            player.inventory.append(item_to_equip)
            return "装备失败：无法找到装备ID"
    
    def unequip_item(self, player, equipment_type):
        """卸下装备"""
        if not hasattr(player, 'equipped') or equipment_type not in player.equipped:
            return None
        
        equipment_id = player.equipped[equipment_type]
        if not equipment_id:
            return None
        
        # 获取装备对象
        equipment = self.equipment_list.get(equipment_id)
        if not equipment:
            # 装备无效，直接删除
            del player.equipped[equipment_type]
            return "卸下了无效装备"
        
        # 移除装备属性
        self.apply_equipment_stats(player, equipment, False)
        
        # 将装备放回背包
        player.inventory.append(f"装备_{equipment_id}")
        
        # 移除装备
        del player.equipped[equipment_type]
        
        return f"卸下了 {equipment.name}"
    
    def apply_equipment_stats(self, player, equipment, equip=True):
        """应用或移除装备属性"""
        if not equipment or not hasattr(equipment, 'stats'):
            return  # 如果装备无效，直接返回
        
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
        
        # 标题栏
        title = self.font.render("背包 (TAB关闭) | 左键:选中 | 空格:使用 | D:丢弃 | X:摧毁", True, self.text_color)
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
            # 绘制槽位边框，选中时使用高亮颜色
            border_color = self.selected_color if slot_type == self.selected_equipment_slot else self.border_color
            pygame.draw.rect(self.screen, border_color, (sx, sy, sw, sh), 2)
            
            # 绘制标签
            label = self.font.render(slot_labels[slot_type], True, self.text_color)
            self.screen.blit(label, (sx, sy - 25))
            
            # 绘制已装备的装备
            if hasattr(player, 'equipped') and slot_type in player.equipped:
                equipment_id = player.equipped[slot_type]
                if equipment_id and equipment_id in self.equipment_list:
                    equipment = self.equipment_list[equipment_id]
                    # 绘制装备图标
                    icon = self.equipment_icons.get(slot_type, "⚡")
                    icon_surface = self.font.render(icon, True, (255, 215, 0))
                    icon_rect = icon_surface.get_rect(center=(sx + sw//2, sy + sh//2 - 10))
                    self.screen.blit(icon_surface, icon_rect)
                    
                    # 绘制装备名称
                    name_surface = self.font.render(equipment.name[:4], True, self.text_color)
                    name_rect = name_surface.get_rect(center=(sx + sw//2, sy + sh//2 + 15))
                    self.screen.blit(name_surface, name_rect)
                else:
                    # 装备无效，显示空槽图标
                    icon = self.equipment_icons.get(slot_type, "⚡")
                    icon_surface = self.font.render(icon, True, (128, 128, 128))
                    icon_rect = icon_surface.get_rect(center=(sx + sw//2, sy + sh//2))
                    self.screen.blit(icon_surface, icon_rect)
            else:
                # 绘制空槽图标
                icon = self.equipment_icons.get(slot_type, "⚡")
                icon_surface = self.font.render(icon, True, (128, 128, 128))
                icon_rect = icon_surface.get_rect(center=(sx + sw//2, sy + sh//2))
                self.screen.blit(icon_surface, icon_rect)
    
    def draw_inventory_items(self, player):
        """绘制背包物品"""
        # 背包标题
        inv_title = self.font.render("物品:", True, self.text_color)
        self.screen.blit(inv_title, (self.inventory_start_x, self.inventory_start_y - 30))
        
        # 获取物品计数（用于叠加显示）
        item_counts = {}
        for item in player.inventory:
            item_counts[item] = item_counts.get(item, 0) + 1
        
        # 创建显示列表，装备不叠加，消耗品叠加
        display_items = []
        seen_items = set()
        for item in player.inventory:
            # 装备类物品不叠加，每个都显示
            if item.startswith("装备_"):
                display_items.append(item)
            # 消耗品叠加显示
            elif item not in seen_items:
                display_items.append(item)
                seen_items.add(item)
        
        for i, item in enumerate(display_items):
            slot_x = self.inventory_start_x + (i % self.slots_per_row) * (self.slot_size + 5)
            slot_y = self.inventory_start_y + (i // self.slots_per_row) * (self.slot_size + 5)
            
            # 绘制槽位边框
            color = self.selected_color if i == self.selected_slot else self.border_color
            pygame.draw.rect(self.screen, color, (slot_x, slot_y, self.slot_size, self.slot_size), 2)
            
            # 绘制物品图标或名称
            if item.startswith("装备_"):
                # 装备物品 - 显示更清晰的名称
                equipment_id = item[3:]  # 去掉"装备_"前缀
                if equipment_id in self.equipment_list:
                    equipment = self.equipment_list[equipment_id]
                    # 根据装备类型显示不同图标
                    if equipment.type == "weapon":
                        item_text = "⚔"
                    elif equipment.type == "armor":
                        item_text = "🛡"
                    elif equipment.type == "accessory":
                        item_text = "💍"
                    else:
                        item_text = "⚡"
                    text_color = (255, 215, 0)  # 金色
                else:
                    item_text = "?"
                    text_color = (128, 128, 128)  # 灰色
            elif item == "血瓶":
                item_text = "Po"  # 保持原来的显示
                text_color = (255, 100, 100)  # 红色
            elif item == "Gold":
                item_text = "💰"
                text_color = (255, 215, 0)  # 金色
            else:
                item_text = item[:2]
                text_color = self.text_color
            
            # 绘制物品图标
            text_surface = self.font.render(item_text, True, text_color)
            text_rect = text_surface.get_rect(center=(slot_x + self.slot_size//2, slot_y + self.slot_size//2 - 5))
            self.screen.blit(text_surface, text_rect)
            
            # 绘制数量（只对消耗品显示）
            count = item_counts[item]
            if count > 1 and not item.startswith("装备_"):
                count_text = self.font.render(f"x{count}", True, (255, 255, 255))
                count_rect = count_text.get_rect(bottomright=(slot_x + self.slot_size - 2, slot_y + self.slot_size - 2))
                self.screen.blit(count_text, count_rect)
    
    def draw_item_info(self, player):
        """绘制物品信息"""
        # 处理装备槽选中的情况
        if self.selected_equipment_slot is not None and hasattr(player, 'equipped'):
            if (self.selected_equipment_slot in player.equipped and 
                player.equipped[self.selected_equipment_slot]):
                equipment_id = player.equipped[self.selected_equipment_slot]
                if equipment_id in self.equipment_list:
                    item_name = f"装备_{equipment_id}"
                else:
                    return
            else:
                return
        # 处理背包物品选中的情况
        elif self.selected_slot >= 0:
            display_items = self._get_display_items(player)
            if self.selected_slot < len(display_items):
                actual_index = self._get_actual_index(player, self.selected_slot)
                item_name = player.inventory[actual_index]
            else:
                return
        else:
            return
        info_x = self.x + self.width - 150  # 固定在右侧
        info_y = self.y + 50   # 保持在上方
        
        # 绘制信息背景
        pygame.draw.rect(self.screen, (60, 60, 60), (info_x, info_y, 140, 150))
        pygame.draw.rect(self.screen, self.border_color, (info_x, info_y, 140, 150), 2)
        
        info_lines = []
        
        if item_name.startswith("装备_"):
            equipment_id = item_name[3:]  # 去掉 "装备_" 前缀
            if equipment_id in self.equipment_list:
                equipment = self.equipment_list[equipment_id]
                if equipment and hasattr(equipment, 'name'):  # 检查装备是否有效
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
                else:
                    info_lines.append("无效装备")
            else:
                info_lines.append(f"未知装备: {equipment_id}")  # 显示具体的装备ID用于调试
        
        elif item_name == "血瓶":
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
    
    def drop_selected_item(self, player):
        """丢弃选中的物品"""
        display_items = self._get_display_items(player)
        if 0 <= self.selected_slot < len(display_items):
            actual_index = self._get_actual_index(player, self.selected_slot)
            item_name = player.inventory[actual_index]
            player.inventory.pop(actual_index)
            if self.selected_slot >= len(display_items) and self.selected_slot > 0:
                self.selected_slot -= 1
            return f"丢弃了 {item_name}"
        return None
    
    def destroy_selected_item(self, player):
        """摧毁选中的物品"""
        display_items = self._get_display_items(player)
        if 0 <= self.selected_slot < len(display_items):
            actual_index = self._get_actual_index(player, self.selected_slot)
            item_name = player.inventory[actual_index]
            player.inventory.pop(actual_index)
            if self.selected_slot >= len(display_items) and self.selected_slot > 0:
                self.selected_slot -= 1
            return f"摧毁了 {item_name}"
        return None

    def handle_event(self, event, player):
        """处理背包事件"""
        result = self.handle_input(event, player)
        if result == "close":
            return "close"
        
        # 处理鼠标移动高亮
        if event.type == pygame.MOUSEMOTION:
            if self.is_open:
                mx, my = event.pos
                # 检查是否在背包区域内
                if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
                    # 检查是否在装备槽区域
                    for slot_type, (sx, sy, sw, sh) in self.equipment_slots.items():
                        if sx <= mx <= sx + sw and sy <= my <= sy + sh:
                            self.selected_equipment_slot = slot_type
                            return
                    
                    # 检查是否在背包物品区域
                    for i in range(self.inventory_rows * self.slots_per_row):
                        display_index = i  # 默认显示索引
                        actual_index = self._get_actual_index(player, display_index)  # 获取实际索引
                        
                        slot_x = self.inventory_start_x + (i % self.slots_per_row) * (self.slot_size + 5)
                        slot_y = self.inventory_start_y + (i // self.slots_per_row) * (self.slot_size + 5)
                        
                        if (slot_x <= mx <= slot_x + self.slot_size and 
                            slot_y <= my <= slot_y + self.slot_size):
                            self.selected_slot = actual_index  # 更新实际索引
                            return
                else:
                    # 鼠标不在背包区域，取消所有选中
                    self.selected_slot = 0
                    self.selected_equipment_slot = None
    
    def update(self, player):
        """更新背包状态"""
        if not self.is_open:
            return
        
        # 确保选中的槽位始终有效
        if self.selected_slot >= len(player.inventory):
            self.selected_slot = len(player.inventory) - 1
        
        # 更新装备槽的状态
        if hasattr(player, 'equipped'):
            for slot_type in self.equipment_slots.keys():
                equipment_id = player.equipped.get(slot_type)
                if equipment_id is None or equipment_id not in self.equipment_list:
                    # 如果装备无效，自动卸下
                    self.unequip_item(player, slot_type)
        
        # 自动选择第一个有效物品
        if len(player.inventory) > 0 and self.selected_slot == -1:
            self.selected_slot = 0
        
        # 确保背包物品的选中状态正确
        display_items = self._get_display_items(player)
        for i, item in enumerate(display_items):
            actual_index = self._get_actual_index(player, i)
            if actual_index != i:
                # 如果实际索引和显示索引不一致，说明有叠加物品
                if i == self.selected_slot:
                    # 如果当前选中的是叠加的物品，更新为实际索引
                    self.selected_slot = actual_index
                    break
        
        # 更新物品信息框
        if self.selected_slot >= 0 and self.selected_slot < len(player.inventory):
            item_name = player.inventory[self.selected_slot]
            if item_name.startswith("装备_"):
                equipment_id = item_name[3:]  # 去掉 "装备_" 前缀
                if equipment_id in self.equipment_list:
                    equipment = self.equipment_list[equipment_id]
                    # 确保装备的状态是有效的
                    if not hasattr(equipment, 'name') or equipment.name == "":
                        # 装备无效，自动卸下
                        self.unequip_item(player, equipment.type)
                        self.selected_slot = 0  # 重置选中槽位
            else:
                # 确保消耗品的状态是有效的
                if item_name == "血瓶" and player.hp >= player.max_hp:
                    # 生命值已满，血瓶无效
                    self.selected_slot = 0
                elif item_name == "Gold":
                    # 金币始终有效
                    pass
                else:
                    # 其他物品检查名称是否有效
                    if item_name == "" or item_name is None:
                        # 物品无效，移除
                        player.inventory.pop(self.selected_slot)
                        self.selected_slot = 0  # 重置选中槽位
    
    def reset_selection(self):
        """重置选中状态"""
        self.selected_slot = 0
        self.selected_equipment_slot = None
        
        

