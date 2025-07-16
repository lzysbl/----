#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试装备掉落到背包功能
验证装备掉落后进入背包而不是自动装备
"""

import pygame
from player import Player
from item import Item
from equipment import EquipmentSystem

def test_equipment_drop_to_inventory():
    """测试装备掉落到背包功能"""
    print("=== 装备掉落到背包测试 ===")
    
    # 初始化pygame
    pygame.init()
    screen = pygame.display.set_mode((100, 100))
    
    # 创建玩家
    player = Player(50, 50)
    player.level = 1  # 低等级，无法装备高级装备
    
    print(f"初始状态:")
    print(f"  背包: {player.inventory}")
    print(f"  已装备: {getattr(player, 'equipped', {})}")
    
    # 测试1: 拾取铁剑
    print(f"\n测试1: 拾取铁剑")
    iron_sword = Item(100, 100, "Equipment")
    iron_sword.equipment_id = "iron_sword"
    
    result = player.pick_up(iron_sword)
    print(f"  拾取结果: {result}")
    print(f"  背包: {player.inventory}")
    print(f"  已装备: {getattr(player, 'equipped', {})}")
    
    # 测试2: 拾取钢剑（等级不足）
    print(f"\n测试2: 拾取钢剑（等级不足）")
    steel_sword = Item(100, 100, "Equipment")
    steel_sword.equipment_id = "steel_sword"
    
    result = player.pick_up(steel_sword)
    print(f"  拾取结果: {result}")
    print(f"  背包: {player.inventory}")
    print(f"  已装备: {getattr(player, 'equipped', {})}")
    
    # 测试3: 拾取皮甲
    print(f"\n测试3: 拾取皮甲")
    leather_armor = Item(100, 100, "Equipment")
    leather_armor.equipment_id = "leather_armor"
    
    result = player.pick_up(leather_armor)
    print(f"  拾取结果: {result}")
    print(f"  背包: {player.inventory}")
    print(f"  已装备: {getattr(player, 'equipped', {})}")
    
    # 验证结果
    expected_items = 3  # 应该有3件装备在背包中
    actual_items = len(player.inventory)
    
    print(f"\n=== 测试结果 ===")
    print(f"背包中装备数量: {actual_items}")
    print(f"预期装备数量: {expected_items}")
    print(f"是否有装备被自动装备: {hasattr(player, 'equipped') and any(player.equipped.values()) if hasattr(player, 'equipped') else False}")
    
    if actual_items == expected_items:
        print("✓ 测试通过：装备正确进入背包，没有自动装备")
        success = True
    else:
        print("✗ 测试失败：装备数量不正确")
        success = False
    
    if hasattr(player, 'equipped') and any(player.equipped.values()):
        print("✗ 测试失败：检测到自动装备行为")
        success = False
    
    pygame.quit()
    return success

if __name__ == "__main__":
    test_equipment_drop_to_inventory()
