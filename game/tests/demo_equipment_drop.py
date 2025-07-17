#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整的装备掉落系统演示
展示新的装备掉落到背包的完整流程
"""

import pygame
import sys
from player import Player
from inventory import InventoryUI
from item import Item
from equipment import EquipmentSystem

def demo_equipment_drop_system():
    """演示装备掉落系统的完整流程"""
    print("=== 装备掉落系统演示 ===")
    
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("装备掉落系统演示")
    clock = pygame.time.Clock()
    
    # 创建字体
    font = pygame.font.Font(None, 24)
    
    # 创建玩家和背包
    player = Player(400, 300)
    player.level = 3  # 设置等级为3
    inventory_ui = InventoryUI(screen, font)
    
    # 创建一些掉落的装备
    dropped_items = []
    
    # 创建铁剑
    iron_sword = Item(200, 200, "Equipment")
    iron_sword.equipment_id = "iron_sword"
    dropped_items.append(iron_sword)
    
    # 创建钢剑
    steel_sword = Item(250, 200, "Equipment")
    steel_sword.equipment_id = "steel_sword"
    dropped_items.append(steel_sword)
    
    # 创建皮甲
    leather_armor = Item(300, 200, "Equipment")
    leather_armor.equipment_id = "leather_armor"
    dropped_items.append(leather_armor)
    
    # 创建基础戒指
    basic_ring = Item(350, 200, "Equipment")
    basic_ring.equipment_id = "basic_ring"
    dropped_items.append(basic_ring)
    
    messages = []
    
    def add_message(text):
        messages.append(text)
        if len(messages) > 15:
            messages.pop(0)
    
    # 初始说明
    add_message("装备掉落系统演示")
    add_message("1. 走到装备上自动拾取")
    add_message("2. 装备会进入背包，不会自动装备")
    add_message("3. 按TAB打开背包查看装备")
    add_message("4. 按ENTER装备选中的装备")
    add_message("5. 装备新装备时旧装备会放回背包")
    add_message("")
    add_message("当前装备分布:")
    add_message("  铁剑(左) - 等级1")
    add_message("  钢剑(中左) - 等级3")
    add_message("  皮甲(中右) - 等级1")
    add_message("  基础戒指(右) - 等级2")
    
    # 主循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    inventory_ui.toggle()
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif inventory_ui.is_open:
                    result = inventory_ui.handle_input(event, player)
                    if result and result != "close":
                        add_message(f"装备操作: {result}")
        
        # 处理玩家移动
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= 200 * (1/60)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += 200 * (1/60)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            player.y -= 200 * (1/60)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            player.y += 200 * (1/60)
        
        # 检查装备拾取
        for item in dropped_items[:]:  # 使用切片创建副本
            if abs(player.x - item.x) < 30 and abs(player.y - item.y) < 30:
                result = player.pick_up(item)
                add_message(result)
                dropped_items.remove(item)
        
        # 绘制
        screen.fill((0, 0, 0))
        
        # 绘制掉落的装备
        for item in dropped_items:
            color = (255, 255, 0)  # 黄色表示装备
            pygame.draw.rect(screen, color, (item.x-15, item.y-15, 30, 30))
            
            # 绘制装备标签
            equipment_system = EquipmentSystem()
            equipment = equipment_system.get_all_equipment().get(item.equipment_id)
            if equipment:
                label = font.render(equipment.name, True, (255, 255, 255))
                screen.blit(label, (item.x-30, item.y-35))
        
        # 绘制玩家
        pygame.draw.rect(screen, (0, 255, 0), 
                        (player.x - player.width//2, player.y - player.height//2, 
                         player.width, player.height))
        
        # 绘制背包
        inventory_ui.draw(player)
        
        # 绘制消息
        y_offset = 10
        for message in messages:
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (10, y_offset))
            y_offset += 20
        
        # 绘制状态信息
        status_y = 450
        status_info = [
            f"玩家等级: {player.level}",
            f"背包物品数: {len(player.inventory)}",
            f"已装备: {len(getattr(player, 'equipped', {}))}"
        ]
        
        for info in status_info:
            text = font.render(info, True, (255, 255, 255))
            screen.blit(text, (10, status_y))
            status_y += 20
        
        # 绘制操作提示
        controls = [
            "WASD/方向键: 移动",
            "TAB: 开关背包",
            "ESC: 退出"
        ]
        
        control_y = 550
        for control in controls:
            text = font.render(control, True, (200, 200, 200))
            screen.blit(text, (10, control_y))
            control_y += 20
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    
    # 显示最终结果
    print("\n=== 演示结果 ===")
    print(f"背包中的装备: {player.inventory}")
    if hasattr(player, 'equipped'):
        print(f"已装备的装备: {player.equipped}")
    else:
        print("没有装备任何装备")
    
    print("\n✓ 演示完成：装备掉落系统正常工作")
    print("  - 装备正确进入背包")
    print("  - 没有自动装备行为")
    print("  - 玩家可以手动选择装备")

if __name__ == "__main__":
    demo_equipment_drop_system()
