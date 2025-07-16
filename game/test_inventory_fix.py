#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试背包系统修复
"""

import pygame
import sys
from map import GameMap
from player import Player
from inventory import InventoryUI
from font_manager import FontManager
from equipment import EquipmentSystem

def test_inventory_fix():
    """测试背包系统修复"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("背包系统修复测试")
    clock = pygame.time.Clock()
    
    # 创建游戏实体
    game_map = GameMap()
    player = Player(x=400, y=300)
    
    # 为玩家添加一些测试物品和装备
    player.inventory = ["Potion", "装备_sword_iron", "装备_armor_leather", "Gold"]
    
    # 模拟已装备的状态
    equipment_system = EquipmentSystem()
    equipment_list = equipment_system.get_all_equipment()
    
    # 给玩家装备一些装备
    player.equipped = {}
    if "sword_iron" in equipment_list:
        player.equipped["weapon"] = equipment_list["sword_iron"]
    if "armor_leather" in equipment_list:
        player.equipped["armor"] = equipment_list["armor_leather"]
    
    # 使用字体管理器
    font = FontManager.get_chinese_font(20)
    
    # 创建背包界面
    inventory_ui = InventoryUI(screen, font)
    
    print("=== 背包系统修复测试 ===")
    print(f"玩家背包: {player.inventory}")
    print(f"已装备物品: {player.equipped}")
    
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
                    if inventory_ui.is_open:
                        print("背包打开")
                    else:
                        print("背包关闭")
                elif event.key == pygame.K_ESCAPE:
                    running = False
                elif inventory_ui.is_open:
                    result = inventory_ui.handle_input(event, player)
                    if result and result != "close":
                        print(f"背包操作: {result}")
            elif inventory_ui.is_open:
                result = inventory_ui.handle_input(event, player)
                if result and result != "close":
                    print(f"背包操作: {result}")
        
        # 绘制
        screen.fill((0, 0, 0))
        game_map.draw(screen)
        
        # 绘制玩家
        pygame.draw.rect(screen, (0, 255, 0), 
                        (player.x - player.width//2, player.y - player.height//2, 
                         player.width, player.height))
        
        # 绘制背包
        try:
            inventory_ui.draw(player)
        except Exception as e:
            print(f"背包绘制错误: {e}")
            # 继续运行，不让程序崩溃
        
        # 显示说明
        info_lines = [
            "TAB: 打开/关闭背包",
            "ESC: 退出测试",
            "点击装备槽: 卸装备",
            "点击背包物品: 使用/装备"
        ]
        
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (10, 10 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("测试完成")

if __name__ == "__main__":
    test_inventory_fix()
