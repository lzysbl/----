#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试敌人生成位置，检查是否会卡在墙里
"""

import pygame
import sys
import os

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.map import GameMap
from entities.enemy import Enemy
from entities.enemy_spawner import EnemySpawner

def test_enemy_spawn():
    """测试敌人生成位置"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("敌人生成位置测试")
    clock = pygame.time.Clock()
    
    # 创建地图
    game_map = GameMap()
    
    # 生成一些敌人测试
    enemies = []
    for i in range(10):
        enemy = EnemySpawner.spawn_enemy(game_map, "basic")
        enemies.append(enemy)
        print(f"敌人{i+1}: 位置({enemy.x}, {enemy.y}), 是否在墙里: {not game_map.can_move_to(enemy.x, enemy.y, enemy.width, enemy.height)}")
    
    # 游戏循环
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # 按空格键重新生成敌人
                    enemies.clear()
                    for i in range(10):
                        enemy = EnemySpawner.spawn_enemy(game_map, "basic")
                        enemies.append(enemy)
                        print(f"敌人{i+1}: 位置({enemy.x}, {enemy.y}), 是否在墙里: {not game_map.can_move_to(enemy.x, enemy.y, enemy.width, enemy.height)}")
        
        # 绘制
        screen.fill((0, 0, 0))
        game_map.draw(screen)
        
        # 绘制敌人
        for enemy in enemies:
            # 如果敌人在墙里，用红色标记
            if not game_map.can_move_to(enemy.x, enemy.y, enemy.width, enemy.height):
                enemy_color = (255, 0, 255)  # 紫色表示有问题
            else:
                enemy_color = (255, 0, 0)  # 红色表示正常
            
            pygame.draw.rect(screen, enemy_color, 
                           (enemy.x - enemy.width//2, enemy.y - enemy.height//2, 
                            enemy.width, enemy.height))
        
        # 显示说明
        font = pygame.font.Font(None, 24)
        text = font.render("Press SPACE to regenerate enemies", True, (255, 255, 255))
        screen.blit(text, (10, 10))
        text2 = font.render("Purple = in wall, Red = normal", True, (255, 255, 255))
        screen.blit(text2, (10, 35))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    test_enemy_spawn()
