#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试装备显示和功能
"""

import pygame
import sys
from map import GameMap
from player import Player
from inventory import InventoryUI
from font_manager import FontManager
from equipment import EquipmentSystem

def test_equipment_display():
    """测试装备显示和功能"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("装备显示测试")
    clock = pygame.time.Clock()
    
    # 创建游戏实体
    game_map = GameMap()
    player = Player(x=400, y=300)
    
    # 添加所有类型的装备进行测试
    player.inventory = [
        "装备_iron_sword",
        "装备_steel_sword", 
        "装备_leather_armor",
        "装备_chain_mail",
        "装备_magic_ring",
        "装备_power_amulet",
        "Potion",
        "Gold"
    ]
    
    # 使用字体管理器
    font = FontManager.get_chinese_font(20)
    
    # 创建背包界面
    inventory_ui = InventoryUI(screen, font)
    
    # 获取装备系统
    equipment_system = EquipmentSystem()
    equipment_list = equipment_system.get_all_equipment()
    
    print("=== 装备显示测试 ===")
    print(f"玩家背包: {player.inventory}")
    print("装备列表:")
    for eq_id, equipment in equipment_list.items():
        print(f"  {eq_id}: {equipment.name} ({equipment.type})")
    
    # 打开背包
    inventory_ui.toggle()
    
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
                        print(f"装备操作: {result}")
                        print(f"当前装备: {getattr(player, 'equipped', {})}")
            elif inventory_ui.is_open:
                result = inventory_ui.handle_input(event, player)
                if result and result != "close":
                    print(f"装备操作: {result}")
                    print(f"当前装备: {getattr(player, 'equipped', {})}")
        
        # 绘制
        screen.fill((0, 0, 0))
        game_map.draw(screen)
        
        # 绘制玩家
        pygame.draw.rect(screen, (0, 255, 0), 
                        (player.x - player.width//2, player.y - player.height//2, 
                         player.width, player.height))
        
        # 绘制背包
        inventory_ui.draw(player)
        
        # 显示说明
        info_lines = [
            "TAB: 打开/关闭背包",
            "ESC: 退出测试",
            "点击装备: 装备/卸装备",
            "方向键: 选择物品",
            "回车: 使用选中物品"
        ]
        
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (10, 10 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("测试完成")

if __name__ == "__main__":
    test_equipment_display()
