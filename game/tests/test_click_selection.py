#!/usr/bin/env python3
"""
测试背包物品鼠标点击选中功能
"""
import pygame
import sys
import os

# 确保可以导入游戏模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from game_enhanced import Game

def test_click_selection():
    """测试鼠标点击选中功能"""
    # 创建游戏实例
    game = Game()
    
    # 添加测试物品
    print("添加测试物品...")
    game.player.inventory.append("血瓶")
    game.player.inventory.append("血瓶")
    game.player.inventory.append("血瓶")
    game.player.inventory.append("装备_sword_1")
    game.player.inventory.append("装备_sword_2")
    game.player.inventory.append("装备_armor_1")
    game.player.inventory.append("装备_ring_1")
    
    print(f"背包内容: {game.player.inventory}")
    
    # 打开背包
    game.inventory_ui.toggle()
    
    print("游戏启动，背包已打开")
    print("请用鼠标点击不同物品测试选中功能")
    print("按ESC键退出游戏")
    
    # 游戏主循环
    clock = pygame.time.Clock()
    running = True
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.inventory_ui.is_open:
                    result = game.inventory_ui.handle_mouse_click(event.pos, game.player)
                    if result:
                        print(f"点击结果: {result}")
        
        # 更新游戏状态
        game.update()
        
        # 绘制游戏画面
        game.draw()
        
        # 显示帧率
        clock.tick(60)
    
    # 退出游戏
    pygame.quit()
    print("测试完成！")

if __name__ == "__main__":
    test_click_selection()
