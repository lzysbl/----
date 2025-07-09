#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
墙体碰撞测试程序
测试玩家和敌人的墙体碰撞功能
"""

import pygame
import sys
from map import GameMap
from player import Player
from enemy import Enemy
from font_manager import FontManager

def test_wall_collision():
    """测试墙体碰撞功能"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("墙体碰撞测试")
    clock = pygame.time.Clock()
    font = FontManager.get_chinese_font(20)
    
    # 创建游戏实体
    game_map = GameMap()
    player = Player(x=100, y=100)
    enemy = Enemy(x=600, y=400, enemy_type="basic")
    
    # 测试信息
    test_messages = []
    
    def add_message(msg):
        test_messages.append(msg)
        if len(test_messages) > 10:
            test_messages.pop(0)
    
    add_message("墙体碰撞测试开始")
    add_message("WASD移动玩家，观察墙体碰撞效果")
    add_message("ESC退出测试")
    
    print("墙体碰撞测试开始...")
    print("玩家使用WASD移动")
    print("敌人会自动移动并测试墙体碰撞")
    print("ESC退出测试")
    
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
                # WASD移动
                elif event.key in [pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d]:
                    old_x, old_y = player.x, player.y
                    player.handle_keydown_movement(event.key, game_map)
                    # 检查是否发生碰撞
                    if player.x == old_x and player.y == old_y:
                        add_message("玩家被墙体阻挡！")
                    else:
                        add_message(f"玩家移动到 ({player.x}, {player.y})")
        
        # 更新实体
        old_enemy_x, old_enemy_y = enemy.x, enemy.y
        enemy.update(player, game_map)
        
        # 检查敌人是否被墙体阻挡
        if enemy.x == old_enemy_x and enemy.y == old_enemy_y:
            if hasattr(enemy, 'last_collision_check') and enemy.last_collision_check:
                add_message("敌人被墙体阻挡！")
        
        player.update(game_map)
        
        # 渲染
        screen.fill((0, 0, 0))
        
        # 绘制地图
        game_map.draw(screen)
        
        # 绘制实体
        enemy.draw(screen)
        player.draw(screen)
        
        # 绘制测试信息
        y_offset = 10
        for msg in test_messages:
            text_surface = font.render(msg, True, (255, 255, 255))
            screen.blit(text_surface, (10, y_offset))
            y_offset += 25
        
        # 绘制玩家位置信息
        pos_text = f"玩家位置: ({player.x}, {player.y})"
        pos_surface = font.render(pos_text, True, (255, 255, 0))
        screen.blit(pos_surface, (10, 550))
        
        # 绘制敌人位置信息
        enemy_pos_text = f"敌人位置: ({enemy.x}, {enemy.y})"
        enemy_pos_surface = font.render(enemy_pos_text, True, (255, 0, 0))
        screen.blit(enemy_pos_surface, (10, 570))
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    test_wall_collision()
