#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WASD移动测试程序
测试新的移动控制系统
"""

import pygame
import sys

def test_wasd_movement():
    """测试WASD移动控制"""
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("WASD移动测试")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 24)
    
    # 玩家位置
    player_x = 400
    player_y = 300
    player_size = 30
    speed = 5
    
    # 移动状态记录
    movement_log = []
    
    print("WASD移动测试开始...")
    print("W: 向上, A: 向左, S: 向下, D: 向右")
    print("ESC: 退出测试")
    
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
                # 记录按键
                elif event.key == pygame.K_w:
                    movement_log.append("W (上)")
                elif event.key == pygame.K_a:
                    movement_log.append("A (左)")
                elif event.key == pygame.K_s:
                    movement_log.append("S (下)")
                elif event.key == pygame.K_d:
                    movement_log.append("D (右)")
                
                # 保持最近10条记录
                if len(movement_log) > 10:
                    movement_log.pop(0)
        
        # 处理连续按键
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:  # W键向上
            player_y -= speed
        if keys[pygame.K_s]:  # S键向下
            player_y += speed
        if keys[pygame.K_a]:  # A键向左
            player_x -= speed
        if keys[pygame.K_d]:  # D键向右
            player_x += speed
        
        # 边界检查
        player_x = max(player_size//2, min(800 - player_size//2, player_x))
        player_y = max(player_size//2, min(600 - player_size//2, player_y))
        
        # 绘制
        screen.fill((0, 0, 0))
        
        # 绘制玩家
        pygame.draw.rect(screen, (0, 255, 0), 
                        (player_x - player_size//2, player_y - player_size//2, 
                         player_size, player_size))
        
        # 绘制位置信息
        pos_text = font.render(f"位置: ({player_x}, {player_y})", True, (255, 255, 255))
        screen.blit(pos_text, (10, 10))
        
        # 绘制控制说明
        control_texts = [
            "WASD移动控制测试",
            "W: 向上移动",
            "A: 向左移动", 
            "S: 向下移动",
            "D: 向右移动",
            "ESC: 退出测试"
        ]
        
        for i, text in enumerate(control_texts):
            color = (255, 255, 0) if i == 0 else (200, 200, 200)
            rendered_text = font.render(text, True, color)
            screen.blit(rendered_text, (10, 50 + i * 25))
        
        # 绘制移动记录
        log_title = font.render("最近按键:", True, (255, 255, 255))
        screen.blit(log_title, (400, 50))
        
        for i, move in enumerate(movement_log[-8:]):  # 显示最近8条
            move_text = font.render(move, True, (100, 255, 100))
            screen.blit(move_text, (400, 80 + i * 20))
        
        # 绘制中心十字
        pygame.draw.line(screen, (50, 50, 50), (0, 300), (800, 300), 1)
        pygame.draw.line(screen, (50, 50, 50), (400, 0), (400, 600), 1)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    test_wasd_movement()
