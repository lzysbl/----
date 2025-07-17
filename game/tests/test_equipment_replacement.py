#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试装备替换功能
确保捡到新装备时不会丢失原有装备
"""

import pygame
import sys
import os

def test_equipment_replacement():
    """测试装备替换功能"""
    pygame.init()
    
    # 创建测试用的显示
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("装备替换测试")
    clock = pygame.time.Clock()
    
    # 创建字体
    font = pygame.font.Font(None, 24)
    
    # 导入游戏模块
    from player import Player
    from inventory import InventoryUI
    from equipment import EquipmentSystem
    
    # 创建玩家
    player = Player(400, 300)
    
    # 创建背包界面
    inventory_ui = InventoryUI(screen, font)
    
    # 添加测试装备到背包
    equipment_system = EquipmentSystem()
    player.inventory = [
        "装备_iron_sword",
        "装备_steel_sword", 
        "装备_leather_armor",
        "装备_chain_armor",
        "装备_basic_ring",
        "装备_power_ring"
    ]
    
    # 测试状态
    test_step = 0
    messages = []
    
    def add_message(text):
        messages.append(text)
        if len(messages) > 10:
            messages.pop(0)
    
    def run_test_step():
        nonlocal test_step
        
        if test_step == 0:
            add_message("测试开始：背包中有6件装备")
            add_message("装备: 铁剑, 钢剑, 皮甲, 锁甲, 基础戒指, 力量戒指")
            
        elif test_step == 1:
            # 装备铁剑
            inventory_ui.selected_slot = 0
            result = inventory_ui.use_item(player, 0)
            add_message(f"装备铁剑: {result}")
            add_message(f"背包物品数: {len(player.inventory)}")
            
        elif test_step == 2:
            # 装备钢剑（应该替换铁剑）
            inventory_ui.selected_slot = 0  # 钢剑现在在第一个位置
            result = inventory_ui.use_item(player, 0)
            add_message(f"装备钢剑: {result}")
            add_message(f"背包物品数: {len(player.inventory)}")
            add_message("检查背包是否包含铁剑...")
            has_iron_sword = any("iron_sword" in item for item in player.inventory)
            add_message(f"背包中有铁剑: {has_iron_sword}")
            
        elif test_step == 3:
            # 装备皮甲
            leather_armor_index = next((i for i, item in enumerate(player.inventory) if "leather_armor" in item), -1)
            if leather_armor_index >= 0:
                result = inventory_ui.use_item(player, leather_armor_index)
                add_message(f"装备皮甲: {result}")
                add_message(f"背包物品数: {len(player.inventory)}")
            
        elif test_step == 4:
            # 装备锁甲（应该替换皮甲）
            chain_armor_index = next((i for i, item in enumerate(player.inventory) if "chain_armor" in item), -1)
            if chain_armor_index >= 0:
                result = inventory_ui.use_item(player, chain_armor_index)
                add_message(f"装备锁甲: {result}")
                add_message(f"背包物品数: {len(player.inventory)}")
                has_leather_armor = any("leather_armor" in item for item in player.inventory)
                add_message(f"背包中有皮甲: {has_leather_armor}")
            
        elif test_step == 5:
            # 显示最终状态
            add_message("=== 最终测试结果 ===")
            add_message(f"背包剩余物品: {len(player.inventory)}")
            for i, item in enumerate(player.inventory):
                add_message(f"  {i+1}. {item}")
            
            if hasattr(player, 'equipped'):
                add_message("已装备:")
                for eq_type, eq_id in player.equipped.items():
                    add_message(f"  {eq_type}: {eq_id}")
            
            # 验证测试结果
            expected_items = 4  # 应该剩余4件装备（铁剑、皮甲、基础戒指、力量戒指）
            if len(player.inventory) == expected_items:
                add_message("✓ 测试通过：装备替换正常工作")
            else:
                add_message("✗ 测试失败：装备可能丢失")
        
        test_step += 1
    
    # 主循环
    running = True
    inventory_ui.is_open = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and test_step <= 5:
                    run_test_step()
                elif event.key == pygame.K_ESCAPE:
                    running = False
        
        # 清屏
        screen.fill((0, 0, 0))
        
        # 绘制背包
        inventory_ui.draw(player)
        
        # 绘制测试消息
        y_offset = 10
        for message in messages:
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (10, y_offset))
            y_offset += 25
        
        # 绘制操作提示
        if test_step <= 5:
            hint = font.render("按空格键执行下一步测试", True, (255, 255, 0))
            screen.blit(hint, (10, 550))
        
        hint2 = font.render("按ESC键退出", True, (255, 255, 0))
        screen.blit(hint2, (10, 570))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    test_equipment_replacement()
