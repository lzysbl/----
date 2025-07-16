#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单的装备替换测试
"""

import pygame
from player import Player
from inventory import InventoryUI
from equipment import EquipmentSystem

def test_equipment_replacement():
    """测试装备替换功能"""
    print("=== 装备替换测试 ===")
    
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    font = pygame.font.Font(None, 24)
    
    # 创建玩家和背包
    player = Player(50, 50)
    player.level = 5  # 设置足够的等级
    inventory_ui = InventoryUI(screen, font)
    
    # 添加两把剑到背包
    player.inventory = ['装备_iron_sword', '装备_steel_sword']
    
    print("初始背包:", player.inventory)
    print("背包物品数:", len(player.inventory))
    
    # 装备第一把剑
    result1 = inventory_ui.use_item(player, 0)
    print("\n装备铁剑:", result1)
    print("装备后背包:", player.inventory)
    print("背包物品数:", len(player.inventory))
    
    # 装备第二把剑（应该替换第一把）
    result2 = inventory_ui.use_item(player, 0)
    print("\n装备钢剑:", result2)
    print("最终背包:", player.inventory)
    print("最终背包物品数:", len(player.inventory))
    
    # 检查装备状态
    if hasattr(player, 'equipped'):
        print("\n已装备:", player.equipped)
    
    # 验证结果
    expected_items = 1  # 应该剩余1件装备（铁剑）
    if len(player.inventory) == expected_items:
        print("\n✓ 测试通过：装备替换正常工作，原装备已放回背包")
        success = True
    else:
        print("\n✗ 测试失败：装备可能丢失")
        success = False
    
    pygame.quit()
    return success

if __name__ == "__main__":
    test_equipment_replacement()
