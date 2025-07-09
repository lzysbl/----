#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完整功能测试：背包系统和敌人生成
"""

import pygame
import sys
from map import GameMap
from player import Player
from enemy_spawner import EnemySpawner
from inventory import InventoryUI
from font_manager import FontManager
from equipment import EquipmentSystem

def test_full_features():
    """测试完整功能"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("完整功能测试")
    clock = pygame.time.Clock()
    
    # 创建游戏实体
    game_map = GameMap()
    player = Player(x=400, y=300)
    
    # 为玩家添加一些测试物品
    player.inventory = ["Potion", "装备_sword_iron", "装备_armor_leather", "Gold"]
    
    # 使用字体管理器
    font = FontManager.get_chinese_font(20)
    
    # 创建背包界面
    inventory_ui = InventoryUI(screen, font)
    
    # 生成敌人
    enemies = EnemySpawner.spawn_enemies(game_map, count=5, player_pos=(player.x, player.y))
    
    # 打印敌人生成信息
    print("=== 敌人生成测试 ===")
    for i, enemy in enumerate(enemies):
        in_wall = not game_map.can_move_to(enemy.x, enemy.y, enemy.width, enemy.height)
        print(f"敌人{i+1}: 位置({enemy.x}, {enemy.y}), 在墙里: {in_wall}")
    
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
                elif event.key == pygame.K_SPACE:
                    # 重新生成敌人
                    enemies = EnemySpawner.spawn_enemies(game_map, count=5, player_pos=(player.x, player.y))
                    print("=== 重新生成敌人 ===")
                    for i, enemy in enumerate(enemies):
                        in_wall = not game_map.can_move_to(enemy.x, enemy.y, enemy.width, enemy.height)
                        print(f"敌人{i+1}: 位置({enemy.x}, {enemy.y}), 在墙里: {in_wall}")
                elif event.key == pygame.K_e:
                    # 显示装备信息
                    if hasattr(player, 'equipped') and player.equipped:
                        print("当前装备:", player.equipped)
                    else:
                        print("没有装备")
                elif inventory_ui.is_open:
                    result = inventory_ui.handle_input(event, player)
                    if result and result != "close":
                        print(f"背包操作: {result}")
                # 移动控制
                elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    player.handle_keydown_movement(event.key, game_map)
            elif inventory_ui.is_open:
                result = inventory_ui.handle_input(event, player)
                if result and result != "close":
                    print(f"背包操作: {result}")
        
        # 更新敌人
        for enemy in enemies:
            enemy.update(player, game_map)
        
        # 绘制
        screen.fill((0, 0, 0))
        game_map.draw(screen)
        
        # 绘制敌人（在墙里的用紫色标记）
        for enemy in enemies:
            if not game_map.can_move_to(enemy.x, enemy.y, enemy.width, enemy.height):
                enemy_color = (255, 0, 255)  # 紫色 = 在墙里
            else:
                enemy_color = (255, 0, 0)  # 红色 = 正常
            
            pygame.draw.rect(screen, enemy_color, 
                           (enemy.x - enemy.width//2, enemy.y - enemy.height//2, 
                            enemy.width, enemy.height))
        
        # 绘制玩家
        pygame.draw.rect(screen, (0, 255, 0), 
                        (player.x - player.width//2, player.y - player.height//2, 
                         player.width, player.height))
        
        # 绘制背包
        inventory_ui.draw(player)
        
        # 显示说明
        info_lines = [
            "TAB: 打开/关闭背包",
            "SPACE: 重新生成敌人",
            "E: 显示装备信息",
            "WASD: 移动",
            "紫色敌人 = 在墙里 (有问题)",
            "红色敌人 = 正常"
        ]
        
        for i, line in enumerate(info_lines):
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (10, 10 + i * 20))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    test_full_features()
