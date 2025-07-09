#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试修改后的敌人行为
"""

import pygame
import sys
from map import GameMap
from player import Player
from enemy import Enemy
from font_manager import FontManager

def test_enemy_behavior():
    """测试敌人新的行为"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("敌人行为测试")
    clock = pygame.time.Clock()
    font = FontManager.get_chinese_font(18)
    
    # 创建游戏实体
    game_map = GameMap()
    player = Player(x=200, y=200)
    enemy = Enemy(x=500, y=400, enemy_type="basic")
    
    # 测试信息
    info_lines = [
        "敌人行为测试",
        "1. 敌人会跟随玩家但不会自动攻击",
        "2. 敌人会避开墙体，不会卡在墙里",
        "3. 敌人靠近玩家时会停止移动",
        "使用WASD移动，观察敌人行为",
        "ESC退出测试"
    ]
    
    while True:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    player.handle_keydown_movement(event.key, game_map)
        
        # 更新实体
        player.update(game_map)
        enemy.update(player, game_map)
        
        # 计算距离
        distance = enemy.distance_to_player(player)
        
        # 渲染
        screen.fill((0, 0, 0))
        
        # 绘制地图
        game_map.draw(screen)
        
        # 绘制实体
        enemy.draw(screen)
        player.draw(screen)
        
        # 绘制信息
        y_offset = 10
        for line in info_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (10, y_offset))
            y_offset += 20
        
        # 显示实时状态
        status_lines = [
            f"玩家位置: ({player.x}, {player.y})",
            f"敌人位置: ({enemy.x}, {enemy.y})",
            f"距离: {distance:.1f}",
            f"敌人状态: {enemy.ai_state}",
            f"敌人是否可见玩家: {enemy.can_see_player(player)}"
        ]
        
        y_offset = 450
        for line in status_lines:
            text_surface = font.render(line, True, (255, 255, 0))
            screen.blit(text_surface, (10, y_offset))
            y_offset += 20
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    test_enemy_behavior()
